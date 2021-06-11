from re import search
import math
#from preprocessing import preprocessor
# Reading an excel file using Python
import xlrd
import threading
import src.utils
import pickle


class ReturningThread(threading.Thread):
    def run(self):
        try:
            if self._target:
                self._result = self._target(*self._args, **self._kwargs)
        finally:
            del self._target, self._args, self._kwargs
    def join(self):
        super().join()
        return self._result 
 
class SentimentAnalysis:
    def __init__(self, filePath, upper_case = False):
        upper = 1
        if(upper_case):
            upper = 0
        self.wb = xlrd.open_workbook(filePath)
        print("Initializing SentimentAnalyser")
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


#Sentiment word Counters, Returns count of words for each type of sentiment.
    def negSentimentCounter(self, words):
        negCount = 0
        for word in words:
            if (self.binarySearchOnString(self.negWords, word) != -1):
                negCount = negCount + 1
                words.remove(word)           
        return negCount

    def posSentimentCounter(self, words):
        posCount = 0
        for word in words:
            if (self.binarySearchOnString(self.posWords, word) != -1):
                posCount = posCount + 1
                words.remove(word)
        return posCount
    def uncertSentimentCounter(self, words):
        uncertCount = 0
        for word in words:
            if (self.binarySearchOnString(self.uncertWords, word) != -1):
                uncertCount = uncertCount + 1
                words.remove(word)
        return uncertCount
    def litSentimentCounter(self, words):
        litCount = 0
        for word in words:
            if (self.binarySearchOnString(self.litWords, word) != -1):
                litCount = litCount + 1
                words.remove(word)
        return litCount
    def strongModSentimentCounter(self, words):
        strongModCount = 0
        for word in words:
            if (self.binarySearchOnString(self.strongModWords, word) != -1):
                strongModCount = strongModCount + 1
                words.remove(word)
        return strongModCount

    def weakModSentimentCounter(self, words):
        weakModCount = 0
        for word in words:
            if (self.binarySearchOnString(self.weakModWords, word) != -1):
                weakModCount = weakModCount + 1
                words.remove(word)
        return weakModCount
    def consSentimentCounter(self, words):
        consCount = 0
        for word in words:
            if (self.binarySearchOnString(self.consWords, word) != -1):
                consCount = consCount + 1
                words.remove(word)
        return consCount

    def getSentimentCounts(self, words):
        consCount=0
        weakModCount=0
        strongModCount=0
        litCount=0
        uncertCount=0
        posCount=0
        negCount=0
        for word in words:
            if (self.binarySearchOnString(self.negWords, word) != -1):
                negCount = negCount + 1
            elif (self.binarySearchOnString(self.posWords, word) != -1):
                posCount = posCount + 1
            elif (self.binarySearchOnString(self.consWords, word) != -1):
                consCount = consCount + 1
            elif (self.binarySearchOnString(self.uncertWords, word) != -1):
                uncertCount = uncertCount + 1
            elif (self.binarySearchOnString(self.weakModWords, word) != -1):
                weakModCount = weakModCount + 1
            elif (self.binarySearchOnString(self.strongModWords, word) != -1):
                strongModCount = strongModCount + 1
            elif (self.binarySearchOnString(self.litWords, word) != -1):
                litCount = litCount + 1

        return [negCount, posCount, uncertCount, litCount, strongModCount, weakModCount, consCount]
        

    def getSentimentofWord(self, word):
        sentiment = ''
        if (self.binarySearchOnString(self.consWords, word) != -1):
            sentiment = 'Constrain'
        elif (self.binarySearchOnString(self.weakModWords, word) != -1):
            sentiment = 'WeakMod'
        elif (self.binarySearchOnString(self.strongModWords, word) != -1):
            sentiment = 'StrongMod'
        elif (self.binarySearchOnString(self.litWords, word) != -1):
            sentiment = 'Litigious'
        elif (self.binarySearchOnString(self.uncertWords, word) != -1):
            sentiment = 'Uncertain'
        elif (self.binarySearchOnString(self.posWords, word) != -1):
            sentiment = 'Positive'
        elif (self.binarySearchOnString(self.negWords, word) != -1):
            sentiment = 'Negative'
        return sentiment

    def getSentimentofChange(self, count):
        consCount=0
        weakModCount=0
        strongModCount=0
        litCount=0
        uncertCount=0
        posCount=0
        negCount=0
        #Bottle Neck, possibly implement threading on chuncks of words to speed up
        
        for word in count:
            if (self.binarySearchOnString(self.negWords, word) != -1):
                negCount = negCount + count.get(word)
            elif (self.binarySearchOnString(self.posWords, word) != -1):
                posCount = posCount + count.get(word)
            elif (self.binarySearchOnString(self.uncertWords, word) != -1):
                uncertCount = uncertCount + count.get(word)
            elif (self.binarySearchOnString(self.litWords, word) != -1):
                litCount = litCount + count.get(word)
            elif (self.binarySearchOnString(self.consWords, word) != -1):
                consCount = consCount + count.get(word)
            elif (self.binarySearchOnString(self.weakModWords, word) != -1):
                weakModCount = weakModCount + count.get(word)
            elif (self.binarySearchOnString(self.strongModWords, word) != -1):
                strongModCount = strongModCount + count.get(word)
            

        return [negCount, posCount, uncertCount, litCount, strongModCount, weakModCount, consCount]


    def getSentimentofChangeThread(self, count):

        numberOfwords = math.floor(len(count)/10)
        i = 0	
        chunk = []
        chunks = []
        for word in count:
            i = i+1
            if(numberOfwords % i == 0):
                chunks.append(chunk)
                chunk = []
                continue
            chunk.append(word)
            

        
        def search(words):
            consCount=0
            weakModCount=0
            strongModCount=0
            litCount=0
            uncertCount=0
            posCount=0
            negCount=0
            for word in words:
                if (self.binarySearchOnString(self.negWords, word) != -1):
                    negCount = negCount + count.get(word)
                elif (self.binarySearchOnString(self.posWords, word) != -1):
                    posCount = posCount + count.get(word)
                elif (self.binarySearchOnString(self.uncertWords, word) != -1):
                    uncertCount = uncertCount + count.get(word)
                elif (self.binarySearchOnString(self.litWords, word) != -1):
                    litCount = litCount + count.get(word)
                elif (self.binarySearchOnString(self.consWords, word) != -1):
                    consCount = consCount + count.get(word)
                elif (self.binarySearchOnString(self.weakModWords, word) != -1):
                    weakModCount = weakModCount + count.get(word)
                elif (self.binarySearchOnString(self.strongModWords, word) != -1):
                    strongModCount = strongModCount + count.get(word)
            return [negCount, posCount, uncertCount, litCount, strongModCount, weakModCount, consCount]

        ts = []
        for i in range(len(chunks)):
            t = ReturningThread(target=search, args=(chunks[i],))
            ts.append(t)
            t.start()
        results = []
        for t in ts:
            results.append(t.join())
        total = [0,0,0,0,0,0,0]
        for item in results:
            sum = []
            zip_object = zip(total, item)
            for list1_i, list2_i in zip_object:
                sum.append(list1_i+list2_i)
            total = sum

        return total

