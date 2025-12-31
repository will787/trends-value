# %% 
import pandas as pd 
import datetime as dt 
import matplotlib.pyplot as plt
import yfinance as yf

day_end = dt.date.today()
stocks = ['BBAS3.SA', 'PETR4.SA', 'ITUB4.SA', 'VALE3.SA']

df = yf.download(stocks, start='2000-01-01', end=dt.date.today())

# Calcular retornos percentuais diários
returns = df['Close'].pct_change().dropna()

# Plotar os retornos no mesmo gráfico
plt.figure(figsize=(12, 6))
for stock in stocks:
    plt.plot(returns.index, returns[stock], label=stock, linewidth=1.5)

plt.title('Retornos Diários das Ações', fontsize=14, fontweight='bold')
plt.xlabel('Data', fontsize=12)
plt.ylabel('Retorno (%)', fontsize=12)
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Gráfico de distribuição comparativo (todas as ações juntas)
plt.figure(figsize=(12, 6))
for stock in stocks:
    # Converter retornos para percentual para visualização
    (returns[stock] * 100).hist(bins=50, alpha=0.5, label=stock.replace('.SA', ''), density=True)

plt.title('Distribuição de Retornos - Comparativo', fontsize=14, fontweight='bold')
plt.xlabel('Retorno (%)', fontsize=12)
plt.ylabel('Densidade', fontsize=12)
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Gráficos de distribuição individuais para cada ação
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for i, stock in enumerate(stocks):
    ax = axes[i]
    # Converter retornos para percentual
    ret_pct = returns[stock] * 100
    ret_pct.hist(bins=50, alpha=0.7, color=f'C{i}', edgecolor='black', ax=ax)
    ax.set_title(f'Distribuição de Retornos - {stock.replace(".SA", "")}', 
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('Retorno (%)', fontsize=10)
    ax.set_ylabel('Frequência', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Adicionar estatísticas
    mean_ret = ret_pct.mean()
    std_ret = ret_pct.std()
    ax.axvline(mean_ret, color='red', linestyle='--', linewidth=2, 
               label=f'Média: {mean_ret:.2f}%')
    ax.legend(fontsize=9)
    ax.text(0.05, 0.95, f'Std: {std_ret:.2f}%', transform=ax.transAxes,
            verticalalignment='top', fontsize=9, bbox=dict(boxstyle='round', 
            facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.show()

# Calcular Alpha de cada ação
# Alpha = Retorno do Ativo - Retorno do Benchmark (IBOVESPA)
print("\n" + "="*60)
print("CÁLCULO DE ALPHA")
print("="*60)

# Buscar dados do IBOVESPA como benchmark
benchmark_ticker = '^BVSP'  # IBOVESPA
print(f"\nBuscando dados do benchmark: {benchmark_ticker} (IBOVESPA)...")
df_benchmark = yf.download(benchmark_ticker, start='2000-01-01', end=dt.date.today(), progress=False)

# Verificar se o download funcionou
if df_benchmark.empty:
    print("⚠️  Erro: Não foi possível baixar dados do benchmark")
    print("Pulando cálculo de Alpha...")
else:
    # Ajustar estrutura se for MultiIndex
    if isinstance(df_benchmark.columns, pd.MultiIndex):
        benchmark_returns = df_benchmark['Close'].pct_change().dropna()
        # Se for DataFrame, pegar a primeira coluna ou a coluna do ticker
        if isinstance(benchmark_returns, pd.DataFrame):
            benchmark_returns = benchmark_returns.iloc[:, 0]
    else:
        if 'Close' in df_benchmark.columns:
            benchmark_returns = df_benchmark['Close'].pct_change().dropna()
        else:
            benchmark_returns = df_benchmark.iloc[:, 0].pct_change().dropna()
    
    # Alinhar índices (garantir mesmas datas)
    common_dates = returns.index.intersection(benchmark_returns.index)
    
    if len(common_dates) == 0:
        print("⚠️  Erro: Não há datas em comum entre as ações e o benchmark")
        print("Pulando cálculo de Alpha...")
    else:
        returns_aligned = returns.loc[common_dates]
        benchmark_aligned = benchmark_returns.loc[common_dates]
        
        # Garantir que benchmark_aligned é uma Series
        if isinstance(benchmark_aligned, pd.DataFrame):
            benchmark_aligned = benchmark_aligned.iloc[:, 0]
        
        # Calcular retornos anuais (aproximado)
        days_per_year = 252
        returns_annual = returns_aligned.mean() * days_per_year * 100
        benchmark_annual = benchmark_aligned.mean() * days_per_year * 100
        
        # Alpha simples: excesso de retorno sobre o benchmark
        alpha_simple = returns_annual - benchmark_annual
        
        # Alpha de Jensen (CAPM): necessita calcular Beta primeiro
        print("\nCalculando Beta e Alpha de Jensen (CAPM)...")
        import numpy as np
        
        alpha_results = {}
        beta_results = {}
        
        for stock in stocks:
            stock_returns = returns_aligned[stock].values
            benchmark_values = benchmark_aligned.values
            
            # Garantir que ambos os arrays têm o mesmo tamanho e são arrays 1D
            stock_returns = np.array(stock_returns).flatten()
            benchmark_values = np.array(benchmark_values).flatten()
            
            # Remover qualquer NaN ou infinito
            mask = ~(np.isnan(stock_returns) | np.isnan(benchmark_values) | 
                     np.isinf(stock_returns) | np.isinf(benchmark_values))
            stock_returns = stock_returns[mask]
            benchmark_values = benchmark_values[mask]
            
            if len(stock_returns) == 0 or len(benchmark_values) == 0:
                print(f"⚠️  Aviso: Dados insuficientes para {stock}")
                continue
            
            # Calcular Beta: Beta = Cov(Stock, Market) / Var(Market)
            cov_matrix = np.cov(stock_returns, benchmark_values)
            covariance = cov_matrix[0, 1] if cov_matrix.ndim == 2 else cov_matrix
            variance_market = np.var(benchmark_values, ddof=0)
            beta = covariance / variance_market if variance_market > 0 else 0
            
            # Calcular Alpha de Jensen: Alpha = R(i) - [R(f) + Beta * (R(m) - R(f))]
            # Simplificado: Alpha = R(i) - Beta * R(m) (assumindo Rf próximo de zero para períodos curtos)
            # Ou: Alpha = média(R(i)) - Beta * média(R(m))
            alpha_jensen_daily = np.mean(stock_returns) - beta * np.mean(benchmark_values)
            alpha_jensen_annual = alpha_jensen_daily * days_per_year * 100
            
            # Calcular R² (coeficiente de determinação)
            # R² = (Correlação)²
            correlation = np.corrcoef(stock_returns, benchmark_values)[0][1]
            r_squared = correlation**2 if not np.isnan(correlation) else 0
            
            alpha_results[stock] = {
                'Alpha Simples': alpha_simple[stock],
                'Alpha Jensen (CAPM)': alpha_jensen_annual,
                'Beta': beta,
                'R²': r_squared
            }
            beta_results[stock] = beta
        
        # Mostrar resultados
        if len(alpha_results) > 0:
            results_df = pd.DataFrame(alpha_results).T
            results_df.index.name = 'Ação'
            print("\n" + "="*80)
            print("RESULTADOS - ALPHA E BETA")
            print("="*80)
            print(f"\nBenchmark (IBOVESPA) - Retorno Anual Médio: {benchmark_annual:.2f}%")
            print(f"Período: {common_dates.min().date()} até {common_dates.max().date()}")
            print(f"Total de dias úteis: {len(common_dates)}")
            print("\n" + "-"*80)
            print(results_df.round(2))
            print("-"*80)
        else:
            print("\n⚠️  Nenhum resultado de Alpha calculado. Verifique os dados.")

# Explicação (só mostrar se calculamos algum alpha)
if 'alpha_results' in locals() and len(alpha_results) > 0:
    print("\n📊 INTERPRETAÇÃO:")
    print("  • Alpha Simples: Retorno excedente direto sobre o IBOVESPA")
    print("  • Alpha Jensen (CAPM): Retorno excedente ajustado pelo risco (Beta)")
    print("  • Beta: Sensibilidade do ativo em relação ao mercado")
    print("    - Beta > 1: Mais volátil que o mercado")
    print("    - Beta = 1: Move junto com o mercado")
    print("    - Beta < 1: Menos volátil que o mercado")
    print("  • R²: Qualidade do ajuste (quanto o Beta explica os movimentos)")
    print("\n✅ Alpha positivo = Ativo superou o esperado")
    print("❌ Alpha negativo = Ativo ficou abaixo do esperado")

# %%
