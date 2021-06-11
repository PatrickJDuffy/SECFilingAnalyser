from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import gensim 
import src.utils
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
    

    return words
    
            
        