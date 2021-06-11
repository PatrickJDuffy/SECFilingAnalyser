import pickle
import os
from pathlib import Path
from utils import removeNoneTypePrices, expandData, removeEmptyPrices


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


def changeFormat(TEMP_FILE_DIR):
    for company in TEMP_FILE_DIR.iterdir():
        datasetDir = Path(os.path.join(TEMP_FILE_DIR, company.name + "\\dataset" )) 
        try:
            with open(str(datasetDir) + "\\features_data", "rb") as f:
                data = pickle.load(f)
 
                data = data[4:-8]
                data = removeNoneTypePrices(data)                
                data = removeEmptyPrices(data)
                data = expandData(data)

        except:
            
            continue


        for date in data:
            #Change to percent difference in price
            
            date[2][1] = date[2][1]/date[2][0]
            date[2][2] = date[2][2]/date[2][0]
           
             

            if(date[1] == []):
                continue
            for item in date[1]:
                

                try:
                    wordCountDiff = item[4] / item[5]
                except:
                    item = None
                    continue
                entry = [date[0], item, wordCountDiff]
                output = reemovNestings([entry, date[2]])
                print(output)
                formItem = output.pop(2)
                print(formItem, output[1])
                formItem += "_" + output.pop(1)
                if(formItem not in formItems):
                    formItems.append(formItem)

                index = formItems.index(formItem) 
                output.insert(1, index)
                
                dataset.append(output)
                output = []
    return dataset

