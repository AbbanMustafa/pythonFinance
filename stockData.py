import datetime as dt #in order to work with dates
import matplotlib.pyplot as plt #in order to create graphs and visualize data
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web


style.use('ggplot')

# start = dt.datetime(2000,1,1)
# end = dt.datetime(2016,12,31)

# df = web.DataReader("NASDAQ:TSLA", 'google', start, end) #data frame

# df.to_csv('tsla.csv') #create an excel sheet

df = pd.read_csv('tsla.csv', parse_dates = True, index_col=0) #read from the xcel sheet
# print(df.head())

# print(df[['Open','High']].head())

# df['Close'].plot()
# plt.show()

# df['100ma'] = df['Close'].rolling(window=100, min_periods=0).mean() #The first 100 data points will have Nan so use min_periods param

df_ohlc = df['Close'].resample('10D').ohlc() #open high low close is being resampled by 10 days
df_volume = df['Volume'].resample('10D').sum()


#Need to get all the values from the dateframe including the column headers and the index
df_ohlc.reset_index(inplace=True)

df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num) # Mapping dates to mdates

ax1 = plt.subplot2grid((6,1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan = 1, colspan = 1, sharex=ax1) #Sharex allows you to zoom in on both
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
# ax1.plot(df.index, df['Close'])
# ax1.plot(df.index, df['100ma'])
# ax2.bar(df.index, df['Volume'])

plt.show()
