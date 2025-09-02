import yfinance
import pandas
import json
import numpy
import matplotlib.pyplot as plot
import statistics
from pprint import pprint

#hardcoded gets stock history from 2006-01-01 to present 2025-01-01
#takes a Ticker datatype as input
def getstockhistory(stock):
    return stock.history(start="2006-01-01",end="2025-01-01")

def calcstddev(stockhistory):
    return numpy.std(stockhistory["Open"],ddof=1)

def calcgmean(stockhistory):
    return statistics.geometric_mean(stockhistory["Open"])

def calcexpectedreturn(stockhistory):
    #calculate daily return
    stockhistory['Return']=stockhistory['Close'].pct_change()
    #calculate average daily return
    expectedreturn_daily = stockhistory['Return'].mean()
    #convert to yearly assuming 252 trading days
    expectedreturn_yearly = expectedreturn_daily *252
    return expectedreturn_yearly

def calcsharperatio(standarddev, expectedreturn):
    return expectedreturn/standarddev

def main():
    dow_data = json.load(open("DOW.json","r"))
    #msftticker = yfinance.Ticker(dow_data[0])
    #s = getstockhistory(msftticker)
    #print(calcexpectedreturn(s)) 
    stock_data = []
    for ticker in dow_data:
        stock=yfinance.Ticker(ticker)
        stock_hist = getstockhistory(stock)
        stddev = calcstddev(stock_hist)
        exprtn = calcexpectedreturn(stock_hist)
        sharperatio = float(calcsharperatio(stddev,exprtn))
        stock_data.append([ticker,sharperatio])
    print("Stocks in order of how efficient they are")
    stock_data.sort(key=lambda x: x[1], reverse=True)
    pprint(stock_data)
    stddevs = []
    expectedreturns = []
    for ticker in dow_data:
        stock = yfinance.Ticker(ticker)
        historicaldata = (getstockhistory(stock))
        stddev = calcstddev(historicaldata)
        stddevs.append(stddev)
        expectedreturn = calcexpectedreturn(historicaldata)
        expectedreturns.append(expectedreturn)
        sharperatio = calcsharperatio(stddev, expectedreturn)
        print("Symbol: ", stock.info.get("symbol"), " StandardDev: ", stddev,"Expected Return: ", expectedreturn," Sharpe Ratio: ", sharperatio)
    plot.scatter(stddevs, expectedreturns)
    plot.ylabel("Expected Return")
    plot.xlabel("Standard Deviation")
    for i, ticker in enumerate(dow_data):
        plot.annotate(ticker, (stddevs[i],expectedreturns[i]))
    plot.show()

if __name__ == "__main__":
    main()
