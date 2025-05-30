import yfinance
import pandas
import sqlite3
import json
import numpy
import matplotlib
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

def main():
    dow_data = json.load(open("DOW.json","r"))
    #msftticker = yfinance.Ticker(dow_data[0])
    #pprint(getstockhistory(msftticker))
    for ticker in dow_data:
        stock = yfinance.Ticker(ticker)
        historicaldata = (getstockhistory(stock))
        stddev = calcstddev(historicaldata)
        gmean = calcgmean(historicaldata)
        print("Symbol: ", stock.info.get("symbol"), " StandardDev: ", stddev,"Geo Mean: ", gmean)

if __name__ == "__main__":
    main()
