
def createDataset(sentimentChanges, dates, ticker, stock, ROOT_DIR):
    prices = []
    
    for i in range(len(dates)):
        nextDates = []
        left = len(dates) -1 - i
        if (left < 4 ):
            for x in range(left):
                nextDates.append(dates[i+x][0])     
        else:
            nextDates.append(dates[i+1][0])
            nextDates.append(dates[i+2][0])
            nextDates.append(dates[i+3][0])
            nextDates.append(dates[i+4][0])

        price = stock.getStockPriceByDate(dates[i][0])


        if (price == -1):
            print("Unable to fetch stock Price")
            with open(str(ROOT_DIR)+ '\\temp_Filesx\\finComps.txt', "+a") as f:
                f.write(ticker + "*****\n")
            return

        try:
            diff = stock.getPriceDifference(dates[i][0], nextDates)
            prices.append([dates[i][0], price, diff[0], diff[1]])
        except:
            prices.append([dates[i][0], price, 0, 0])

    
    for date in dates:
        for price in prices:
            if price[0] == date[0]:
                date.append([price[1], price[2], price[3]])

        for entry in sentimentChanges:
            if(entry[0] == date[0]):
                try:
                    date[1].append([entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7]])
                    continue
                except:
                    continue

    return dates