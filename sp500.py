import bs4 as bs
import pickle
import requests
import os
import datetime as dt 
import pandas as pd 
import pandas_datareader.data as web
import time
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

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

	for ticker in tickers:
		print(ticker)
		try:
			if not os.path.exists('stocks_dfs/{}.csv'.format(ticker)):
				df = web.DataReader(ticker, 'google', start, end)
				df.to_csv('stock_dfs/{}.csv'.format(ticker))
			else:
				print('Already have {}'.format(ticker))
		except:
			df = web.DataReader('NYSE:'+ticker, 'google', start, end)
			df.to_csv('stock_dfs/{}.csv'.format(ticker))
		
		#print ("Sleeping....")
		#time.sleep(2)


#getGoogleData()

#combining adjusted close for all data frames
def compile_data():
	with open("sp500.pickle","rb") as f:
		tickers = pickle.load(f)

	main_dataframe = pd.DataFrame()

	for count,ticker in enumerate(tickers):
		df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
		df.set_index('Date', inplace = True)

		df.rename(columns = {'Close': ticker}, inplace=True)
		df.drop(['Open','High','Low','Volume'], 1, inplace=True)

		if main_dataframe.empty:
			main_dataframe = df
		else:
			main_dataframe = main_dataframe.join(df, how ='outer')

		if count % 10 == 0:
			print(count)

	print(main_dataframe.head())
	main_dataframe.to_csv('sp500CombinedClosed.csv')

#compile_data()

def visualizeData():
	df = pd.read_csv('sp500CombinedClosed.csv')
	# df['AAPL'].plot()
	# plt.show()
	dfCorr = df.corr() #generate the correlation values

	print(dfCorr.head())
	data = dfCorr.values
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)

	heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
	fig.colorbar(heatmap)
	ax.set_xticks(np.arange(data.shape[0])+.5, minor = False)
	ax.set_yticks(np.arange(data.shape[1])+.5, minor = False)

	ax.invert_yaxis()
	ax.xaxis.tick_top()

	column_labels = dfCorr.columns
	row_labels = dfCorr.index

	ax.set_xticklabels(column_labels)
	ax.set_yticklabels(row_labels)
	plt.xticks(rotation=90)
	heatmap.set_clim(-1,1)

	plt.tight_layout
	plt.show()

visualizeData()


