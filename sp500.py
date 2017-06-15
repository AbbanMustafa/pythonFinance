import bs4 as bs
import pickle
import requests
import os
import datetime as dt 
import pandas as pd 
import pandas_datareader.data as web
import time

def saveSP500_tickers():
	resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup = bs.BeautifulSoup(resp.text,"html.parser")

	table = soup.find('table', {'class':'wikitable sortable'})
	tickers = []
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[0].text # gets the ticker

		mapping = str.maketrans(".","-")
		ticker = ticker.translate(mapping)

		tickers.append(ticker)

	with open("sp500.pickle","wb") as f:
		pickle.dump(tickers, f)

	print(tickers)

	return tickers

#saveSP500_tickers()

def getGoogleData(reload_sp500=False):
	if reload_sp500:
		tickers = saveSP500_tickers()
	else:
		with open("sp500.pickle","rb") as f:
			tickers = pickle.load(f)

	if not os.path.exists('stock_dfs'):
		os.makedirs('stock_dfs')

	start = dt.datetime(2000,1,1)
	end = dt.datetime(2016,12,31)

	for ticker in tickers[285:]:
		print(ticker)

		if not os.path.exists('stocks_dfs/{}.csv'.format(ticker)):
			df = web.DataReader(ticker, 'google', start, end)
			df.to_csv('stock_dfs/{}.csv'.format(ticker))
		else:
			print('Already have {}'.format(ticker))

		print ("Sleeping....")
		time.sleep(2)


getGoogleData()

