# -*- coding: utf-8 -*-
# Authors: Ivan José dos Reis Filho <ivan.filho@uemg.br>
import pandas as pd
import pymannkendall as mk
import math
import numpy as np

#__all__ = ['ts_features']

class tsf_vectorizer:
    
    r"""
    This module extracts information from time series of prices.
    
    The algorithm extracts differences in values extracted from the levels of each time interval, 
    trends, seasonality, volumes, daily oscillations, and differences between opening
    and closing and between minimums and maximums prices.
    
    """
    
    def __init__(self, 
                 mult   = True,
                 levels = True,
                 trends = True,
                 seas   = True,
                 vol    = True,
                 osc    = True,
                 lag    = False,
                 diff_vl = True,
                 label = False,
                 feature = 'perc', # label, perc, value
                 steps  = 'wmsy',
                 slice_month = int(15),
                 slice_year = int(3)
                 )->None:
    
        self.mult = mult
        self.levels = levels
        self.trends = trends
        self.seas = seas
        self.vol = vol
        self.osc = osc
        self.lag = lag
        self.feature = feature
        self.diff_vl = diff_vl
        self.label = label
        self.steps = steps
        self.slice_month = slice_month
        self.slice_year = slice_year
        
    def pre_processing(self, ts):
        
        ts['year'] = [d.year for d in ts.Date]
        ts['month'] = [int(m.strftime('%m')) for m in ts.Date]
        
        ts['slice_month'] = [d.day / self.slice_month for d in ts.Date]
        ts['slice_month'] = ts['slice_month'].apply(lambda x: math.ceil(x))
        
        ts['slice_year'] = [int(b.strftime('%m')) / self.slice_year for b in ts.Date]
        ts['slice_year'] = ts['slice_year'].apply(lambda x: math.ceil(x))
        
        return ts
    
    def get_level(self, ts):
              
        if 'y' in self.steps and self.levels:
        
            y_lvl = ts[['Close', 'year']].groupby(['year']).mean().reset_index()
            y_lvl.rename(columns={"Close": "level"}, inplace=True)
            
            ts['lvl_year'] = 0.0
            
            for c, y in y_lvl[['level','year']].values:
                
                
                if self.feature == 'label':
                    ts.loc[(ts['year'] == y) & 
                           (ts['Close'] > c), 'lvl_year'] = 1
                    ts.loc[(ts['year'] == y) &
                           (ts['Close'] < c), 'lvl_year'] = -1

                if self.feature == 'value':
                    ts.loc[(ts['year'] == y), 'lvl_year'] = ts['Close'].apply(lambda x: x - c).round(2)

                if self.feature == 'perc':
                    
                    ts.loc[(ts['year'] == y), 'lvl_year'] = ts['Close'].apply(lambda x: ((x - c) / c)*100).round(2)
                    
        if 'm' in self.steps and self.levels: 
            m_lvl = ts[['Close', 'year', 'month']].groupby(['year', 'month']).mean().reset_index()
            m_lvl.rename(columns={"Close": "level"}, inplace=True)
              
            ts['lvl_month'] = 0.0
                        
            for c, y, m in m_lvl[['level','year', 'month']].values:
                
                if self.feature == 'label':
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m) &
                           (ts['Close'] > c), 'lvl_month'] = 1
                    
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m) &
                           (ts['Close'] < c), 'lvl_month'] = -1
                
                if self.feature == 'value':
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m), 'lvl_month'] = ts['Close'].apply(lambda x: x - c).round(2)
                
                if self.feature == 'perc':
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m), 'lvl_month'] = ts['Close'].apply(lambda x: ((x - c) / c)*100).round(2)
        
        if 's' in self.steps and self.levels:
        
            s_lvl = ts[['Close', 'year', 'slice_year']].groupby(['year', 'slice_year']).mean().reset_index()
            s_lvl.rename(columns={"Close": "level"}, inplace=True)
            
            ts['lvl_slice_year'] = 0.0
        
            for c, y, s in s_lvl[['level','year', 'slice_year']].values:
                
                if self.feature == 'label':
                    ts.loc[(ts['year'] == y) &
                           (ts['slice_year'] == s) &
                           (ts['Close'] > c), 'lvl_slice_year'] = 1
                    ts.loc[(ts['year'] == y) &
                           (ts['slice_year'] == s) &
                           (ts['Close'] < c), 'lvl_slice_year'] = -1
                    
                if self.feature == 'value':
                    ts.loc[(ts['year'] == y) &
                           (ts['slice_year'] == s), 'lvl_slice_year'] = ts['Close'].apply(lambda x: x - c).round(2)
                    
                if self.feature == 'perc':
                    ts.loc[(ts['year'] == y) &
                           (ts['slice_year'] == s), 'lvl_slice_year'] = ts['Close'].apply(lambda x: ((x - c) / c)*100).round(2)
        
        if 'w' in self.steps and self.levels:
        
            w_lvl = ts[['Close', 'year', 'month', 'slice_month']].groupby(['year', 'month', 'slice_month']).mean().reset_index()
            w_lvl.rename(columns={"Close": "level"}, inplace=True)
            
            ts['lvl_slice_month'] = 0.0
            
            for c, y, m, w in w_lvl[['level','year', 'month', 'slice_month']].values:
                
                if self.feature == 'label':
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m) &
                           (ts['slice_month'] == w) &
                           (ts['Close'] > c), 'lvl_slice_month'] = 1
                    
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m) &
                           (ts['slice_month'] == w) &
                           (ts['Close'] < c), 'lvl_slice_month'] = -1
                    
                if self.feature == 'value':
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m) &
                           (ts['slice_month'] == w), 'lvl_slice_month'] = ts['Close'].apply(lambda x: x - c).round(2)
                
                if self.feature == 'perc':
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m) &
                           (ts['slice_month'] == w), 'lvl_slice_month'] = ts['Close'].apply(lambda x: ((x - c) / c)*100).round(2)
                    
        return ts
    
    def get_trends(self, ts):
        
        if 'y' in self.steps and self.trends: 

            ts['trd_year'] = 0.0
            
            for y in ts['year'].unique():
                dt = ts[(ts['year'] == y)]
                result = mk.original_test(dt['Close'])
              
                if result.trend == 'decreasing':
                    ts.loc[(ts['year'] == y), 'trd_year'] = -1.0
                elif result.trend == 'increasing':
                    ts.loc[(ts['year'] == y), 'trd_year'] = 1.0

        if 'm' in self.steps and self.trends:
            ts['trd_month'] = 0.0
            
            for y in ts['year'].unique():
                for m in ts['month'].unique():
                    dt = ts[(ts['year'] == y) & (ts['month'] == m)]
                    result = mk.original_test(dt['Close'])
              
                    if result.trend == 'decreasing':
                        ts.loc[(ts['year'] == y) & 
                               (ts['month'] == m), 'trd_month'] = -1.0
                    elif result.trend == 'increasing':
                        ts.loc[(ts['year'] == y) & 
                               (ts['month'] == m), 'trd_month'] = 1.0
                        
        if 'w' in self.steps and self.trends:
            ts['trd_slice_month'] = 0.0
            
            for y in ts['year'].unique():
                for m in ts['month'].unique():
                    for w in ts['slice_month'].unique():
                        dt = ts[(ts['year'] == y) &
                                (ts['month'] == m) & 
                                (ts['slice_month'] == w)]
                        
                        if dt.shape[0] > 3:
                            result = mk.original_test(dt['Close'])
                      
                            if result.trend == 'decreasing':
                                ts.loc[(ts['year'] == y) & 
                                       (ts['month'] == m) & 
                                       (ts['slice_month'] == w), 'trd_slice_month'] = -1.0
                            elif result.trend == 'increasing':
                                ts.loc[(ts['year'] == y) & 
                                       (ts['month'] == m) & 
                                       (ts['slice_month'] == w), 'trd_slice_month'] = 1.0

        if 's' in self.steps and self.trends:
            ts['trd_slice_year'] = 0.0
            
            for y in ts['year'].unique():
                for sy in ts['slice_year'].unique():
                    dt = ts[(ts['year'] == y) & (ts['slice_year'] == sy)]
                    result = mk.original_test(dt['Close'])
                    
                    if result.trend == 'decreasing':
                        ts.loc[(ts['year'] == y) & 
                               (ts['slice_year'] == sy), 'trd_slice_year'] = -1.0
                    elif result.trend == 'increasing':
                        ts.loc[(ts['year'] == y) & 
                               (ts['slice_year'] == sy), 'trd_slice_year'] = 1.0

        return ts
    
    def get_vol(self, ts):
        
        if 'y' in self.steps and self.vol:
        
            y_vol = ts[['Volume', 'year']].groupby(['year']).mean().reset_index()
            y_vol.rename(columns={"Volume": "level"}, inplace=True)

            ts['vol_year'] = 0.0
            
            for c, y in y_vol[['level','year']].values:
                
                if self.feature == 'label':
                    ts.loc[(ts['year'] == y) & 
                           (ts['Volume'] > c), 'vol_year'] = 1
                    ts.loc[(ts['year'] == y) &
                           (ts['Volume'] < c), 'vol_year'] = -1

                if self.feature == 'value':
                    ts.loc[(ts['year'] == y), 'vol_year'] = ts['Volume'].apply(lambda x: x - c).round(2)

                if self.feature == 'perc':
                    ts.loc[(ts['year'] == y), 'vol_year'] = ts['Volume'].apply(lambda x: ((x - c) / c)*100).round(2)
                    
        if 'm' in self.steps and self.vol: 
            m_vol = ts[['Volume', 'year', 'month']].groupby(['year', 'month']).mean().reset_index()
            m_vol.rename(columns={"Volume": "level"}, inplace=True)

            ts['vol_month'] = 0.0
                        
            for c, y, m in m_vol[['level','year', 'month']].values:
                
                if self.feature == 'label':
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m) &
                           (ts['Volume'] > c), 'vol_month'] = 1
                    
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m) &
                           (ts['Volume'] < c), 'vol_month'] = -1
                
                if self.feature == 'value':
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m), 'vol_month'] = ts['Volume'].apply(lambda x: x - c).round(2)
                
                if self.feature == 'perc':
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m), 'vol_month'] = ts['Volume'].apply(lambda x: ((x - c) / c)*100).round(2)
        
        if 's' in self.steps and self.vol:
        
            s_vol = ts[['Volume', 'year', 'slice_year']].groupby(['year', 'slice_year']).mean().reset_index()
            s_vol.rename(columns={"Volume": "level"}, inplace=True)
            
            ts['vol_slice_year'] = 0.0
        
            for c, y, s in s_vol[['level','year', 'slice_year']].values:
                
                if self.feature == 'label':
                    ts.loc[(ts['year'] == y) &
                           (ts['slice_year'] == s) &
                           (ts['Volume'] > c), 'vol_slice_year'] = 1
                    ts.loc[(ts['year'] == y) &
                           (ts['slice_year'] == s) &
                           (ts['Volume'] < c), 'vol_slice_year'] = -1
                    
                if self.feature == 'value':
                    ts.loc[(ts['year'] == y) &
                           (ts['slice_year'] == s), 'vol_slice_year'] = ts['Volume'].apply(lambda x: x - c).round(2)
                    
                if self.feature == 'perc':
                    ts.loc[(ts['year'] == y) &
                           (ts['slice_year'] == s), 'vol_slice_year'] = ts['Volume'].apply(lambda x: ((x - c) / c)*100).round(2)
        
        if 'w' in self.steps and self.vol:
        
            w_vol = ts[['Volume', 'year', 'month', 'slice_month']].groupby(['year', 'month', 'slice_month']).mean().reset_index()
            w_vol.rename(columns={"Volume": "level"}, inplace=True)
            
            ts['vol_slice_month'] = 0.0
            
            for c, y, m, w in w_vol[['level','year', 'month', 'slice_month']].values:
                
                if self.feature == 'label':
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m) &
                           (ts['slice_month'] == w) &
                           (ts['Volume'] > c), 'vol_slice_month'] = 1
                    
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m) &
                           (ts['slice_month'] == w) &
                           (ts['Volume'] < c), 'vol_slice_month'] = -1
                    
                if self.feature == 'value':
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m) &
                           (ts['slice_month'] == w), 'vol_slice_month'] = ts['Volume'].apply(lambda x: x - c).round(2)
                
                if self.feature == 'perc':
                    ts.loc[(ts['year'] == y) &
                           (ts['month'] == m) &
                           (ts['slice_month'] == w), 'vol_slice_month'] = ts['Volume'].apply(lambda x: ((x - c) / c)*100).round(2)
        
        return ts
    
    def get_seas(self, ts):

        if 'm' in self.steps and self.seas:       
            ts['seas_month'] = 0.0
    
            for m in ts['month'].unique():
                mnt = []
                sea = [0]
                for y in ts['year'].unique():
                    
                    yr = ts['year'].unique()
                    
                    tr = ts['trd_month'].loc[(ts['year'] == y) & 
                                             (ts['month'] == m)].unique()
                    if not np.any(tr):
                            tr = np.array([0])
                    
                    mnt.append(tr[0])
                    
                for x in range(1, len(mnt)):
                    sea.append( round(( 100 * mnt[0:x].count(mnt[x]))/ len(mnt[0:x]), 2) )
                    
                for i in range(len(sea)):
                    ts.loc[(ts['year'] == yr[i]) & (ts['month'] == m), 'seas_month'] = sea[i]
                  
                    
        if 'w' in self.steps and self.seas:       
            ts['seas_slice_month'] = 0.0
    
            for m in ts['month'].unique():
                for w in ts['slice_month'].unique():
                    mnt = []
                    sea = [0]
                    for y in ts['year'].unique():
                        
                        yr = ts['year'].unique()
                        
                        tr = ts['trd_slice_month'].loc[(ts['year'] == y) & 
                                                       (ts['month'] == m) &
                                                       (ts['slice_month'] == w)].unique()
                        
                        if not np.any(tr):
                            tr = np.array([0])
                        
                        mnt.append(tr[0])
                    
                    for x in range(1, len(mnt)):
                        sea.append( round(( 100 * mnt[0:x].count(mnt[x]))/ len(mnt[0:x]), 2) )
                      
                    for i in range(len(sea)):
                        ts.loc[(ts['year'] == yr[i]) & (ts['month'] == m) & 
                               (ts['slice_month'] == w), 'seas_slice_month'] = sea[i]
        
        if 's' in self.steps and self.seas:       
            ts['seas_slice_year'] = 0.0
    
            for s in ts['slice_year'].unique():
                mnt = []
                sea = [0]
                for y in ts['year'].unique():
                    
                    yr = ts['year'].unique()
                    
                    tr = ts['trd_slice_year'].loc[(ts['year'] == y) &
                                                  (ts['slice_year'] == s)].unique()
                    if not np.any(tr):
                            tr = np.array([0])
                    
                    mnt.append(tr[0])
                    
                for x in range(1, len(mnt)):
                    sea.append( round(( 100 * mnt[0:x].count(mnt[x]))/ len(mnt[0:x]), 2) )
                    
                for i in range(len(sea)):
                    ts.loc[(ts['year'] == yr[i]) &
                           (ts['slice_year'] == s), 'seas_slice_year'] = sea[i]
                        
        return ts
    
    def intraday_values(self, ts):
        
        
        if self.feature == 'label' and self.osc:
            
            ts['close_intraday'] = 0.0
            ts['close_intraday'] = ts['Close'].pct_change().round(decimals=4) * 100
            ts.loc[ts['close_intraday'] > 0.1, 'close_intraday'] = 1
            ts.loc[ts['close_intraday'] < 0.1, 'close_intraday'] = -1

            ts['op_cl_intraday'] = 0.0
            ts['aux'] = ts['Close'].shift(1)
            ts['op_cl_intraday'] = ((ts[['aux', 'Open']].pct_change(axis=1))['Open'] * 100).round(2)
            ts.loc[ts['op_cl_intraday'] > 0.1, 'op_cl_intraday'] = 1
            ts.loc[ts['op_cl_intraday'] < 0.1, 'op_cl_intraday'] = -1
            ts.drop(columns=['aux'], inplace = True)
            
        if self.feature == 'value' and self.osc:
            
            ts['close_intraday'] = ts['Close'].diff().round(decimals=2)
            ts['op_cl_intraday'] = ts['Open'] - ts['Close'].shift(1)
            
        if self.feature == 'perc' and self.osc:
            #ts['close_intraday'] = 0.0
            ts['close_intraday'] = ts['Close'].pct_change().round(decimals=4) * 100

            ts['aux'] = ts['Close'].shift(1)
            ts['op_cl_intraday'] = ((ts[['aux', 'Open']].pct_change(axis=1))['Open'] * 100).round(2)
            ts.drop(columns=['aux'], inplace = True)

        return ts
    
    def daily_values(self, ts):
         
        if self.feature == 'label' and self.diff_vl:
            diff = ts[['Open', 'Close']].pct_change(axis='columns').round(decimals=4) * 100
            ts['open_close']= diff['Close']
            ts.loc[ts['open_close'] > 0, 'open_close'] = 1
            ts.loc[ts['open_close'] < 0, 'open_close'] = -1
            
            diff = ts[['Low', 'High']].pct_change(axis='columns').round(decimals=4) * 100
            ts['low_high'] = diff['High']
            ts.loc[ts['low_high'] > 0, 'low_high'] = 1
            ts.loc[ts['low_high'] < 0, 'low_high'] = -1
            
        if self.feature == 'value' and self.diff_vl:
            diff = ts[['Open', 'Close']].diff(axis='columns').round(decimals=2)
            ts['open_close']= diff['Close']
            diff = ts[['Low', 'High']].diff(axis='columns').round(decimals=2)
            ts['low_high'] = diff['High']
            
        if self.feature == 'perc' and self.diff_vl:
            diff = ts[['Open', 'Close']].pct_change(axis='columns').round(decimals=4) * 100
            ts['open_close']= diff['Close']
            
            diff = ts[['Low', 'High']].pct_change(axis='columns').round(decimals=4) * 100
            ts['low_high'] = diff['High']
        
        return ts
    
    def end_ts(self, ts):

        tse = ts.drop(columns=['year', 'month', 'slice_month', 'slice_year'])
        tse.set_index('Date', inplace=True)
  
        return tse
    
    def custom_sum(self, row):

        sum_lbs = row.sum()
        vl = 0
        if sum_lbs > len(row)/2:
            vl = 1
    
        return vl

    def extract_label(self, ts):

        self.feature = 'label'
        self.seas = False
        self.trends = False

        ts_label = self.fit_transform(ts)
        df = ts_label.replace(-1.0, 0)

        df.drop(['Close', 'Volume', 'Open', 'High', 'Low'], axis=1, inplace=True)
        df['label'] = df.apply(self.custom_sum, axis = 1)
        
        return df
    
    def fit_transform(self, ts):
        
        if isinstance(ts, str):
            raise ValueError(
                "Iterable over expected time series, string object received."
                )
            
        if isinstance(self.steps, int):
            raise ValueError(
                "String expected (wmsy, wmy, my, m or y), different object received."
                )
           
        if self.steps not in ['wmsy','wmy', 'my', 'm', 'y']:
            
            raise ValueError(
                "The parameter \"steps\" should be \"wmsy\", \"wmy\", \"my\", \"m\" or \"y\""
                )
            
        if self.feature not in['perc', 'value', 'label']:
            
            raise ValueError(
                "The parameter \"features\" should be \"perc\", \"value\" or \"label\""
                )
              
        if self.mult:
            
            ts = self.pre_processing(ts)
            ts = self.intraday_values(ts)     
            ts = self.daily_values(ts)   
            ts = self.get_vol(ts) 
            ts = self.get_trends(ts)    # Melhorar: talvez colocar erro
            ts = self.get_seas(ts)      
            ts = self.get_level(ts)      
            ts = self.end_ts(ts)        
           
        else:
            
            ts = self.pre_processing(ts)
            ts = self.intraday_values(ts)
            ts = self.get_level(ts)
            ts = self.get_trends(ts)
            ts = self.get_seas(ts)
            ts = self.end_ts(ts)
        
        ts.fillna(0, inplace=True)

        return ts
    
