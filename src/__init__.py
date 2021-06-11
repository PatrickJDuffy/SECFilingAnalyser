import os
from src.main import main, SentimentAnalysis

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

#Create temp files path if it doesnt exist
if not os.path.exists(str(ROOT_DIR) + '\\temp_Filesx'):
    os.makedirs(str(ROOT_DIR) + '\\temp_Filesx')

