import tensorflow.keras as k
import csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.datasets import make_regression
import numpy as np
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
data = []
X = []
y = []
with open(str(ROOT_DIR) +'\\play_tennis.csv', 'r') as csvf:
    csv_reader = csv.reader(csvf, delimiter=',')
    next(csv_reader, None)  # skip the headers
    for row in csv_reader:
        x=[]
        for i in range(1, len(row)-2):
            #print(row[i])
            x.append(float(row[i]))
        X.append(x)
        y.append(float(row[5]))

X = np.array(X)
y = np.array(y)
scalarX, scalarY = MinMaxScaler(), MinMaxScaler()
scalarX.fit(X)
scalarY.fit(y.reshape(14,1))
X = scalarX.transform(X)
y = scalarY.transform(y.reshape(14,1))


x_train, x_val_test, y_train, y_val_test = \
        train_test_split(X, y, test_size=0.5, random_state=10)



model = k.models.Sequential()
model.add(k.layers.Dense(3, input_dim=3, activation='relu')) 
model.add(k.layers.Dense(2, activation='relu')) 
model.add(k.layers.Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam')

model.fit(x_train, y_train, epochs=1, batch_size=100)

y_pred= model.predict_classes(x_val_test)

print(y_pred, y_val_test)

_, accuracy = model.evaluate(x_val_test, y_val_test)
print('Mean squared error: %.8f' % (accuracy))