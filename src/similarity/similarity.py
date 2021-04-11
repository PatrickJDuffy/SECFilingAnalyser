from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
import difflib
import pandas as pd
import numpy as np

def cos_Similarity(d1, d2, input_type = 'filename', max_features_val = 500):
    vectorizer = TfidfVectorizer(input = input_type, max_features = max_features_val)  
    countvectorizer = CountVectorizer(analyzer= 'word')
    tfidf = vectorizer.fit_transform([d1, d2])
    
    feature_array = np.array(vectorizer.get_feature_names())
    tfidf_sorting = np.argsort(tfidf.toarray()).flatten()[::-1]

    n = 3
    top_n = feature_array[tfidf_sorting][:n]
    # for line in difflib.unified_diff(d1, d2, fromfile='file1', tofile='file2', lineterm=''):
    #     print (line) 

    #print (top_n)
    count_wm = countvectorizer.fit_transform([d1, d2])
    #count_tokens = countvectorizer.get_feature_names()
    tfidf_tokens = vectorizer.get_feature_names()
    
    #df_countvect = pd.DataFrame(data = count_wm.toarray(),columns = count_tokens)
    df_tfidfvect = pd.DataFrame(data = tfidf.toarray(),columns = tfidf_tokens)
    df_tfidfvect.sort_values(by=1 ,axis = 1)
    
    #print("Count Vectorizer\n")
    #print(df_countvect)
    #print("\nTD-IDF Vectorizer\n")
    #print(df_tfidfvect)
    return ((tfidf * tfidf.T).A)


