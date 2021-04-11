from re import search
import pandas as pd
import math
#from preprocessing import preprocessor
# Reading an excel file using Python
import xlrd
 
class SentimentAnalysis:
    def __init__(self, filePath, upper_case = False):
        upper = 1
        if(upper_case):
            upper = 0
        self.wb = xlrd.open_workbook(filePath)
        print("Initializing SentimentAnalysis")
        negSheet = self.wb.sheet_by_index(1)
        posSheet = self.wb.sheet_by_index(2)
        uncertSheet = self.wb.sheet_by_index(3)
        litSheet = self.wb.sheet_by_index(4)
        strongModSheet = self.wb.sheet_by_index(5)
        weakModSheet = self.wb.sheet_by_index(6)
        consSheet = self.wb.sheet_by_index(7)
        self.negWords = []
        for word in range(0, negSheet.nrows):
            self.negWords.append(negSheet.cell(word, upper).value)
        self.posWords = []
        for word in range(0, posSheet.nrows):
            self.posWords.append(posSheet.cell(word, upper).value)
        self.uncertWords = []
        for word in range(0, uncertSheet.nrows):
            self.uncertWords.append(uncertSheet.cell(word, upper).value)
        self.litWords = []
        for word in range(0, litSheet.nrows):
            self.litWords.append(litSheet.cell(word, upper).value)
        self.strongModWords = []
        for word in range(0, strongModSheet.nrows):
            self.strongModWords.append(strongModSheet.cell(word, upper).value)
        self.weakModWords = []
        for word in range(0, weakModSheet.nrows):
            self.weakModWords.append(weakModSheet.cell(word, upper).value)
        self.consWords = []
        for word in range(0, consSheet.nrows):
            self.consWords.append(consSheet.cell(word, upper).value)

    def binarySearchOnString(self, arr, x):
        l = 0
        r = len(arr) - 1
        while (l <= r): 
            m = math.floor((l + r) / 2)
            if (arr[m] == x): 
                return m
            elif (arr[m] < x): 
                l = m + 1
            else: 
                r = m - 1
        return -1  #   If element is not found  then it will return -1

    def negSentimentCounter(self, words):
        negCount = 0
        for word in words:
            if (self.binarySearchOnString(self.negWords, word) != -1):
                negCount = negCount + 1
        #print (negCount, file)
        return negCount

    def posSentimentCounter(self, words):
        posCount = 0
        for word in words:
            if (self.binarySearchOnString(self.posWords, word) != -1):
                posCount = posCount + 1
        #print (posCount, file)
        return posCount
    def uncertSentimentCounter(self, words):
        uncertCount = 0
        for word in words:
            if (self.binarySearchOnString(self.uncertWords, word) != -1):
                uncertCount = uncertCount + 1
        #print (uncertCount, file)
        return uncertCount
    def litSentimentCounter(self, words):
        litCount = 0
        for word in words:
            if (self.binarySearchOnString(self.litWords, word) != -1):
                litCount = litCount + 1
        #print (litCount, file)
        return litCount
    def strongModSentimentCounter(self, words):
        strongModCount = 0
        for word in words:
            if (self.binarySearchOnString(self.strongModWords, word) != -1):
                strongModCount = strongModCount + 1
        #print (strongModCount, file)
        return strongModCount

    def weakModSentimentCounter(self, words):
        weakModCount = 0
        for word in words:
            if (self.binarySearchOnString(self.weakModWords, word) != -1):
                weakModCount = weakModCount + 1
        #print (weakModCount, file)
        return weakModCount
    def consSentimentCounter(self, words):
        consCount = 0
        for word in words:
            if (self.binarySearchOnString(self.consWords, word) != -1):
                consCount = consCount + 1
        #print (consCount, file)
        return consCount