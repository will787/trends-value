# %%
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from pytrends.request import TrendReq

# find value of interest (single ticket)
kw_list = ['BBAS3']
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

pytrend = TrendReq()
pytrend.build_payload(kw_list, timeframe='2025-01-01 2025-10-01', geo='BR')
res = pytrend.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=True)
similars = pytrend.related_queries()

similars
# %%
