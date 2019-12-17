import numpy as np
import tensorflow as tf
import pandas as pd
from tensorflow import keras
from keras.optimizers import Adadelta
import matplotlib.pyplot as plt
from pathlib import Path

from kerastuner import HyperModel
from kerastuner.tuners import RandomSearch

data_train = pd.read_csv('../data/trump/train_rounds_filtered_merged.csv', header=None)
data_test = pd.read_csv('../data/trump/test_rounds_filtered_merged.csv', header=None)

#Data Preperation
cards = [
# Diamonds
'DA','DK','DQ','DJ','D10','D9','D8','D7','D6',
# Hearts
'HA','HK','HQ','HJ','H10','H9','H8','H7','H6',
# Spades
'SA','SK','SQ','SJ','S10','S9','S8','S7','S6',
# Clubs
'CA','CK','CQ','CJ','C10','C9','C8','C7','C6'
]

forehand = ['forehand']
trump = ['trump']


data_train.columns = cards + forehand + trump
data_test.columns = cards + forehand + trump
print(f'Raw Data Count -> Train Data: {data_train.shape}, Test Data: {data_test.shape}')

data_train = data_train.drop_duplicates(keep="first")
data_test = data_test.drop_duplicates(keep="first")
print(f'Cleaned Data Count -> Train Data: {data_train.shape}, Test Data: {data_test.shape}')

print(f'Duplicated Hands in Train: {any(data_train[0:36].duplicated())}')
print(f'Duplicated Hands in Test: {any(data_test[0:36].duplicated())}')

#Create Data to train an to test

x_train = data_train.drop('trump', axis='columns', inplace=False)
x_train = x_train.drop('forehand', axis='columns', inplace=False)

x_test = data_test.drop('trump', axis='columns', inplace=False)
x_test = x_test.drop('forehand', axis='columns', inplace=False)

#Training
class MyHyperModel(HyperModel):

    def __init__(self):
        pass

    def build(self, hp):
        model = keras.Sequential()
        model.add(keras.layers.Dense(36, activation='relu', input_shape=[36]))
        for i in range(hp.Int('num_layers', 3, 9)):
            model.add(keras.layers.Dense(units=hp.Int('units_' + str(i),
                                                min_value=16,
                                                max_value=72,
                                                step=1),
                                        activation='relu'))
        model.add(keras.layers.Dense(7, activation='softmax'))
        model.compile(
            optimizer=keras.optimizers.Adam(
                hp.Choice('learning_rate',
                          values=[0.15e-4, 0.125e-4, 1e-4, 0.75e-5, 0.5e-5])),
            loss='categorical_crossentropy',
            metrics=['accuracy'])

        return model

y_train_label = data_train['trump']
y_train = keras.utils.to_categorical(y_train_label, num_classes=7)

y_test_label = data_test['trump']
y_test = keras.utils.to_categorical(y_test_label, num_classes=7)

hypermodel = MyHyperModel()

# Run Tuner
tuner = RandomSearch(
    hypermodel,
    objective='val_accuracy',
    max_trials=36,
    directory='test_dir')

tuner.search(x=x_train.to_numpy(),
             y=y_train,
             epochs=36,
             batch_size=4096,
             validation_data=(x_test.to_numpy(), y_test))

tuner.search_space_summary()

tuner.results_summary()

models = tuner.get_best_models(num_models=2)

#Version    Epoch   Layers  Layer Size      learning Rate       Acc
#V11, V12   10      1-7     7-54 (Step 2)   [1e-2, 1e-3, 1e-4]  0.6128
#V11, V12   50      1-14    7-72 (Step 2)   [1e-3, 1e-4, 1e-5]


version = "Vnight_1"
models[0].save(f'../models/trump_prediction_model_{version}.h5')
print(f'Wrote Best Model: {version}, Summary:')
models[0].summary()

version = "Vnight_2"
models[1].save(f'../models/trump_prediction_model_{version}.h5')
print(f'Wrote 2nd Model: {version}, Summary:')
models[1].summary()
