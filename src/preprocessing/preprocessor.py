from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import gensim 
from gensim.models import Word2Vec 

def preProcess_text(text, tokenize_words = True, remove_stopwords = True, 
                    stemming = True):

    if stemming:
        lemmatizer = WordNetLemmatizer()
        lemmatizer.lemmatize(text)

    if tokenize_words:
        #print('Tokenising text...')
        words = word_tokenize(text)

    if remove_stopwords:
        #print('Removing stopwords...')
        stop_words = stopwords.words('english')
        words = [word for word in words if word not in stop_words]
    
    # if stemming:
    #     print('Stemming words...')
    #     porter = PorterStemmer()
    #     words = [porter.stem(word) for word in words]
    

    #print('Text preprocessing complete...')
    return words
    

def pos_text(text):
    #print('Tagging parts of speech...')
    words = word_tokenize(text)
    pos = pos_tag(words)
    return pos


def word2Vec(tokenizedText):
    # Create CBOW model 
    model1 = gensim.models.Word2Vec(tokenizedText, min_count = 1,  
                              size = 100, window = 5)   