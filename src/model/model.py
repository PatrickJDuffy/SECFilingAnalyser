import os
import pickle
from models import nn_2, nn, rnn
import numpy as np
import pandas as pd
import tensorflow as tf
from models import nn
from pathlib import Path
#import keras
#from keras.models import Sequential
#import keras.preprocessing.sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers.experimental.preprocessing import Normalization
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
#from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
#from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
#from keras_visualizer import visualizer 
from sklearn import preprocessing
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from utils import removeNoneTypePrices, expandData, removeEmptyPrices, normaliseCol,\
                    populateItemDataset, batchData, getItems
from preprocess import changeFormat


ROOT_DIR = os.path.dirname(os.path.abspath(__file__).split("model")[0])
TEMP_FILE_DIR = Path(os.path.join(str(ROOT_DIR), 'temp_filesx\\'))

formItems = []
dataset = []

output = []
def removeNestings(l):
    
    for i in l:
        if type(i) == list:
            removeNestings(i)
        else:
            output.append(i)
    return output

# #Load datasets and convert into 
rnns = False
if True:
    #dataset = changeFormat(TEMP_FILE_DIR)
    for company in TEMP_FILE_DIR.iterdir():
        datasetDir = Path(os.path.join(TEMP_FILE_DIR, company.name + "\\dataset" )) 
        try:
            with open(str(datasetDir) + "\\features_data", "rb") as f:
                data = pickle.load(f)

                if not rnns:
                    data = data[4:-8]
                    #data = getItems('10Q', 'Item2', data)
                    data = removeNoneTypePrices(data)                
                    data = removeEmptyPrices(data)
                    data = expandData(data)
                if rnns:
                    data = populateItemDataset('10Q', 'Item2', data)
                    data = batchData(data, 6)

                    print(data)

        except:
            
            continue


        for date in data:
            #Change to percent difference in price
            
            date[2][1] = float(date[2][1])/float(date[2][0])
            date[2][2] = date[2][2]/date[2][0]
           
             

            if(date[1] == []):
                continue
            for item in date[1]:
                try:
                    wordCountDiff = item[4] / item[5]
                except:
                    item = None
                    continue
                entry = [date [0], item, wordCountDiff]
                output = removeNestings([entry, date[2]])
                formItem = output.pop(2)
                formItem += "_" + output.pop(1)
                if(formItem not in formItems):
                    formItems.append(formItem)


                index = formItems.index(formItem) 
                output.insert(1, index)
                
                dataset.append(output)
                output = []
        
    
    if True:
        cols = ["date", "formItem", "negCount", "posCount", "uncertCount", "litCount", "strongModCount", 
        "weakModCount", "consCount", "negDif", "posDif", "uncertDif", "litDif", "strongModDif", "weakModDif", 
        "consDif", "wordCount", "lastWordCount", "wordCountDiff", "sim", "price", "nextYearPriceDiff", 
        "nextQuarterPriceDiff", "next2YearPriceDiff"]
        print(np.array(dataset).shape)

        df = DataFrame(dataset, columns=cols)
        df.dropna(inplace=True, axis=0)
        
        df.drop('date', axis=1, inplace=True)
        # print(len(df), ' Before dropping similarity under x')
        # df = df.drop(df[df.sim > .9].index)
        # print(len(df), ' Before dropping outliers')
        df = df.drop(df[abs(df.nextQuarterPriceDiff) > abs(df.nextQuarterPriceDiff.quantile(.8))].index)
        print(len(df), ' After dropping similarity and outliers')


        ydf = df.nextQuarterPriceDiff
        
        #df.drop('formItem', axis=1, inplace=True)
        df.drop('negCount', axis=1, inplace=True)
        df.drop('posCount', axis=1, inplace=True)
        df.drop('uncertCount', axis=1, inplace=True)
        df.drop('litCount', axis=1, inplace=True)
        df.drop('strongModCount', axis=1, inplace=True)
        df.drop('weakModCount', axis=1, inplace=True)
        df.drop('consCount', axis=1, inplace=True)
        #df.drop('negDif', axis=1, inplace=True) 
        #df.drop('posDif', axis=1, inplace=True)
        df.drop('uncertDif', axis=1, inplace=True)
        #df.drop('litDif', axis=1, inplace=True)
        df.drop('strongModDif', axis=1, inplace=True) 
        df.drop('weakModDif', axis=1, inplace=True)
        #df.drop('consDif', axis=1, inplace=True)
        #df.drop('wordCount', axis=1, inplace=True)
        df.drop('lastWordCount', axis=1, inplace=True)
        #df.drop('wordCountDiff', axis=1, inplace=True)
        #df.drop('sim', axis=1, inplace=True)
        df.drop('price', axis=1, inplace=True)
        df.drop('nextYearPriceDiff', axis=1, inplace=True)
        df.drop('nextQuarterPriceDiff', axis=1, inplace=True)
        df.drop('next2YearPriceDiff', axis=1, inplace=True)
 
        inputLen = len(df.columns)

        X = np.array(df)
        ycon = np.array(ydf)
        ycat = np.array(ydf)
        for i in range(len(ycat)):
            if ycat[i] > 0.2:
                ycat[i] = 1
            # elif ycat[i] > 0:
            #     ycat[i] = 0
            else:
                ycat[i] = 0

        
        scalarX, scalarY = MinMaxScaler(), MinMaxScaler()
        scalarX.fit(X)
        #scalarY.fit(ycon.reshape(len(ycon),1))
        scalarY.fit(ycon.reshape(-1,1))
        X = scalarX.transform(X)
        #y = scalarY.transform(ycon.reshape(len(ycon),1))
        y = scalarY.transform(ycon.reshape(-1,1))
        print(y.mean())
        x_train, x_val_test, y_train, y_val_test = \
            train_test_split(X, ycon, test_size=0.2, random_state=1300)

        x_trainCat, x_val_testCat, y_trainCat, y_val_testCat = \
            train_test_split(X, ycat, test_size=0.2, random_state=1300)


        model = nn(x_train, y_train, inputLen)
        y_pred2 = model.predict(x_val_test)
        y_pred2 = scalarY.inverse_transform(y_pred2)
        zip_object = zip(y_pred2, y_val_test)
        i = 0
        for list1_i, list2_i in zip_object:
            if i > 50:
                break
            print(list1_i, list2_i)
            i = i+1

        
        # modelcat = nn_2(x_trainCat, y_trainCat, inputLen)
        # y_pred1 = modelcat.predict_classes(x_val_testCat)
        # print(confusion_matrix(y_val_testCat, y_pred1, labels=[0, 1]))





