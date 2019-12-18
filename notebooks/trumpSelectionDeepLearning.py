import numpy as np
import tensorflow as tf
import pandas as pd
import keras
from keras.optimizers import Adadelta
import matplotlib.pyplot as plt
from pathlib import Path

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

y_train_label = data_train['trump']
y_train = keras.utils.to_categorical(y_train_label, num_classes=7)

model = keras.Sequential()
model.add(keras.layers.Dense(36, activation='relu', input_shape=[36]))
model.add(keras.layers.Dense(22, activation='relu'))
model.add(keras.layers.Dense(16, activation='relu'))
model.add(keras.layers.Dense(7, activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='sgd', #'rmsprop', 'sgd', Adadelta()
              metrics=['accuracy'])
history = model.fit(x_train, y_train, epochs=70, batch_size=100, shuffle=True)

model.summary()
#print(model.get_weights())

#Prediction on test data
y_pred = model.predict(x_test)

TOTAL_COUNT = len(x_test)
CORRECT_COUNT = 0

for i in range(0,len(y_pred)):

    predicted_trump = np.where(y_pred[i] == np.amax(y_pred[i]))[0][0]
    real_trump = data_test.iloc[i]['trump']

    if int(predicted_trump) == int(real_trump):
        CORRECT_COUNT = CORRECT_COUNT + 1


accuracy = (CORRECT_COUNT / TOTAL_COUNT) * 100
print(f'Total Count   : {TOTAL_COUNT}')
print(f'Correct Count : {CORRECT_COUNT}')
print(f'Accuracy      : {accuracy}')


#Version  CSV epoch	 Batch size	Layers	                                    Loss	AccTrain	AccTest	FH
#V0	      100	     2500	    9 relu & 1 softmax	                        0.89	0.61	    0.615	No
#V1	      100	     1000	    9 relu & 1 softmax	                        0.8309	0.6365	    0.6344	No
#V2	      100	     150	    1 relu (16) & 1 softmax	                    0.8727	0.6369	    0.6236	No
#V3	      100	     150	    2 relu (22 (dropout(0.1), 16) & 1 softmax	0.8972	0.6273	    0.6293	No
#V4	      100	     150	    2 relu (22, 16) & 1 softmax	                0.8520	0.6316 	    0.6292  No
#V5	      100	     150	    3 relu (36, 22, 16) & 1 softmax	            0.8551	0.6428	    0.6205	No
#V6	      100	     150	    3 relu (35, 28, 21, 14) & 1 softmax	        0.8489	0.6446	    0.6226	No
#V7	      100	     300	    2 relu (22, 16) & 1 softmax	                0.8850	0.6307	    0.6210	No
#V8	      100	     300        1 relu (20) & 1 softmax	                    0.8634  0.6277      0.6240  No
#V9	      100	     3000	    2 relu (22, 16) & 1 softmax	                0.8814	0.6228	    0.6231	No
#V10	  70	     100	    2 relu (22, 16) & 1 softmax	                		    	No

version = "V10"

model.save(f'../models/trump_prediction_model_{version}.h5')
