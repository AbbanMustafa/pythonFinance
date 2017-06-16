import numpy as np
import pandas as pd 
import pickle
from collections import Counter

from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier


def processData(ticker):
	numDays = 7#days into the future
	df = pd.read_csv('sp500CombinedClosed.csv', index_col = 0)
	tickers = df.columns.values.tolist()
	df.fillna(0, inplace=True)

	for i in range(1, numDays+1):

		df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]

	df.fillna(0, inplace=True)
	return tickers, df


def buySellHold(*args):
	cols = [c for c in args]
	requirement = .025 #if stock price increases by 2 percent - buy

	for col in cols:
		if col > requirement:
			return 1
		if col < -requirement:
			return -1
	return 0

def extractFeatureSets(ticker):
	tickers, df = processData(ticker)

	df['{}_target'.format(ticker)] = list(map(buySellHold, df['{}_1d'.format(ticker)],df['{}_2d'.format(ticker)],df['{}_3d'.format(ticker)],df['{}_4d'.format(ticker)],df['{}_5d'.format(ticker)],df['{}_6d'.format(ticker)],df['{}_7d'.format(ticker)]))


	vals = df['{}_target'.format(ticker)].values.tolist()
	str_vals = [str(i) for i in vals]
	print('Data spread', Counter(str_vals))

	df.fillna(0, inplace=True)

	df = df.replace([np.inf, -np.inf], np.nan)
	df.dropna(inplace=True)

	df_vals = df[[ticker for ticker in tickers]].pct_change() #normalized
	df_vals = df_vals.replace([np.inf, -np.inf], 0)
	df_vals.fillna(0, inplace=True)


	featSet = df_vals.values
	label = df['{}_target'.format(ticker)].values

	return featSet, label, df #returning feature sets, labels and dataframe for future reference

#extractFeatureSets('XOM')


def mLearning(ticker):
	x, y, df = extractFeatureSets(ticker)

	x_train, x_test, y_train, y_test = cross_validation.train_test_split(x,y,test_size=.25)

	#clf = neighbors.KNeighborsClassifier()
	clf = VotingClassifier([('lsvc', svm.LinearSVC()),
							('knn', neighbors.KNeighborsClassifier()),
							('rfor', RandomForestClassifier() )])

	clf.fit(x_train, y_train)
	confidence = clf.score(x_test, y_test)
	
	print('Accuracy', confidence)
	predictions = clf.predict(x_test)
	print('Predicted spread:', Counter(predictions))
	print()
	return confidence


print("AAPL")
mLearning('AAPL')



