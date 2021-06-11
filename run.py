import src
from pathlib import Path
#from threading import *
import os


print('Loading Project...')
src.__loader__
 
print('Starting Project')   


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
path = 'src\\SEC_EDGAR_text\\output_files_examples\\batch_0073\\001\\'
companiesDir = Path(os.path.join(ROOT_DIR, path))



for company in companiesDir.iterdir():
    dir = path + "\\" + company.name
    ticker = company.name.split("_")[0] 
    src.main(ticker, dir) 

  