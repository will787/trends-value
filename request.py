# %%
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
import time

# find value of interest (single ticket)
kw_list = ['BBAS3.SA', 'PETR4.SA', 'ITUB4.SA', 'VALE3.SA', 'ABEV3.SA']
today = dt.date.today()

def find_ticker(ticker, start_date='2025-01-01', end_date=today):
    print(f"   Conectando ao Google Trends...")
    pytrend = TrendReq(hl='pt-BR', tz=360, retries=2, backoff_factor=0.1)
    # Converter end_date para string no formato correto
    if isinstance(end_date, dt.date):
        end_date_str = end_date.strftime('%Y-%m-%d')
    else:
        end_date_str = str(end_date)
    print(f"   Construindo payload para {len(ticker)} termos de busca...")
    pytrend.build_payload(ticker, timeframe=f'{start_date} {end_date_str}', geo='BR')
    print(f"   Obtendo dados de interesse ao longo do tempo... (pode levar alguns segundos)")
    df = pd.DataFrame(pytrend.interest_over_time())
    return df

print("Buscando dados do Google Trends...")
print("⚠️  Nota: O Google Trends pode ser lento. Aguarde...\n")
df = find_ticker(kw_list)
print(f"Dados obtidos: {len(df)} registros")
print(f"Colunas: {df.columns.tolist()}")
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

print("\nGerando gráfico de comparação...")
show_graph_comparison(df, column_names)
print("Gráfico exibido!")


print("\nBuscando dados adicionais...")
print("⚠️  Aguarde, fazendo novas requisições ao Google Trends...\n")
time.sleep(1)
pytrend = TrendReq(hl='pt-BR', tz=360, retries=2, backoff_factor=0.1)
print("   Construindo payload...")
pytrend.build_payload(kw_list, timeframe='2025-01-01 2025-10-01', geo='BR')
print("   Obtendo dados por região...")
time.sleep(1)  
res = pytrend.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=True)
print("   Obtendo consultas relacionadas...")
time.sleep(1)
similars = pytrend.related_queries()

print("\nConsultas relacionadas:")
print(similars)
# %%
