import numpy as np
import tensorflow as tf
import pandas as pd
import keras
import matplotlib.pyplot as plt
from pathlib import Path

# Data Preperation

data_train = pd.read_csv('../data/play/play_train_rounds_merged.csv', header=None)
data_test = pd.read_csv('../data/play/play_test_rounds_merged.csv', header=None)

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

player = ['P0','P1','P2','P3']
trump = ['D','H','S','C','O','U']
played_card = ['PlayedCard']

data_train.columns = cards + cards + player + trump + played_card
data_test.columns = cards + cards + player + trump + played_card
print(f'Raw Data Count -> Train Data: {data_train.shape}, Test Data: {data_test.shape}')

data_train = data_train.drop_duplicates(keep="first")
data_test = data_test.drop_duplicates(keep="first")
print(f'Cleaned Data Count -> Train Data: {data_train.shape}, Test Data: {data_test.shape}')

print(f'Duplicated Hands in Train: {any(data_train[0:36].duplicated())}')
print(f'Duplicated Hands in Test: {any(data_test[0:36].duplicated())}')

# Train and Test Data
x_train = data_train.drop('PlayedCard', axis='columns', inplace=False)
x_test = data_test.drop('PlayedCard', axis='columns', inplace=False)

# Training
y_train_label = data_train['PlayedCard']
y_train = keras.utils.to_categorical(y_train_label, num_classes=36)

model = keras.Sequential()
model.add(keras.layers.Dense(82, activation='relu', input_shape=[82]))
model.add(keras.layers.Dense(59, activation='relu'))
model.add(keras.layers.Dense(55, activation='relu'))
model.add(keras.layers.Dense(36, activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])
history = model.fit(x_train, y_train, epochs=100, batch_size=300, shuffle=True)

model.summary()
#print(model.get_weights())

# Predict and Test
y_pred = model.predict(x_test)

TOTAL_COUNT = len(x_test)
CORRECT_COUNT = 0

for i in range(0,len(y_pred)):
    predicted_played_card = np.where(y_pred[i] == np.amax(y_pred[i]))[0][0]
    real_played_card = data_test.iloc[i]['PlayedCard']

    if int(predicted_played_card) == int(real_played_card):
        CORRECT_COUNT = CORRECT_COUNT + 1

accuracy = (CORRECT_COUNT / TOTAL_COUNT) * 100
print(f'Total Count  : {TOTAL_COUNT}')
print(f'Correct Count: {CORRECT_COUNT}')
print(f'Accuracy     : {accuracy}')

version = "V1"

model.save(f'../models/card_prediction_model_{version}.h5')
