# TS Features

Module for extracting time series data components.

## 1. Method

A Time Series $TS$ of size $m$ is defined as an ordered sequence of observations, i.e., $ TS=(s_1, s_2,..., s_m)$, where $s_t \in \mathbb{R}^d $ represents an observation $s$ at time $t$ with $d$ features. A time series can be composed of the following components:

<p align="center">
TS = T + S + C + N
</p>

where $T$ refers to trend, $S$ is seasonality, $C$ is cyclical variation, and $N$ is Noise. Each component captures some important features of the series dynamics. Seasonality refers to patterns that repeat at regular intervals within the time series. These patterns could be daily($d$), fortnightly($f$), monthly($m$), quarterly($q$), or yearly($y$), depending on the specific application.

The trend component captures the long-term direction or tendency of the time series. Cyclical variation represents the recurrent but non-periodic fluctuations in the time series that occur over extended periods. Noise $N$ represents the unpredictable and random fluctuations present in the time series. The Level ($L$) is another fundamental component implicitly present in any time series. The level is the average value in the series over some time ($j$).

TS Features is a method for extracting time series features from its components and fluctuations daily. The features $d$ of $s_i$ represent opening($o$), closing($c$), high($h$), low($l$) and volume($v$) values of the agribusiness financial market. The features are designed to capture various aspects of the time series and provide valuable insights into its behavior present in Table below:

<div align="center">

| Feature | Description |
| --- | --- |
| Closing intraday           | Percentual difference between $s_i^c$ and $s_{i+1}^c$.    | 
| Open/Close intraday        | Percentual difference between $s_i^o$ and $s_{i-1}^c$.    |
| Open/Close daily           | Percentual difference between $s_i^{d(o, c)}$.            |  
| Low/High daily             | Percentual difference between $s_i^{d(l, h)}$.            |  
| Vol.  (yearly)             | Percentual difference between $L_j^{v_y}$ and $s_i^v$.    |   
| Vol.  (quarterly)          | Percentual difference between $L_j^{v_q}$ and $s_i^v$.    | 
| Vol.  (monthly)            | Percentual difference between $L_j^{v_m}$ and $s_i^v$.    | 
| Vol.  (fortnightly)        | Percentual difference between $L_j^{v_f}$ and $s_i^v$.    | 
| Trend (yearly)             | Upward, downward, or neutral trends in $T_j^y$.           | 
| Trend (quarterly)          | Upward, downward, or neutral trends in $T_j^q$.           | 
| Trend (monthly)            | Upward, downward, or neutral trends in $T_j^m$.           | 
| Trend (fortnightly)        | Upward, downward, or neutral trends in $T_j^f$.           | 
| Seas. (quarterly)          | Perc. of occurrences of a specific trend in $S_j^{T_q}$.  | 
| Seas. (monthly)            | Perc. of occurrences of a specific trend in $S_j^{T_m}$.  | 
| Seas. (fortnightly)        | Perc. of occurrences of a specific trend in $S_j^{T_f}$.  | 
| Level (yearly)             | Percentual difference between $L_j^{c_y}$ and $s_i$.      | 
| Level (quarterly)          | Percentual difference between $L_j^{c_q}$ and $s_i$.      | 
| Level (monthly)            | Percentual difference between $L_j^{c_m}$ and $s_i$.      | 
| Level (fortnightly)        | Percentual difference between $L_j^{c_f}$ and $s_i$.      | 

</div>

The intra-day, open/close, and low/high features represent the daily oscillations of data points ($S_i^d$) in a time series. The features yearly, quarterly, monthly, and fortnightly volumes represent the percentage difference of the time series level ($L_j$) in each data point ($s_i$) within specific time intervals. The trends ($T$) features represent the results of the Mann-Kendall (MK) test applied to the time series within specific time intervals. The seasonality (seas.) or cyclical features indicate the percentage of trend occurrences within specific previous periods $S_j$. The level features represent the percentage difference between a price series (closing) level and its corresponding value within specific periods, such as yearly, quarterly, monthly, and fortnightly intervals.

## 2. Installation

Installation and use can be done as:

```python
!git clone https://github.com/ivanfilhoreis/ts_features.git
!pip install -r requirements.txt
```

## 3. Usage

The most minimal example can be seen below:

```python
import pandas as pd

df = pd.read_csv("dataset/soja_CBOT.csv")
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by='Date', inplace = True)
df.reset_index(drop=True, inplace=True)

```
The default parameters of TS-Features are:

```python
tsf_vectorizer(mult = True,            # multivariate (True) or univariate (False)
               steps = 'wmsy',         # steps: week(w), monthly (m), split year (s), yearly(y)
               levels = True,          # level (w,m,s,y)
               trends = True,          # trends (w,m,s,y)
               seas = True,            # seasonality (w,m,s,y)
               vol = True,             # volume (w,m,s,y)
               osc = True,             # daily oscilation (intra-day)
               lag = False,            # lag
               diff_vl = True,         # diff Open/Close, Low/High
               feature = 'perc',       # Options: label, perc, value
               slice_month = int(15),  # split the month into a set of days.
               slice_year = int(3)     # split the year into a set of month.
               )->None:
```

So, you can use fit_transform from tsf_vectorizer to extract features from time series components:

```python
from ts_features import tsf_vectorizer

tsf = tsf_vectorizer()
df_tsf = tsf.fit_transform(df)

df_tsf.sample()
```

## 4. How to use TS Features

A public version of TS Features is available in this [Jupyter Notebook](TS_Features.ipynb), with examples for extracting features from time series components.

## 5. Citing

In process.
