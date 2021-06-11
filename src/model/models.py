from tensorflow.keras.layers import Dense, LSTM, LeakyReLU
from tensorflow.keras.models import Sequential
from keras_visualizer import visualizer 
import tensorflow as t
from tensorflow.python.keras.layers.core import Dropout
# import os
# os.environ["PATH"] += os.pathsep + 'C:\Program Files\Graphviz\bin'

def nn(x_train, y_train, inputLen):
    model = Sequential()
    model.add(Dropout(.2))
    model.add(Dense(inputLen * 2, input_dim= inputLen))
    model.add(Dense(22, activation='relu'))
    model.add(Dense(16, activation='sigmoid'))
    model.add(Dropout(.2))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(1, activation='linear'))
    
    opt = t.keras.optimizers.Adam(learning_rate=0.01)
    model.compile(loss="mean_squared_error", optimizer=opt, metrics=['mse'])
    model.fit(x_train, y_train, epochs=1, batch_size=1000)
    #visualizer(model, format='png', view=True)
    return model

def nn_2(x_train, y_train, inputLen):
    model = Sequential()
    model.add(Dense(11, input_dim=inputLen, kernel_initializer='normal', activation='relu'))
    model.add(Dense(9, activation='relu'))
    model.add(Dense(3, activation='relu'))
    model.add(Dense(1, activation='tanh', kernel_initializer='normal', name='output'))
    model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=100, batch_size=500)
    visualizer(model, format='png', view=True)
    return model

def rnn(x_train, y_train, inputLen):
    model = Sequential()
    model.add(LSTM(11))
    model.add(Dense(22, activation="relu"))
    model.add(Dense(1, activation='softmax'))
    model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=100, batch_size=500)
    visualizer(model, format='png', view=True)
    return model