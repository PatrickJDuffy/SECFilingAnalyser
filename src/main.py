import os
import pickle
from threading import *
from collections import Counter
from nltk.corpus import stopwords
from functools import reduce
import re
from datetime import datetime
from numpy.lib import index_tricks

from progressbar.widgets import Bar
from src.similarity.similarity import getVectorizer, fitVectorizer, cos_Sim, tfIDF
from src.preprocessing.preprocessor import preProcess_text
from src.preprocessing.cleanText import clean_text
from src.preprocessing.dataset import createDataset

from src.sentiment import SentimentAnalysis
from src.stockdata.crsp import Stock
from src.utils import checkValidPrices, checkSymbol, findUniqueHeadings, createDirs, getEntries, getDates,\
        removeDir

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def main(ticker, entriesPath,
    	sentiment_Analysis = True , 
        preProcess = True, 
        tf_idf = True, 
        createFeatureSpace = True):

    

    if not os.path.exists(entriesPath):
        print("Entries not found...")
        return

    TEMP_FILE_DIR, CLEAN_TEXT_DIR, SENTIMENT_DIR, PICKLE_DIR, DATASET_DIR = createDirs(ticker)

    with open(str(ROOT_DIR)+ '\\temp_Filesx\\finComps.txt', "r") as f:
        contents = f.read()

        if(ticker in contents):
            print(ticker, ' Ticker already processed')
            return


    #print('check4')
    if not checkSymbol(ticker):
        print(ticker, " No Stock Details")
        with open(str(ROOT_DIR)+ '\\temp_Filesx\\finComps.txt', "+a") as f:
            f.write(ticker + "*******\n")
        removeDir(TEMP_FILE_DIR + "\\dataset")
        removeDir(TEMP_FILE_DIR + "\\clean_files")
        removeDir(TEMP_FILE_DIR + "\\pickle_Files")
        removeDir(TEMP_FILE_DIR + "\\sentimentCount_Files")
        removeDir(TEMP_FILE_DIR)
        return


    print("Starting : " + ticker)



    # Gets filling entries for a given company
    entriesDir = os.listdir(entriesPath)


    # Stores the different headings
    headings = findUniqueHeadings(entriesDir)

    #Reverse Sort to differentiate between item1 and item1A for instance 
    #otherwise item 1A could be wrongly tagged as Item 1
    headings.sort(reverse=True)

    entries = []



    for heading in headings:
        entries.append([heading[0], heading[1], getEntries(entriesDir, heading[1], heading[0])])


    dates = getDates(entries)     

    if not checkValidPrices(ticker, dates):
        print(ticker, ' invalid price data')
        return


    numOfEntries = 0
    for heading in headings:
        for entry in heading:
            numOfEntries = numOfEntries + 1


    if preProcess:
        print(ticker, 'Preprocessing text...')
        start = datetime.now()

        for headings in entries:
            for entry in headings[2]:       
                path = entriesPath + '\\' + entry
                file = open(path + ".txt", "r", encoding="utf8")
                cleanText = clean_text(file.read())               
                words = preProcess_text(cleanText)
                with open(PICKLE_DIR + '\\' + "preProccess_" + entry, 'wb') as f:
                        pickle.dump(words, f)

        end = datetime.now()
        dTime = end - start
        print(ticker, ' Preprocessing text complete in ', dTime.seconds, 's')


    sentimentChanges = [] 

    if sentiment_Analysis:
        print(ticker, ' Starting Sentiment Analysis')
        path = os.path.join(ROOT_DIR, 'sentiment\SentimentWordLists_2018.xlsx')
        SENTIMENT_ANALYSER = SentimentAnalysis.SentimentAnalysis(path)
        start = datetime.now()

        sentimentChanges = SentimentAnalysis.sentiment_Analyzer(entries, sentimentChanges, SENTIMENT_ANALYSER, PICKLE_DIR)

        end = datetime.now()
        dTime = end - start
        print(ticker, ' Sentiment Analysis Complete in ', dTime.seconds, 's')


    if tf_idf:

        print(ticker, ' Inspecting Document Similarity...')

        if not sentiment_Analysis:
            with open(PICKLE_DIR + "\\sentimentChanges_" + ticker, 'rb') as f:
                sentimentChanges = pickle.load(f)
            path = os.path.join(ROOT_DIR, 'sentiment\SentimentWordLists_2018.xlsx')
            SENTIMENT_ANALYSER = SentimentAnalysis.SentimentAnalysis(path)

        start = datetime.now()

        sentimentChanges = tfIDF(entries, sentimentChanges, PICKLE_DIR)

        with open(PICKLE_DIR + "\\sentimentChanges_" + ticker, 'wb') as f:
            pickle.dump(sentimentChanges, f)

        end = datetime.now()
        dTime = end - start
        print(ticker, ' Document Similarity Complete in ', dTime.seconds, 's')


    # take second element for sort
    def takeDate(elem):
        return elem[0]

    
    if createFeatureSpace:
        start = datetime.now()

        if not tf_idf:
            try:
                with open(PICKLE_DIR + "\\sentimentChanges_" + ticker, 'rb') as f:
                    sentimentChanges = pickle.load(f)
            except:
                print(ticker, ' Unable to acquire SentimentChanges file')
                return

        print(ticker, " Creating dataset")
        
        stock = Stock(ticker)
        
        dates.sort(key=takeDate)

        dataset = createDataset(sentimentChanges, dates, ticker, stock, ROOT_DIR)
    	
        path2 = DATASET_DIR +  "\\features"
        with open(path2 + "_data", 'wb') as f:
            pickle.dump(dataset, f)    
        with open(str(ROOT_DIR)+ '\\temp_Filesx\\finComps.txt', "+a") as f:
            f.write(ticker + "\n")
        end = datetime.now()
        dTime = end - start
        print(ticker, ' Feature Space Complete in ', dTime.seconds, 's')


