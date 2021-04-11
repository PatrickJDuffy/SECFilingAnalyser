import os
from datetime import datetime
from similarity.similarity import cos_Similarity
from preprocessing.preprocessor import preProcess_text
from preprocessing.cleanText import clean_text
from preprocessing.preprocessor import pos_text, preProcess_text
from sentiment import SentimentAnalysis
import utils
from yellowbrick.text import PosTagVisualizer

sentiment_Analysis = True
cleanTexts = True
pos_Tag = True
preProcess = True
tf_idf = True



ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
entriesPath = os.path.join(ROOT_DIR, 'SEC-EDGAR-text\\output_files_examples\\batch_0018\\001\\AIG_0000005272')
TEMP_FILE_DIR = os.path.join(ROOT_DIR, 'temp_files')
CLEAN_TEXT_DIR = os.path.join(TEMP_FILE_DIR, 'clean_Files')
PREPROCESS_TEXT_DIR = os.path.join(TEMP_FILE_DIR, 'preprocessed_Files')
ticker = 'AIG'
# Gets filling entries for a given company
entriesDir = os.listdir(entriesPath)

if not os.path.exists(entriesPath):
    print("Entries not found...")
    exit

#headings = SLinkedList()
# Stores the different headings
headings = utils.findUniqueHeadings(entriesDir)
headings.sort(reverse=True)

entries = []

for heading in headings:
    entries.append([heading, utils.getEntries(entriesDir, heading)])

csv_file = open(TEMP_FILE_DIR + '\csv_Ticker_Files\\' + ticker + '.csv' , "+w")


if(cleanTexts  == True):
    print('Cleaning text...')
    start = datetime.now()
    last = ""
    for entry in entries[3][1]:
        path = entriesPath + '\\' + entry
        #print(path)
        file = open(path, "r", encoding="utf8")
        cleanText = clean_text(file.read())

        path2 = CLEAN_TEXT_DIR + '\\clean_' + entry 
        file = open(path2 , "+w")
        file.write(cleanText)
    end = datetime.now()
    dTime = end - start
    print('Cleaning process complete in ', dTime.seconds, 's')


if preProcess:
    print("Preprocessing documents...")
    start = datetime.now()
    for entry in entries[3][1]:
        path = CLEAN_TEXT_DIR + '\\clean_' + entry
        file = open(path, "r")
        words = preProcess_text(file.read())
        path2 = PREPROCESS_TEXT_DIR + '\\preProcess_' + entry 
        file = open(path2 , "+w")
        for word in words:
            file.write(word + " ")
    end = datetime.now()
    dTime = end - start
    print('PreProcessing Complete in ', dTime.seconds, 's')

if tf_idf:
    print('Inspecting Document Similarity...')
    start = datetime.now()
    corpus = []
    for entry in entries[3][1]: 
        path = PREPROCESS_TEXT_DIR + '\\preProcess_' + entry
        corpus.append(path)
        lastDoc = ''
    docNum = 0
    for document in corpus:
        if docNum == 0:
            lastDoc = document
            docNum += 1
            continue
        if docNum <= len(corpus):
            sim = cos_Similarity(document, lastDoc)
            #print(sim)
        lastDoc = document
        docNum += 1
    end = datetime.now()
    dTime = end - start
    print('Document Similarity Complete in ', dTime.seconds, 's')

if sentiment_Analysis:
    print('Sentiment Analysis...')
    start = datetime.now()
    sentimentAnalyzer = SentimentAnalysis.SentimentAnalysis(r"C:\Users\duffy\Documents\FYP bits\SECFilingAnalyser\sentiment\SentimentWordLists_2018.xlsx")
    for entry in entries[3][1]:
        filePath = PREPROCESS_TEXT_DIR + '\\preProcess_' + entry
        words = preProcess_text(open(filePath , "r").read())
        wordCount = len(words)
        negCount = sentimentAnalyzer.negSentimentCounter(words)
        posCount = sentimentAnalyzer.posSentimentCounter(words)
        uncertCount = sentimentAnalyzer.uncertSentimentCounter(words)
        litCount = sentimentAnalyzer.litSentimentCounter(words)
        strongModCount = sentimentAnalyzer.strongModSentimentCounter(words)
        weakModCount = sentimentAnalyzer.weakModSentimentCounter(words)
        consCount = sentimentAnalyzer.consSentimentCounter(words)
        #print(entry, wordCount, negCount, posCount, uncertCount, litCount, strongModCount, weakModCount, consCount)
    end = datetime.now()
    dTime = end - start
    print('Sentiment Analysis Complete in ', dTime.seconds, 's')


# if pos_Tag:
    
#     for entry in entries[0][1]:
#         path = tempFilePath + '\\clean_' + entry 
#         print(path)
#         file = open(path, "r")
#         tagged = pos_text(file.read())
#         #print()
#         viz = PosTagVisualizer()
#         viz.fit(tagged)
#         viz.show()
#         exit



