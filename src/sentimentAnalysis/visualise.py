import os
import pickle
from pathlib import Path
import matplotlib.pyplot as plt

ROOT_DIR = os.path.dirname(os.path.abspath(__file__).split("sentimentAnalysis")[0])
TEMP_FILE_DIR = Path(os.path.join(ROOT_DIR, 'temp_files\\x\\'))

def visualise(dir):
    for company in dir.iterdir():
        datasetDir = Path(os.path.join(TEMP_FILE_DIR, company.name + "\\dataset" ))
        try:
            print(datasetDir)
            with open(str(datasetDir) + "\\features_data", "rb") as f:
                data = pickle.load(f)
                
        except:
            continue
        
        lastCount = 0
        correlation = []
        for date in data:
            
            if(date[1] == []):
                continue
            #print(date[2])

            price = date[2][1]
            for i in range(0, len(date[1])):
                item = date[1][i][0] + "_" + date[1][i][1]
                #form = 
                #print(date[1][i])
                sim = date[1][i][4] 
                addData(correlation,item, sim, price)
            #print(correlation)
        plotCorrelation(correlation)
            
            

def addData(list, item, sim, price):
    if(list == []):
        list.append([item, [[sim, price]]])
        return
    for e in list:
        if(e[0] == item):
            e[1].append([sim, price])
            return
    list.append([item, [[sim, price]]])
        

def plotCorrelation(list):
    for item in list:
        for entry in item[1]:
            x = entry[1]
            y = entry[0]
            # plotting the line 1 points 
            # plotting the points 
            plt.plot(x, y, color='green', linestyle='dashed', linewidth = 3,
                            marker='o', markerfacecolor='blue', markersize=5)
              
            # setting x and y axis range
            plt.ylim(0,1)

            plt.xlim(-100,100)
            
            # naming the x axis
            plt.xlabel('Price Difference from next quarter')
            # naming the y axis
            plt.ylabel('Similarity to last Quarter/Year')  
            plt.title(item[0])
        plt.show()              
       


visualise(TEMP_FILE_DIR)
