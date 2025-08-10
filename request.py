# %%
import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq

# find value of interest
kw_list = ['BBAS3']


def find_ticker(ticker, start_date='2025-01-01', end_date='2025-08-10'):
    pytrend = TrendReq()
    pytrend.build_payload(ticker, timeframe=f'{start_date} {end_date}', geo='BR')
    df = pd.DataFrame(pytrend.interest_over_time())
    return df

df = find_ticker(kw_list)
column_names = df.columns.tolist()

def show_graph(df, column_names=None):
    print(f"DataFrame columns: {column_names}")
    column_names = df.columns.tolist()
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df[column_names[0]], label=f'{column_names[0]} Interest', color='blue')
    plt.title(f'Interest Over Time for {column_names[0]}')
    plt.xlabel('Date')
    plt.ylabel('Interest')
    plt.legend()
    plt.grid()
    plt.show()

show_graph(df, column_names)
# %%
