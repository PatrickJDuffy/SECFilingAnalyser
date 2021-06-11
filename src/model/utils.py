import tensorflow as tf
def removeNoneTypePrices(data):
    count = 0
    ret = []
    for i in range(len(data)):
        removeEntry = False
        for price in data[i][2]:
            if price == None:
                removeEntry = True
        if not removeEntry:
            ret.append(data[i])
            count += 1

    return ret


def expandData(data):
    for i in range(len(data)):
        try:
            data[i][2].append(data[i+8][2][0] - data[i][2][0])
            #data[i][2].append(data[i+8][2][0] - data[i][2][0])

        except:
            data[i][2].append(None)

    return data

def removeEmptyPrices(data):
    ret = []
    for i in range(len(data)):
        skip = False
        for price in data[i][2]:
            if price == 0 or price == 0.0 and (data[i] not in ret):
                price = None
                skip = True
                continue
        if skip == False:
            ret.append(data[i])
    return data
    #return ret


def reemovNestings(ret ,l):
    for i in l:
        if type(i) == list:
            reemovNestings(ret, i)
        else:
            ret.append(i)
    return ret


def normaliseCol(df):
    min = df.min()
    max = df.max()
    for value in df:
        value = (value - min) / (max - min)
    return df

def populateItemDataset(form, item, data):
    output = []
    for date in data:
        for entry in date[1]:
            if entry[0] == form and entry[1] == item:
                lis = []
                lis = reemovNestings(lis, [date[0], entry, date[2]])
                output.append(lis)
    return output

def getItems(form, item, data):
    output = []
    for date in data:
        for entry in date[1]:
            if entry[0] == form and entry[1] == item:
                output.append(date[0], [entry], date[2])
    return output

def batchData(data, batchSize):
    output = []
    batch = []
    for entry in data:
        if len(batch) == batchSize:
            output.append(batch)
            batch = []
        batch.append(entry)
    return output

# def changeMissingValues(data):
    
#     for i in range(len(data)):

    