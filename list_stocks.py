# %%
import pandas as pd

def list_b3_stocks():
    """
    Lista todas as ações negociadas na B3 (Bolsa de Valores do Brasil)
    Retorna lista básica das principais ações
    """
    return get_main_b3_stocks()


def get_main_b3_stocks():
    """
    Retorna uma lista das principais ações negociadas na B3 (IBOVESPA)
    Inclui as ações mais líquidas e negociadas - aproximadamente 80+ ações
    """
    # Lista das principais ações da B3 (IBOVESPA e outras)
    # Formato: código sem .SA (será adicionado depois)
    main_stocks = [
        # Bancos e Financeiras
        'BBAS3', 'ITUB4', 'BBDC4', 'SANB11', 'BBDC3', 'ABCB4', 'BPAC11',
        'ITSA4', 'BPAN4', 'CARD3',
        # Petróleo e Energia
        'PETR4', 'PETR3', 'VALE3', 'ELET3', 'ELET6', 'CSNA3', 'USIM5',
        'CMIG4', 'CPLE6', 'EGIE3', 'ENBR3', 'EQTL3', 'TAEE11',
        # Varejo e Consumo
        'ABEV3', 'RENT3', 'LREN3', 'MGLU3', 'VIVT3', 'TIMS3', 'PCAR3',
        'PETZ3', 'VIIA3', 'YDUQ3',
        # Tecnologia e Construção
        'WEGE3', 'RADL3', 'CYRE3', 'TOTS3', 'HAPV3',
        # Siderurgia e Mineração
        'GGBR4', 'GOAU4', 'CSAN3',
        # Outras
        'HYPE3', 'IRBR3', 'KLBN11', 'LIGT3', 'MULT3',
        'PRIO3', 'QUAL3', 'RAIL3', 'SBSP3', 'SUZB3',
        'UGPA3', 'BRAP4', 'BRKM5', 'BRML3', 'CCRO3',
        'CIEL3', 'CPFE3', 'CRFB3', 'CVCB3', 'DXCO3',
        'ELET3', 'EMBR3', 'ENGI11', 'FLRY3', 'GNDI3',
        'HAPV3', 'IGTA3', 'JHSF3', 'JSLG3', 'KLBN11',
        'LWSA3', 'MRFG3', 'MRVE3', 'NTCO3', 'POMO4',
        'POSI3', 'RAPT4', 'RDOR3', 'RECV3', 'RRRP3',
        'SLCE3', 'SMTO3', 'SOMA3', 'SUZB3', 'TEND3',
        'TGMA3', 'TRPL4', 'VAMO3', 'VBBR3', 'VLID3',
        'VSTE3', 'VVAR3', 'WIZS3', 'ZAMP3'
    ]
    
    # Remover duplicatas e ordenar
    main_stocks = sorted(list(set(main_stocks)))
    
    # Adicionar sufixo .SA para compatibilidade com yfinance
    stocks_with_suffix = [f"{stock}.SA" for stock in main_stocks]
    
    df = pd.DataFrame({
        'Ticker': stocks_with_suffix,
        'Código': main_stocks
    })
    
    return df


def get_all_b3_stocks_from_file():
    """
    Função para carregar lista completa de ações de um arquivo CSV
    Você pode criar um arquivo stocks_list.csv com todas as ações
    """
    try:
        df = pd.read_csv('stocks_list.csv')
        return df
    except FileNotFoundError:
        print("Arquivo stocks_list.csv não encontrado.")
        return None


# Função principal mais completa usando investpy (requer instalação)
def list_all_b3_stocks_investpy():
    """
    Lista todas as ações usando investpy (requer: pip install investpy)
    Esta é a forma mais completa e atualizada
    """
    try:
        import investpy
        
        print("Buscando ações brasileiras usando investpy...")
        stocks = investpy.get_stocks_list(country='brazil')
        
        # Adicionar sufixo .SA para yfinance
        stocks_df = pd.DataFrame({
            'Ticker': [f"{stock}.SA" for stock in stocks],
            'Código': stocks
        })
        
        return stocks_df
    except ImportError:
        print("⚠️  Biblioteca investpy não instalada.")
        print("Para lista completa, instale com: pip install investpy")
        return get_main_b3_stocks()
    except Exception as e:
        print(f"Erro ao buscar com investpy: {e}")
        return get_main_b3_stocks()


if __name__ == "__main__":
    # Tentar usar investpy primeiro, senão usar lista principal
    df_stocks = list_all_b3_stocks_investpy()
    
    print(f"\n✅ Total de ações encontradas: {len(df_stocks)}")
    print("\nPrimeiras 20 ações:")
    print(df_stocks.head(20))
    
    # Salvar em CSV
    df_stocks.to_csv('b3_stocks_list.csv', index=False)
    print(f"\n💾 Lista salva em 'b3_stocks_list.csv'")
    
    # Mostrar algumas estatísticas
    print(f"\n📊 Estatísticas:")
    print(f"   Total de tickers: {len(df_stocks)}")
    print(f"\nÚltimas 10 ações:")
    print(df_stocks.tail(10))

# %%

