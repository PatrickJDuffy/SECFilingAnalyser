import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

class Stock:

    def __init__(self, ticker):
        self.stock = yf.Ticker(ticker)
        self.history = yf.Ticker(ticker).history(period='max')
        print('Check')

    def getStockPriceByPeriod(self, start, end):
        return self.history['Close'][start:end]
    


    def getStockPriceByDate(self, qDate): 
        return self.history['Close'][qDate]


stock = Stock('TSLA')


stock.getStockPriceByPeriod('2020-1-2', '2020-3-1')
print(stock.getStockPriceByDate('2020-1-2'))
