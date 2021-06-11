import re
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from html import unescape

"""Parses, cleans and returns the text"""


def clean_text(text, rem_ellipses=True, tokenize_words = True, remove_stopwords = True,
                conv_lcase=True, expand_abbrev=True, stemming = True,
                rem_punc=True, repl_nonprint_chars=True, rem_wspace=True):

    # Remove ellipsis i.e. "..."
    if rem_ellipses:
        text = re.sub(r"\.{2,}", " ", text)


    # Removes non printable characters e.g. UTF-8 BOM characters
    if repl_nonprint_chars:
        text = re.sub(r"[^" + string.printable + "]", "", text)

    # Converts to lower case
    if conv_lcase:
        text = text.lower()

    # Expands abbreviations
    if expand_abbrev:
        abbrevs = {"can't": "can not", "won't": "will not", "n't": " not",
                   "'ve": " have", "'re": " are", " it's": " it is",
                   "i'm": "i am", " he's": " he is", " she's": " she is",
                   "'ll": " will", "'d": " would", "&": " and ",
                   "%": " percent", "'s": " "}
        for abr, exp in abbrevs.items():
            text = re.sub(r"" + abr, exp, text)

    # Removes punctuation
    if rem_punc:
        text = re.sub(r"[" + string.punctuation + "]", " ", text)


    # Removes whitespace
    if rem_wspace:
        text = re.sub(r"(\s{2,})|(\t+)|(\n)", " ", text)
        text = re.sub(r"(^\s+)|(\s+$)", "", text)

    # if remove_stopwords:
    #     #print('Removing stopwords...')
    #     stop_words = stopwords.words('english')
    #     words = [word for word in text if word not in stop_words]

    return text

