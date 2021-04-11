import os
from src.main import main

print('__init__.py')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

#Create temp files path if it doesnt exist
if not os.path.exists(str(ROOT_DIR) + '\\temp_Files'):
    os.makedirs(str(ROOT_DIR) + '\\temp_Files')

#Create temp Folders path if they dont exist
if not os.path.exists(str(ROOT_DIR)+ '\\temp_Files\\clean_Files'):
    os.makedirs(str(ROOT_DIR)+ '\\temp_Files\\clean_Files')

if not os.path.exists(str(ROOT_DIR)+ '\\temp_Files\\preProcessed_Files'):
    os.makedirs(str(ROOT_DIR)+ '\\temp_Files\\preProcessed_Files')

if not os.path.exists(str(ROOT_DIR)+ '\\temp_Files\\csv_Ticker_Files'):
    os.makedirs(str(ROOT_DIR)+ '\\temp_Files\\csv_Ticker_Files')

