#!/usr/bin/env python
# coding: utf-8

# In[11]:


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


# In[2]:


# stocks from https://www.thebalance.com/most-popular-stocks-and-etfs-for-day-trading-1031371#:~:text=Most%20Popular%20Stocks%20and%20ETFs,sizes%20adapted%20to%20the%20volatility.
stock_list = ['xlf','qqq','vxx','fxi','ewz','efa','eem','sqqq','spy','gdx','spy','gdx','amd']


# In[3]:


# a dictionary to store the mean value
stock_mean_dict = {}


# In[4]:


for stock in stock_list:
    ticker = yf.Ticker(stock)
    try:
        stock_price_df = ticker.history(period = '5d', interval = '15m')
    except:
        print('There is an error with connection')
        continue
    # mean is calculated using open and close
    stock_mean = (stock_price_df['Open'].mean() + stock_price_df['Close'].mean())/2
    print("calculating mean stock price for ", stock)
    print(stock_mean)
    stock_mean_dict[stock] = stock_mean
    
    


# In[50]:


# real time data： http://hq.sinajs.cn/list=gb_[symbol]
# There might be a lag
url_link = 'http://hq.sinajs.cn/list=gb_'
for stock in stock_list:
    # get the cur_price for this stock
    try:
        cur_price = requests.get(url_link + stock).text
    except:
        print('There is an error with connection')
        continue
    cur_price = cur_price.split(',')[1]
    
    if float(cur_price) > 1.02 * stock_mean_dict[stock]:
        print('this is a good time to sell ', stock)
    elif float(cur_price) < 0.99 * stock_mean_dict[stock]:
        print('this is a good time to buy ', stock)
    


# In[ ]:


# next step:
# check the return rate for this strategy
# it is slow to use yfinance outside canada


# In[51]:


stock_prices_dict = {}


# In[ ]:


# verify against yesterday's data
# get yesterday's stock price
for stock in stock_list:
    ticker = yf.Ticker(stock)
    try:
        stock_price_df = ticker.history(period = '2d', interval = '1m')
    except:
        print('There is an error with connection')
        continue
    print(stock)
    stock_prices_dict[stock] = stock_price_df
    


# In[65]:


stock_prices_dict['qqq'].reset_index()
buy_price = 0
sale_price = 0
buy_mode = 0
revenue = 0
asset = 100
for i in range(0,82):
    if buy_mode == 0 and stock_prices_dict['qqq']['Low'][i] < 0.99 * stock_mean_dict['qqq']:
        buy_mode = 1
        buy_price = stock_prices_dict['qqq']['Low'][i]
    elif buy_mode == 1 and stock_prices_dict['qqq']['High'][i] > 1.02 * stock_mean_dict['qqq']:
        buy_mode = 0
        sale_price = stock_prices_dict['qqq']['High'][i]
        asset = asset * sale_price / buy_price
        print('--buy at: price:%.2f high:%.2f'%(buy_price,sale_price))


# In[ ]:





# In[ ]:




