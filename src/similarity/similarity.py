import pickle
import os
import src.utils
from threading import *
from sklearn.feature_extraction.text import TfidfVectorizer


def getVectorizer(input_type = 'content', max_features_val = 500):
    return TfidfVectorizer(input = input_type, max_features = max_features_val)  

def fitVectorizer(d1, d2, vectorizer):
    with open(d1, 'rb') as f:
        content1 = ' '.join([str(elem) for elem in pickle.load(f)])
    with open(d2, 'rb') as f:
        content2 = ' '.join([str(elem) for elem in pickle.load(f)])
    return vectorizer.fit_transform([content1, content2])

def cos_Sim(tfidf):
    return (tfidf*tfidf.T)[0,1]


def tfIDF(entries, sentimentChanges, PICKLE_DIR):
    for headings in entries:           
        corpus = []     
        for entry in headings[2]:
            path = PICKLE_DIR + '\\preProccess_' + entry
            corpus.append([path, entry])
            lastDoc = ''
            
        docNum = 0
        for document in corpus:
            if docNum == 0:
                lastDoc = document[0]
                docNum += 1
                continue

            if docNum < len(corpus):
                #Gets Vectorizer and fits the model with current and last doc
                vect = getVectorizer()
                tfidf = fitVectorizer(document[0], lastDoc, vect)
                #Finds similarity to last document
                sim = cos_Sim(tfidf)
                #print(sim)
                date = src.utils.getEntryDate(document[1])
                form = src.utils.getEntryForm(document[1])
                item = src.utils.getEntryItem(document[1])
                #list, date, form, item

                index = src.utils.getIndex(sentimentChanges, date, form, item)
                if (index != -1):
                    sentimentChanges[index].append(sim)
                
            lastDoc = document[0]
            docNum += 1

    return sentimentChanges



