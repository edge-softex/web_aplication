import joblib
import numpy as np
import tensorflow as tf

tf.keras.utils.get_custom_objects().clear()

@tf.keras.utils.register_keras_serializable()
class DLinear(tf.keras.models.Model):
    """
    Input and output data is expected in (batch, timesteps, features) format.
    
    separate_features = False
    Uses all input features to directly estimate output features, using 2 linear layers.
        
    DLinear-I: separate_features = True
    Uses all input features to directly estimate output features, using 2 linear layers
    PER OUTPUT CHANNEL.
    
    """
    def __init__(self, output_steps, output_features, separate_features=False, kernel_size=25):
        super().__init__()
        self.kernel_size = kernel_size
        self.output_steps = output_steps
        self.output_features = output_features
        self.separate_features = separate_features
        
        
    def build(self, input_shape):
        self.kernel_initializer = "he_normal"
        self.built_input_shape = input_shape
        
        if self.separate_features:
            self.trend_dense = []
            self.residual_dense = []
            for feature in range(self.output_features):
                self.trend_dense.append(tf.keras.layers.Dense(self.output_steps,
                                                           kernel_initializer=self.kernel_initializer,
                                                          name="trend_decoder_feature_"+str(feature)))
                self.residual_dense.append(tf.keras.layers.Dense(self.output_steps,
                                                               kernel_initializer=self.kernel_initializer,
                                                              name="residual_decoder_feature_"+str(feature)))   
        else:
            self.trend_dense = tf.keras.layers.Dense(self.output_steps*self.output_features, 
                                                  kernel_initializer=self.kernel_initializer,
                                                 name="trend_recomposer")
            self.residual_dense = tf.keras.layers.Dense(self.output_steps*self.output_features, 
                                                     kernel_initializer=self.kernel_initializer,
                                                    name="residual_recomposer")
    
    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "kernel_size": self.kernel_size,
                "output_steps": self.output_steps,
                "output_features": self.output_features,
                "separate_features": self.separate_features,
            }
        )
        return config

    def call(self, inputs):
        trend = tf.keras.layers.AveragePooling1D(pool_size=self.kernel_size,
                                              strides=1,
                                              padding="same",
                                              name="trend_decomposer")(inputs)
        
        residual = tf.keras.layers.Subtract(name="residual_decomposer")([inputs, trend])
        
        if self.separate_features:
            paths = []

            for feature in range(self.output_features):
                trend_sliced = tf.keras.layers.Lambda(lambda x: x[:, :, feature],
                                                  name="trend_slicer_feature_"+str(feature))(trend)
                trend_sliced = self.trend_dense[feature](trend_sliced)
                trend_sliced = tf.keras.layers.Reshape((self.output_steps, 1),
                                                      name="reshape_trend_feature_"+str(feature))(trend_sliced)
                
                residual_sliced = tf.keras.layers.Lambda(lambda x: x[:, :, feature],
                                                      name="residuals_slicer_feature_"+str(feature))(residual)
                residual_sliced = self.residual_dense[feature](residual_sliced)
                residual_sliced = tf.keras.layers.Reshape((self.output_steps, 1),
                                                          name="reshape_residual_feature_"+str(feature))(residual_sliced)
                
                path = tf.keras.layers.Add(name="recomposer_feature_"+str(feature))([trend_sliced, residual_sliced])
                
                paths.append(path)
                
            reshape = tf.keras.layers.Concatenate(axis=2,
                                              name="output_recomposer")(paths)
        else:
            flat_residual = tf.keras.layers.Flatten()(residual)
            flat_trend = tf.keras.layers.Flatten()(trend)

            residual = self.residual_dense(flat_residual)
            
            trend = self.trend_dense(flat_trend)

            add = tf.keras.layers.Add(name="recomposer")([residual, trend])

            reshape = tf.keras.layers.Reshape((self.output_steps, self.output_features))(add)
        
        return reshape
    
    def summary(self):
        if self.built:
            self.model().summary()
        else:
            # If we haven't built the model, show the normal error message.
            super().summary()
            
    def model(self):
        x = tf.keras.layers.Input(shape=(self.built_input_shape[1:]))
        model = tf.keras.models.Model(inputs=[x],outputs=self.call(x))
        
        return model
    
class DlinearForecaster:
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

        input_data[np.isnan(input_data)] = 0.0
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

        es = tf.keras.callbacks.EarlyStopping(monitor ='val_loss', min_delta = 1e-9, patience = 35, verbose = 0)

        rlr = tf.keras.callbacks.ReduceLROnPlateau(monitor = 'val_loss', factor = 0.1, patience = 15, min_lr=1e-7, verbose = 0)

        mcp =  tf.keras.callbacks.ModelCheckpoint(filepath = "./artifacts/dlinear/model", monitor = 'val_loss', save_best_only= True, save_format="tf")

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