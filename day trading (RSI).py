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


stock_price_rsi_df = pd.DataFrame(columns = ['baidu'] , index = date_series)


# In[81]:


price_up= []
price_down = []
cur_avg_gain = np.nan
prev_price = np.nan
cur_avg_loss = np.nan
for date in date_series:
    file_name = date.strftime("%Y%m%d") + '.csv'
    file_path = folder_path + file_name
    try:
        stock_price_df = pd.read_csv(file_path,header=None,names = ['Datetime','Open','High','Low','Close','unknown1','unknown2','unknown3','unknown4'])
    except FileNotFoundError:
        print('the market is closed on ', date.strftime('%Y-%m-%d'))
        continue
        
    if (len(stock_price_df) > 0 and stock_price_df.iloc[-1,4] >=2):
        cur_rsi = np.nan
        cur_close_price = stock_price_df.iloc[-1,4]
        # calculate rsi
        if (len(price_up) >= 14):
            avg_gain = np.array(price_up[-15:-1]).mean()
            avg_loss = np.array(price_down[-15:-1]).mean()
            cur_rsi = 100 - 100 / (1 + avg_gain / avg_loss)
                
            
        # adding price up and price down for average gain and avg loss
        if (np.isnan(prev_price)):
            price_up.append(0)
            price_down.append(0)
        elif (cur_close_price > prev_price):
            price_up.append(cur_close_price - prev_price)
            price_down.append(0)
        elif (cur_close_price < prev_price):
            price_down.append(-cur_close_price + prev_price)
            price_up.append(0) 
                
        stock_price_rsi_df.loc[date,'baidu'] = cur_rsi       
        prev_price = cur_close_price
        
    print('calculating rsi stock price. stock : ', 'baidu', ' date: ', date.strftime('%Y-%m-%d'))
    #stock_price_mean_df.loc[date,"baidu"] = 
        
    


# In[24]:


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
        cur_rsi = stock_price_rsi_df.loc[date,'baidu']
        if (not np.isnan(cur_rsi) and len(stock_price_df) != 0):
            print('trading on date :', date.strftime("%Y-%m-%d"))
            
            if (buy_mode == 0 and cur_rsi < 30):
                buy_mode = 1
                buy_price = stock_price_df.iloc[-1,4]
            elif (buy_mode == 1 and cur_rsi > 70):
                buy_mode = 0
                sale_price = stock_price_df.iloc[-1,4]
                asset = asset * sale_price / buy_price
                print("buy at ",buy_price,", sale at ",sale_price)
                    

            return_rate_df.loc[date,'baidu'] = asset
    


# In[26]:


return_rate_df.fillna(method='pad')


# In[25]:


# the return rate of the stupid strategy is 229% from 2005 to 2020
# the strategy is not really good
# next step:
# 1. the interval is too big maybe try every 30 seconds 


# In[55]:


# calculating the return rate
#return_rate_df = pd.DataFrame(columns = ['baidu'],index = date_series)
return_rate_list = []

price_up= []
price_down = []
prev_price = np.nan

buy_price = 0
buy_time = ''
sale_price = 0
sale_time = ''
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
        for i in range(0,len(stock_price_df)):
            cur_rsi = np.nan
            cur_open_price = stock_price_df.iloc[i,1]
            # calculate rsi
            if (len(price_up) >= 14):
                avg_gain = np.array(price_up[-15:-1]).mean()
                avg_loss = np.array(price_down[-15:-1]).mean()
                cur_rsi = 100 - 100 / (1 + avg_gain / avg_loss)
                
            
            # adding price up and price down for average gain and avg loss
            if (np.isnan(prev_price)):
                price_up.append(0)
                price_down.append(0)
            elif (cur_open_price > prev_price):
                price_up.append(cur_open_price - prev_price)
                price_down.append(0)
            elif (cur_open_price < prev_price):
                price_down.append(-cur_open_price + prev_price)
                price_up.append(0)
                
            # buy and sale
            if (buy_mode == 0 and cur_rsi < 30):
                buy_mode = 1
                buy_price = stock_price_df.iloc[i,4]
                buy_time = stock_price_df.iloc[i,0]
            elif (buy_mode == 1 and cur_rsi > 70):
                buy_mode = 0
                sale_price = stock_price_df.iloc[i,4]
                sale_time = stock_price_df.iloc[i,0]
                asset = asset * sale_price / buy_price
                #print("buy at ",buy_price,", sale at ",sale_price)
                return_rate_list.append([buy_price, buy_time, sale_price, sale_time, asset])
            
            prev_price = stock_price_df.iloc[i,1]
        #return_rate_df.loc[date,'baidu'] = asset
            
                
            
                
                
        


# In[56]:


return_rate_df = pd.DataFrame(columns = ['buy price','buy time',
                                         'sale price', 'sale time','asset'], data = return_rate_list)


# In[ ]:


# the return rate of the msi strategy is 2341% from 2005 to 2020
# the strategy is relatively good
# next step:
# 1. the strategy is about 36% correct


# In[78]:


# calculating the return rate
#return_rate_df = pd.DataFrame(columns = ['baidu'],index = date_series)
return_rate_list = []

price_up= []
price_down = []
prev_price = np.nan

buy_price = 0
buy_time = ''
sale_price = 0
sale_time = ''
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
        for i in range(0,len(stock_price_df)):
            cur_rsi = np.nan
            cur_open_price = stock_price_df.iloc[i,1]
            # calculate rsi
            if (len(price_up) >= 14):
                avg_gain = np.array(price_up[-15:-1]).mean()
                avg_loss = np.array(price_down[-15:-1]).mean()
                cur_rsi = 100 - 100 / (1 + avg_gain / avg_loss)
                
            
            # adding price up and price down for average gain and avg loss
            if (np.isnan(prev_price)):
                price_up.append(0)
                price_down.append(0)
            elif (cur_open_price > prev_price):
                price_up.append(cur_open_price - prev_price)
                price_down.append(0)
            elif (cur_open_price < prev_price):
                price_down.append(-cur_open_price + prev_price)
                price_up.append(0)
                
            # buy and sale
            if (buy_mode == 0 and cur_rsi < 30):
                buy_mode = 1
                buy_price = stock_price_df.iloc[i,4]
                buy_time = stock_price_df.iloc[i,0]
            elif (buy_mode == 1 and cur_rsi > 70):
                buy_mode = 0
                sale_price = stock_price_df.iloc[i,4]
                sale_time = stock_price_df.iloc[i,0]
                asset = asset * sale_price / buy_price
                #print("buy at ",buy_price,", sale at ",sale_price)
                return_rate_list.append([buy_price, buy_time, sale_price, sale_time, asset])
            # contigency plan
            elif (buy_mode == 1 and cur_open_price < buy_price * 0.95):
                buy_mode = 0
                sale_price = stock_price_df.iloc[i,4]
                sale_time = stock_price_df.iloc[i,0]
                asset = asset * sale_price / buy_price
                #print("buy at ",buy_price,", sale at ",sale_price)
                return_rate_list.append([buy_price, buy_time, sale_price, sale_time, asset])
                
            
            prev_price = stock_price_df.iloc[i,1]
        #return_rate_df.loc[date,'baidu'] = asset


# In[79]:


return_rate_df = pd.DataFrame(columns = ['buy price','buy time',
                                         'sale price', 'sale time','asset'], data = return_rate_list)


# In[80]:


return_rate_df
# the return rate of the msi strategy is 2427% from 2005 to 2020
# the strategy is relatively good
# next step:
# try MFI


# In[ ]:




