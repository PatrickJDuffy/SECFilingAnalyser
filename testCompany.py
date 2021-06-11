
from src.utils import getCikNumber, getCompanyDataset

# storage = ''
# report_period = 'all'
# filings = '10-K, 10-Q'
# start = '20150101'
# end = '20200101'
# multiprocessing_cores = 3

ticker = 'msft'
company = getCikNumber(ticker.upper())
data = getCompanyDataset(ticker)

if(data != -1):
    #Import model and plug in values
    print()
