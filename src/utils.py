import os
import shutil
import pickle
from collections import Counter
from nltk.corpus import stopwords
from functools import reduce
from src.stockdata.crsp import Stock
import re


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#Finds unique form/heading combinations
def findUniqueHeadings(entriesDir):
    Headings = []
    for entry in entriesDir:
        if(entry.endswith('.json')):
            continue

        form = getEntryForm(entry)
        head = getEntryItem(entry)
        isUnique = True
        for heading in Headings:
            if(form == heading[0] and head == heading[1]):
                isUnique = False
                break 
        if isUnique or Headings == []:
            Headings.append([form, head])
        
    return Headings

#Get all entries for a certain form:heading
def getEntries(entriesDir, heading, form):
    entries = []
    for entry in entriesDir:
        head = getEntryItem(entry)
        formType = getEntryForm(entry)
        if(entry.endswith('.json')):
            continue
        elif(heading == head and form == formType):
            entries.append(entry.split(".")[0])

    return entries


def deleteFileContent(pfile):
    pfile.seek(0)
    pfile.truncate()


# take second element for sort
def takeDate(elem):
    return elem[0]

#Gets all filing dates for specific company
def getDates(entries):
    dates  = []
    for heading in entries:
        for entry in heading[2]:
            date = getEntryDate(entry)
            if [date,[]] not in dates:
                dates.append([date, []])
    dates.sort(key=takeDate)
    return dates

#Gets data from entry name
def getEntryData(entry):
    data = []
    date = ''
    types = ''
    appended = False
    date = entry[0:8]
    date = date[0:4] + '/' + date[4:6] + '/' + date[6:8]
    data.append(date)
    types = entry[8:]
    types = types.split('_', 2)
    if(types[0].endswith('A')):
        appended = True
        types[0] = types[0][:-1]
    if(types[0].endswith('405')):
        types[0] = types[0][:-3]   
    data.append(types[0])
    data.append(types[1])
    data.append(appended)
    return data
    #[Date, FormType, Item, Appendage]

def getEntryDate(entry):
    data = getEntryData(entry)
    return data[0]
def getEntryForm(entry):
    data = getEntryData(entry)
    return data[1]
def getEntryItem(entry):
    data = getEntryData(entry)
    return data[2]


#Creates various directories for storing data throughout the processing phase
def createDirs(ticker):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(str(ROOT_DIR)+ '\\temp_Filesx\\' + ticker):
        os.makedirs(str(ROOT_DIR)+ '\\temp_Filesx\\' + ticker)
    TEMP_FILE_DIR = os.path.join(ROOT_DIR, 'temp_filesx\\' + ticker)

    if not os.path.exists(str(ROOT_DIR)+ '\\temp_Filesx\\'+ ticker + '\\clean_Files'):
        os.makedirs(str(TEMP_FILE_DIR) + '\\clean_Files')
    CLEAN_TEXT_DIR = os.path.join(TEMP_FILE_DIR, 'clean_Files')

    if not os.path.exists(str(ROOT_DIR)+ '\\temp_Filesx\\'+ ticker + '\\sentimentCount_Files'):
        os.makedirs(str(TEMP_FILE_DIR) + '\\sentimentCount_Files')
    SENTIMENT_DIR = os.path.join(TEMP_FILE_DIR, 'sentimentCount_Files')

    if not os.path.exists(str(ROOT_DIR)+ '\\temp_Filesx\\'+ ticker + '\\pickle_Files'):
        os.makedirs(str(TEMP_FILE_DIR) + '\\pickle_Files')
    PICKLE_DIR = os.path.join(TEMP_FILE_DIR, 'pickle_Files')    

    if not os.path.exists(str(TEMP_FILE_DIR)+ '\\dataset'):
        os.makedirs(str(TEMP_FILE_DIR) + '\\dataset')
    DATASET_DIR = os.path.join(TEMP_FILE_DIR, 'dataset')

    return TEMP_FILE_DIR, CLEAN_TEXT_DIR, SENTIMENT_DIR, PICKLE_DIR, DATASET_DIR


def seperateTypes(list, type):
    ret = []
    for item in list:
        if(item[1] == type):
            ret.append(item)
    return ret

#Finds index of a multideminsional list
def getIndex(list, date, form, item):
    for i in range(len(list)-1):
        if(list[i][0] == date and list[i][1] == form and list[i][2] == item):
            return i

    return -1


def mapreduce(data):
    cnt = Counter()
    for text in data:
        tokens_in_text = text.split()
        tokens_in_text = map(clean_word, tokens_in_text)
        tokens_in_text = filter(word_not_in_stopwords, tokens_in_text)
        cnt.update(tokens_in_text)
    return cnt

def mapper(text):
    tokens_in_text = text.split()
    tokens_in_text = map(clean_word, tokens_in_text)
    tokens_in_text = filter(word_not_in_stopwords, tokens_in_text)
    return Counter(tokens_in_text)

def reducer(cnt1, cnt2):
    cnt1.update(cnt2)
    return cnt1

def chunk_mapper(chunk):
    mapped = map(mapper, chunk)
    reduced = reduce(reducer, mapped)
    return reduced

def clean_word(word):
    return re.sub(r'[^\w\s]','',word).lower()

def word_not_in_stopwords(word):
    return word not in stopwords.words('english') and word and word.isalpha()

#Checks if the stock has recent stock data to avoid downloading 
# companies filings without price data 
def checkSymbol(ticker):
    stock = Stock(ticker)
    hist = stock.stock.history(period="1mo")
    if (len(hist) == 0):
        print("No Stock Details")
        return False
    return True

#Checks if stock has price data for the duration of its filing history
def checkValidPrices(ticker, dates):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    stock = Stock(ticker)
    for date in dates:
        price = stock.getStockPriceByDate(date[0])
        if (price == -1):
            print("Unable to fetch stock Prices")
            with open(str(ROOT_DIR)+ '\\temp_Filesx\\finComps.txt', "+a") as f:
                f.write(ticker + "*****\n")
            return False
    return True


#Retrieves Cik Number associated with Ticker symbol 
def getCikNumber(iticker):
#    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(str(ROOT_DIR) + '\\SEC_EDGAR_text\\cik_ticker.txt', 'r') as f:
        companies = f.readlines()
    for company in companies:
        temp = company.split('\n')[0]
        comp = temp.split("\t")
        cik = comp[0]
        ticker = comp[1]
        if ticker == iticker:
            return cik
    return -1

def getCompanyDataset(ticker):
    try:
        with open(str(ROOT_DIR) + '\\tempFilesx\\' + ticker + '\\dataset\\features_data.txt', 'r') as f:
            companyData = pickle.load(f)
    except:
        print('Unable to access company data')
        return -1
    return companyData
    

def removeDir(dir_path):
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))
