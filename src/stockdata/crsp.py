import yfinance as yf
import datetime


class Stock:

    def __init__(self, ticker):
        self.stock = yf.Ticker(ticker)
        self.history = yf.Ticker(ticker).history(period='max')

    def getStockPriceByPeriod(self, start, end):
        return self.history['Close'][start:end]

    def getStockPriceByDate(self, qDate, count = 0): 
        date = qDate.split("/")
        date = datetime.date(int(date[0]),int(date[1]),int(date[2]))
        date = date + datetime.timedelta(days=[0, 0, 0, 0, 0, 2, 1][date.weekday()])
        diff = 1
        today = date.today()
        price = None
        if(count > 20):
            return -1
        try:
            strDate = date.strftime("%Y/%m/%d")
            price = self.history['Close'][strDate]
        except:
            if(date > today or diff == -1):
                print("Reveresed search")
                date = date + datetime.timedelta(days=diff)
                strDate = date.strftime("%Y/%m/%d")
                price = self.getStockPriceByDate(strDate, count+1)

            date = date + datetime.timedelta(days=diff)
            strDate = date.strftime("%Y/%m/%d")
            price = self.getStockPriceByDate(strDate, count+1)

        return price

    def getPriceDifference(self, start, end):
        ret = []
        if(len(end) == 0):
            return
        period = self.getStockPriceByPeriod(start, end[0])
        ret.append(period[len(period) - 1] - period[0])

        period = self.getStockPriceByPeriod(start, end[len(end)-1])
        ret.append(period[len(period) - 1] - period[0])

        #[diffLastYear, diffLastQuarter]
        return ret

    def financials(self):
        print(self.stock.get_earnings())
