#from src.main import main
import src
from pathlib import Path
from src.utils import checkSymbol
from threading import *
import concurrent.futures
import os
import pickle

dataPreprocessThreading = False
dataPreprocess = False
getValidCIKTicker = True
cleanData = False
shuffleCikFile = False
threads = []
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

print('Loading Package...')
src.__loader__

cikPath = os.path.join(str(ROOT_DIR), 'src\\SEC_EDGAR_text\\cik_tickersx1.txt')
secEdgarTextPath = os.path.join(str(ROOT_DIR), 'src\\SEC_EDGAR_text\\')


'''Iterates through the folder of downloaded companies and processes/cleans the data'''

if dataPreprocess:
    print('Starting Data Preprocessing')
    batch = 2000
    while batch < 2133:
        path = 'src\\SEC_EDGAR_text\\output_files_examples\\batch_' + \
            str(batch) + '\\001\\'
        try:
            companiesDir = Path(os.path.join(ROOT_DIR, path))

            for company in companiesDir.iterdir():
                dir = path + "\\" + company.name
                ticker = company.name.split("_")[0]
                src.main(ticker, dir)
            batch += 1
        except:
            batch += 1

def initiateThread(args, jobsLeft):
    print(jobsLeft)
    src.main(args[0], args[1])

if dataPreprocessThreading:
    print('Starting Data Preprocessing')
    noOfThreads = 10
    batch = 2100
    jobs = []

    while batch < 2134:

        path = 'src\\SEC_EDGAR_text\\output_files_examples\\batch_' + \
            str(batch) + '\\001\\'
        try:
            companiesDir = Path(os.path.join(ROOT_DIR, path))

            for company in companiesDir.iterdir():
                dir = path + company.name
                ticker = company.name.split("_")[0]
                jobs.append([ticker, dir])
            batch += 1
        except:
            batch += 1

    print(jobs.pop())
    with concurrent.futures.ThreadPoolExecutor(max_workers=noOfThreads) as executor:
        while len(jobs) > 0:
            print('check')
            executor.submit(initiateThread, jobs.pop(), len(jobs))



''' Checks for valid tickers from the list of publicly trading companies from the SEC
        Checks If they are downloaded already, 
        and if there is stock data available for them with the yahoo finance package'''

if getValidCIKTicker:
    TEMP_FILE_DIR = Path(os.path.join(str(ROOT_DIR), 'src\\temp_filesx\\'))
    
    path = 'src\\SEC_EDGAR_text\\output_files_examples\\'
    outputDir = Path(os.path.join(ROOT_DIR, path))
    downloaded = []
    for batch in outputDir.iterdir():
        try:
            
            dir = Path(os.path.join(outputDir, batch.name + "\\001\\"))
            print(dir)
            for company in dir.iterdir():
                #print(company.absolute())
                split = company.name.split('_')
                tickerCIK = split[0] + '_' + split[1]
                downloaded.append(tickerCIK)
                #print('Added ',tickerCIK, ' to downloaded companies' )
        except:
            #print('Unable to acquire downloaded batch information')
            continue
    
    processed = []
    for company in TEMP_FILE_DIR.iterdir():
        processed.append(company.name)


    with open(os.path.join(str(ROOT_DIR), 'src\\SEC_EDGAR_text\\cik_tickersx.txt'), 'r') as f:
        companies = f.readlines()

    # # Gets list of previously processed tickers
    # try:
    #     with open(os.path.join(str(ROOT_DIR), 'src\\SEC_EDGAR_text\\cik_tickersx.txt'), 'r') as f:
    #         processed = f.readlines()
    # except:
    #     processed = []

    # Gets list of previously processed and unfit tickers
    try:
        with open(os.path.join(str(ROOT_DIR), 'src\\SEC_EDGAR_text\\broken_tickers.txt'), 'r') as f:
            broken = f.readlines()
    except:
        broken = []

    #downloadable = []
    for line in companies:
        if '#' in line:
            continue

        temp = line.split('\n')[0]
        ticker = temp.split("\t")[1]
        if line not in downloaded and line not in broken:
            if ticker not in processed and checkSymbol(ticker):
                with open(os.path.join(str(ROOT_DIR), 'src\\SEC_EDGAR_text\\cik_tickersx2.txt'), '+a') as f:
                    f.write(line)
            else:
                with open(os.path.join(str(ROOT_DIR), 'src\\SEC_EDGAR_text\\broken_tickers2.txt'), '+a') as f:
                    f.write(line)


            


if shuffleCikFile:
    
    with open(cikPath, 'r') as f:
        ciks = f.readlines()
    import random

    random.shuffle(ciks)
    with open(cikPath, 'w') as f:
        f.writelines(ciks)


''' Make sub files for multiple SEC_Edgar_Text programs to run in parallel'''

def createSubFiles(file, dir_path, numOfFiles, numOfCompanies):
    with open(file, 'r') as f:
        companies = f.readlines()

    for i in range(numOfFiles):
        fPath = dir_path + 'companyList' + str(i) + '.txt'
        ciks = []
        companiesi = companies[i*numOfCompanies:(i+1)*numOfCompanies]
        for comp in companiesi:
            if '#' not in comp:
                ciks.append(comp)
        with open(fPath, '+a') as f:
            f.writelines(ciks)

#createSubFiles(cikPath, secEdgarTextPath, 15, 20)