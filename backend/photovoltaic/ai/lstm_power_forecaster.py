import joblib
import numpy as np
import tensorflow as tf

class LstmPowerForecaster:
    def __init__(self):
        path_to_artifacts = "./artifacts/"
        self.input_labels = ["Radiacao_Avg", "Temp_Cel_Avg", "Potencia_FV_Avg"]
        self.output_label = "Potencia_FV_Avg"

        self.input_scalers = []
        for i in self.input_labels:
            self.input_scalers.append(joblib.load(path_to_artifacts+f"norm/norm{i}.save"))

        self.output_scaler = joblib.load(path_to_artifacts+f"norm/norm{self.output_label}.save")
        self.model = tf.keras.models.load_model(path_to_artifacts + "lstm/model.h5")

    def preprocessing(self, input_data):
        input_data = np.array(input_data)

        # fill missing values
        input_data[np.isnan(input_data)] = 0
        input_data = input_data.reshape(1, int(input_data.shape[0]/len(self.input_labels)),len(self.input_labels))
        
        for i in range(len(self.input_labels)):
            scaler = self.input_scalers[i]
            aux = scaler.transform(input_data[:,:,i].reshape(-1, 1))
            input_data[:,:,i] = aux.reshape(1, -1)
        return input_data

    def predict(self, input_data):
        return self.model.predict(input_data)

    def postprocessing(self, input_data):
        input_data = self.output_scaler.inverse_transform(input_data)
        return input_data[0].tolist()

    def compute_prediction(self, input_data):
        input_data = self.preprocessing(input_data)
        prediction = self.predict(input_data)
        prediction = self.postprocessing(prediction)

        return prediction