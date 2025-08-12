# %%
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from pytrends.request import TrendReq

# find value of interest (single ticket)
kw_list = ['BBAS3', 'PETR4']
today = dt.date.today()

def find_ticker(ticker, start_date='2025-01-01', end_date=today):
    pytrend = TrendReq()
    pytrend.build_payload(ticker, timeframe=f'{start_date} {end_date}', geo='BR')
    df = pd.DataFrame(pytrend.interest_over_time())
    return df

df = find_ticker(kw_list)
column_names = df.columns.tolist()

# to do: create for comparison between two or more tickets
def show_graph_comparison(df, column_names=None):
    if column_names is None:
        column_names = df.columns.tolist()
    plt.figure(figsize=(10, 5))
    for col in column_names:
        if col == 'isPartial':
            continue
        plt.plot(df.index, df[col], label=f'{col} Interest')
    plt.title('Interest Over Time for Multiple Tickets')
    plt.xlabel('Date')
    plt.ylabel('Interest')
    plt.legend()
    plt.grid()
    plt.show()

show_graph_comparison(df, column_names)

# %%

def show_graph(df, column_names=None):
    print(f"DataFrame columns: {column_names}")
    column_names = df.columns.tolist()
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df[column_names[0]], label=f'{column_names[0]} Interest', color='blue')
    plt.plot(df.index, df[column_names[1]], label=f'{column_names[1]} Interest', color='orange')
    plt.title(f'Interest Over Time for {column_names[0]}')
    plt.xlabel('Date')
    plt.ylabel('Interest')
    plt.legend()
    plt.grid()
    plt.show()

show_graph(df, column_names)