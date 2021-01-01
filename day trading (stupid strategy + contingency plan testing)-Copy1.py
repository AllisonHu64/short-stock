#!/usr/bin/env python
# coding: utf-8

# In[1]:


# tools for all the running delta
# import all the resource
import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
import requests
from datetime import datetime as dt
import datetime
import yfinance as yf
import time
import urllib.request


# In[2]:


# run the strategy on baidu's stock prices from 2005/12/30 to 2020/01/15
# the sequence Open High Low Close

folder_path = '/Users/allison/Desktop/BIDU/'


# In[3]:


start = datetime.datetime(2005, 12, 30)
end = datetime.datetime(2020, 1, 15)


# In[4]:


date_series = pd.date_range(start = start, end = end, freq = '1D')


# In[5]:


stock_price_mean_df = pd.DataFrame(columns = ['baidu'] , index = date_series)


# In[6]:


datetime.datetime(2020,12,25,0,0,tzinfo=datetime.timezone.utc)


# In[ ]:


for date in date_series:
    file_name = date.strftime("%Y%m%d") + '.csv'
    file_path = folder_path + file_name
    try:
        stock_price_df = pd.read_csv(file_path,header=None,names = ['Datetime','Open','High','Low','Close','unknown1','unknown2','unknown3','unknown4'])
    except FileNotFoundError:
        print('the market is closed on ', date.strftime('%Y-%m-%d'))
        continue
        
    print('calculating mean stock price. stock : ', 'baidu', ' date: ', date.strftime('%Y-%m-%d'))
    stock_price_df['Mean'] = (stock_price_df['High']/2 + stock_price_df['Low']/2)
    stock_price_mean_df.loc[date,"baidu"] = stock_price_df['Mean'].mean()
        
    


# In[29]:


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
  


# In[30]:


# calculating the return rate
return_rate_df = pd.DataFrame(columns = ['baidu'],index = date_series)

buy_price = 0
sale_price = 0
asset = 100
buy_mode = 0
for date in date_series:
    # check if file exists
    file_name = date.strftime("%Y%m%d") + '.csv'
    file_path = folder_path + file_name
    try:
        stock_price_df = pd.read_csv(file_path,header=None,names = ['Datetime','Open','High','Low','Close','unknown1','unknown2','unknown3','unknown4'])
    except FileNotFoundError:
        print('the market is closed on ', date.strftime('%Y-%m-%d'))
        continue
    
    # check if market opens
    if (len(stock_price_df) == 0):
        print('market is not open on ', date.strftime("%Y-%m-%d"))
    else:
        cur_mean = cal_mean_days(date, stock_price_mean_df['baidu'], 5)
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

            return_rate_df.loc[date,'baidu'] = asset
    


# In[25]:


# the return rate of the stupid strategy is 852% from 2005 to 2020
# the stupid strategy doesn't do well if the stock prices continues to decrease or continues to increase
# next step:
# 1. add a contingency plan, maybe abort if we lose 5% today 
# return_rate_df


# In[6]:


# calculating the return rate
return_rate_df = pd.DataFrame(columns = ['baidu'],index = date_series)

buy_price = 0
sale_price = 0
asset = 100
buy_mode = 0
for date in date_series:
    # check if file exists
    file_name = date.strftime("%Y%m%d") + '.csv'
    file_path = folder_path + file_name
    try:
        stock_price_df = pd.read_csv(file_path,header=None,names = ['Datetime','Open','High','Low','Close','unknown1','unknown2','unknown3','unknown4'])
    except FileNotFoundError:
        print('the market is closed on ', date.strftime('%Y-%m-%d'))
        continue
    
    # check if market opens
    if (len(stock_price_df) == 0):
        print('market is not open on ', date.strftime("%Y-%m-%d"))
    else:
        cur_mean = cal_mean_days(date, stock_price_mean_df['baidu'], 5)
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
                elif (buy_mode == 1 and stock_price_df['High'][i] < 0.95 * buy_price):
                    print("activate contingency plan, stop trading for the day")
                    buy_mode = 0
                    sale_price = stock_price_df['High'][i]
                    asset = asset * sale_price / buy_price
                    print("buy at ",buy_price,", sale at ",sale_price)
                    continue

            return_rate_df.loc[date,'baidu'] = asset
    


# In[50]:


# the return rate of the stupid strategy is 2339.74% from 2005 to 2020
# The contingency plan works
# next step:
# 1. look at other indicators
# return_rate_df