def sentiment_Analyzer(entries, sentimentChanges, SENTIMENT_ANALYSER, PICKLE_DIR):
    for headings in entries:
        counts = []
        sentimentCounts = []
        lastWordCount= None
        
        #Counts sentiment of words for each document
        for entry in headings[2]:
            with open(PICKLE_DIR + '\\' + "preProccess_" + entry, 'rb') as f:
                words = pickle.load(f) 

            #MapReduce the words to quickly compare sentiment change between chronological documents
            #i.e. this quarters Item 2 section against last quarters Item 2 Section
            count = src.utils.mapreduce(words)
            wordCount = len(count)
            if(len(counts) == 0): 
                lastWordCount = wordCount

            counts.append([entry, count])

            #Gets overall sentiment of the document
            sentimentCount = SENTIMENT_ANALYSER.getSentimentofChangeThread(count) 
            sentimentCounts.append([entry, sentimentCount, wordCount, lastWordCount])
            lastWordCount = wordCount
        lastEntry = None
        

        #Measure difference of sentiment between chronological documents
        for entry in sentimentCounts:
            difference = []
            if lastEntry == None:
                lastEntry = entry

            zip_object = zip(entry[1], lastEntry[1])
            for list1_i, list2_i in zip_object:
                difference.append(list1_i-list2_i)

            lastEntry = entry
            date = src.utils.getEntryDate(entry[0])
            form = src.utils.getEntryForm(entry[0])
            item = src.utils.getEntryItem(entry[0])

            sentimentChanges.append([ date , form, item, entry[1], difference, entry[2], entry[3]])

    return sentimentChanges