import joblib
import numpy as np
import tensorflow as tf

class LstmForecaster:
    def __init__(self, model_path):
        self.path_to_artifacts = "./artifacts/"
        self.input_labels = ["irradiance", "temperature_amb"]
        self.output_labels = ["irradiance", "temperature_amb"]
        self.input_steps = 120
        self.output_steps = 5
        self.update = False

        self.input_scalers = [joblib.load(self.path_to_artifacts+f"norm/norm_{feature}.save") for feature in self.input_labels]
        self.output_scalers = [joblib.load(self.path_to_artifacts+f"norm/norm_{feature}.save") for feature in self.output_labels]
        
        self.model = tf.keras.models.load_model(self.path_to_artifacts + model_path)
    
    def preprocessing(self, input_data):
        input_data = np.array(input_data)

        input_data[np.isnan(input_data)] = 0
        input_data = input_data.reshape(1, int(input_data.shape[0]/len(self.input_labels)),len(self.input_labels), order='f')
        
        for i in range(len(self.input_labels)):
            scaler = self.input_scalers[i]
            aux = scaler.transform(input_data[:,:,i].reshape(-1, 1))
            input_data[:,:,i] = aux.reshape(1, -1)
        return input_data

    def predict(self, input_data):
        return self.model.predict(input_data)

    def postprocessing(self, prediction):
        prediction=prediction.reshape(prediction.shape[0],self.output_steps,-1)

        for i in range(len(self.output_labels)):
            scaler = self.output_scalers[i]
            aux = scaler.inverse_transform(prediction[:,:,i].reshape(-1, 1))
            prediction[:,:,i] = aux.reshape(1, -1)

        return prediction[0]

    def compute_prediction(self, input_data):
        input_data = self.preprocessing(input_data)
        prediction = self.predict(input_data)
        prediction = self.postprocessing(prediction)

        return prediction
    
    def update_model(self, model_path):
        self.model = tf.keras.models.load_model(self.path_to_artifacts + model_path)
        self.update = False

    def retraining(self, df):
        df_label = df[self.input_labels]
        df_label = df_label.fillna(df_label.mean())
        df_label = df_label.reset_index(drop=True)

        for i in range(len(self.input_labels)):
            scaler = self.input_scalers[i]
            df_label[self.input_labels[i]] = scaler.transform(df_label[self.input_labels[i]].values.reshape(-1, 1))

        training_input, training_output  = self.split_sequence(df_label)
        training_output = training_output.reshape(training_output.shape[0], training_output.shape[1]*training_output.shape[2])

        es = tf.keras.callbacks.EarlyStopping(monitor ='val_loss', min_delta = 1e-9, patience = 35, verbose = 0)

        rlr = tf.keras.callbacks.ReduceLROnPlateau(monitor = 'val_loss', factor = 0.1, patience = 15, min_lr=1e-7, verbose = 0)

        mcp =  tf.keras.callbacks.ModelCheckpoint(filepath = "./artifacts/lstm/model.h5", monitor = 'val_loss', save_best_only= True)

        self.model.fit(x = training_input, y= training_output, validation_split=0.2, epochs = 1000, batch_size = 512, callbacks = [es,rlr,mcp], verbose = 2)

    def split_sequence(self, sequence):
        X, y = list(), list()
        input_sequence = sequence[self.input_labels]
        output_sequence = sequence[self.output_labels]
        
        for i in range(0,len(sequence)):
            end_ix = i + self.input_steps
            out_end_ix = end_ix + self.output_steps
            if out_end_ix > len(sequence):
                break
            seq_x, seq_y = input_sequence[i:end_ix], output_sequence[end_ix:out_end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return np.array(X), np.array(y)
