# %% 
import pandas as numpy 
import datetime as dt 
import matplotlib.pyplot as plt
import yfinance as yf

day_end = dt.date.today()
stocks = ['BBAS3.SA', 'PETR4.SA']

df = yf.download(stocks, start='2025-01-01', end=dt.date.today())

df['Close']['BBAS3.SA'].head()
# %%
