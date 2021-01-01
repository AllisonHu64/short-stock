#!/usr/bin/env python
# coding: utf-8

# In[1]:


# tools for all the running delta
# import all the resource
import pandas as pd
import numpy as np
import requests
from datetime import datetime as dt
import datetime
import yfinance as yf
import time
import urllib.request
import os


# In[2]:


os.environ['TZ'] = 'America/st.johns'


# In[3]:


# stocks from https://www.thebalance.com/most-popular-stocks-and-etfs-for-day-trading-1031371#:~:text=Most%20Popular%20Stocks%20and%20ETFs,sizes%20adapted%20to%20the%20volatility.
stock_list = ['xlf','qqq','vxx','fxi','ewz','efa','eem','sqqq','spy','gdx','spy','gdx','amd']


# In[4]:


today = datetime.date.today()
today = datetime.datetime(today.year,today.month,today.day)


# In[13]:


date_series = pd.date_range(start = today - datetime.timedelta(days = 30), end = today, freq = '1D')


# In[ ]:


for stock in stock_list:
    for date in date_series:
        
        stock_price = yf.download( 
            tickers = stock,
            interval = "1m",
            end = date,
            start = date - datetime.timedelta(days=1)
            )
        file_name = 'yahoo_stock_prices/' + date.strftime("%Y-%m-%d") + ' ' + stock + '.csv'
        stock_price.to_csv(file_name)
        print('saving stock prices to local : ', file_name)


# In[16]:


# calculate the mean stock prices 
stock_price_mean_df = pd.DataFrame(columns = stock_list, index = date_series)


# In[34]:


# calculate the mean stock prices 
for stock in stock_list:
    for date in date_series:
        file_name = 'yahoo_stock_prices/' + date.strftime("%Y-%m-%d") + ' ' + stock + '.csv'
        #file_name = date.strftime("%Y-%m-%d") + ' ' + stock + '.csv'
        try:
            stock_price_df = pd.read_csv(file_name)
        except:
            print('filename: ', file_name,' file not found' )
            continue
        
        if (len(stock_price_df) == 0):
            print('market is not open on ', date.strftime("%Y-%m-%d"))
        else:
            print('calculating mean stock price. stock : ', stock, " date: ", date.strftime("%Y-%m-%d"))
            stock_price_df['Mean'] = (stock_price_df['High']/2 + stock_price_df['Low']/2)
            stock_price_mean_df.loc[date,stock] = stock_price_df['Mean'].mean()


# In[43]:


'''
@param: date
@param: stock_mean_df
@param: k
@return: np.nan if k is not a positive interger
         else: returns the mean of k valid stock prices before date

'''
def cal_mean_days(date, stock_prices_df, k):
    if k <= 0 or not isinstance(k,int):
        return np.nan
    
    total_price = 0
    days = 0
    cur_date = date - datetime.timedelta(days=1)
    while (days != k):
        try:
            cur_price = stock_prices_df[cur_date]
        except:
            #print("index is out of range")
            return np.nan
            
        if (not np.isnan(cur_price)):
            total_price += cur_price
            days += 1
            
        cur_date = cur_date - datetime.timedelta(days=1)
    return total_price/k
    


# In[47]:


# calculating the return rate
return_rate_df = pd.DataFrame(columns = stock_list,index = [0])
for stock in stock_list:
    buy_price = 0
    sale_price = 0
    asset = 100
    buy_mode = 0
    for date in date_series:
        # check if file exists
        file_name = 'yahoo_stock_prices/' + date.strftime("%Y-%m-%d") + ' ' + stock + '.csv'
        #file_name = date.strftime("%Y-%m-%d") + ' ' + stock + '.csv'
        try:
            stock_price_df = pd.read_csv(file_name)
        except:
            print('filename: ', file_name,' file not found' )
            continue
    
        # check if market opens
        if (len(stock_price_df) == 0):
            print('market is not open on ', date.strftime("%Y-%m-%d"))
        else:
            cur_mean = cal_mean_days(date, stock_price_mean_df[stock], 5)
            if (not np.isnan(cur_mean)):
                print('trading on date :', date.strftime("%Y-%m-%d"))
                for i in range(0, len(stock_price_df)):
                    if (buy_mode == 0 and stock_price_df['Low'][i] < 0.99 * cur_mean):
                        buy_mode = 1
                        buy_price = stock_price_df['Low'][i]
                    elif (buy_mode == 1 and stock_price_df['High'][i] > 1.01 * cur_mean):
                        buy_mode = 0
                        sale_price = stock_price_df['High'][i]
                        asset = asset * sale_price / buy_price
                        print("buy at ",buy_price,", sale at ",sale_price)
    
    return_rate_df.loc[0,stock] = asset
    


# In[ ]:


return_rate_df


# In[ ]:


# the return rate is about 3% for 15 days of trading which is too high
# 1. we buy and sell at the max and min 
# 2. the stock market is werid during covid


# In[ ]:


# next step:
# 1. calculate return rate to some more data
# 2. try using other indicators: EMA, MACD, RSI

