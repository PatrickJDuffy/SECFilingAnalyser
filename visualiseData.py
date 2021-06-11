import os
import pickle
#from src.model.train import train_nn
import numpy as np
import pandas as pd

from pathlib import Path
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from src.model.utils import removeNoneTypePrices, expandData, removeEmptyPrices


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_FILE_DIR = Path(os.path.join(str(ROOT_DIR), 'src\\temp_filesx\\'))

formItems = []
dataset = []
 
output = []
def reemovNestings(l):
    
    for i in l:
        if type(i) == list:
            reemovNestings(i)
        else:
            output.append(i)
    return output

#Load datasets and convert into 
changeFormat = True
if changeFormat:
    for company in TEMP_FILE_DIR.iterdir():
        datasetDir = Path(os.path.join(TEMP_FILE_DIR, company.name + "\\dataset" )) 
        try:
            with open(str(datasetDir) + "\\features_data", "rb") as f:
                data = pickle.load(f)
                # for date in data:
                #     print(date)

                data = data[4:]
                data = removeNoneTypePrices(data)              
                data = removeEmptyPrices(data)
                data = expandData(data)

                for date in data:
                    print(date)
        except:
            
            continue


        # for date in data:
        #     #Change to percent difference in price
        #     i = 0
        #     for i in range(1, 3):
        #         date[2][i] = date[2][i]/date[2][0]
        #         #date[2][2] = date[2][2]/date[2][0]
           
             

        #     if(date[1] == []):
        #         continue
        #     for item in date[1]:
        #         try:
        #             wordCountDiff = item[4] / item[5]
        #         except:
        #             item = None
        #             continue
        #         entry = [date[0], item, wordCountDiff]
        #         output = reemovNestings([entry, date[2]])
        #         formItem = output.pop(2)
        #         formItem += "_" + output.pop(1)
        #         if(formItem not in formItems):
        #             formItems.append(formItem)


        #         index = formItems.index(formItem) 
        #         output.insert(1, index)
                 
        #         #print(formItem, output)
                
        #         dataset.append(output)
        #         output = []