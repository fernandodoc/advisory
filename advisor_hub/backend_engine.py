import pandas as pd

def get_wealth_data():
    """
    Cérebro de Inteligência Geográfica e Comportamental.
    Foco: Segmento Alta Renda / Wealth Management (Tickets > R$ 300k).
    """
    data = {
        'Estado': [
            'Distrito Federal', 'São Paulo', 'Mato Grosso', 
            'Santa Catarina', 'Rio de Janeiro', 'Paraná', 'Goiás'
        ],
        'Região': [
            'Centro-Oeste', 'Sudeste', 'Centro-Oeste', 
            'Sul', 'Sudeste', 'Sul', 'Centro-Oeste'
        ],
        'Renda_Media': [
            4257, 3520, 2850, 3122, 3354, 2987, 2490
        ],
        'Publico_Alvo': [
            'Altos Funcionários Públicos / Judiciário', 
            'Executivos C-Level / Mercado Financeiro / Tech', 
            'Grandes Produtores Rurais / Donos de Revendas Agro', 
            'Empresários Têxteis / Investidores Imobiliários', 
            'Engenheiros de Petróleo / Oficiais / Herdeiros',
            'Empresários Industriais / Agroindustriais',
            'Pecuaristas / Donos de Frigoríficos / Grãos'
        ],
        'Janela_Liquidez': [
            'Fevereiro (Bônus/PLR)', 
            'Março (Dividendos e Bônus Corporativos)', 
            'Abril (Liquidação de Safra)', 
            'Dezembro (Ciclo Turístico/Vendas)', 
            'Janeiro (Recebimento de Royalties)',
            'Maio (Segunda Safra)',
            'Junho (Leilões de Gado)'
        ],
        'Principais_Condominios': [
            'Lago Sul, Mansões Dom Bosco, Sudoeste', 
            'Itaim Bibi, Tamboré, Fazenda Boa Vista', 
            'Portal da Mata (Sinop), Carpe Diem (Sorriso)', 
            'Brava Home (BC), Jurerê Internacional', 
            'Jardim Pernambuco (Leblon), Santa Mônica',
            'Batel, Ecoville, Condomínio Alphaville PR',
            'Setor Marista, Aldeia do Vale (Goiânia)'
        ],
        'Dor_Principal': [
            'Planejamento Sucessório e ITCMD', 
            'Eficiência Fiscal, Offshore e Previdência', 
            'Gestão de Caixa Rural e Proteção Cambial (Hedge)', 
            'Blindagem Patrimonial e Holding Familiar', 
            'Diversificação Internacional e Renda Fixa High Yield',
            'Sucessão em Empresas Familiares',
            'Alocação Estruturada e Liquidez Diária'
        ],
        'Lat': [-15.79, -23.55, -12.64, -27.59, -22.90, -25.42, -16.68],
        'Lon': [-47.88, -46.63, -55.49, -48.54, -43.17, -49.27, -49.25]
    }
    
    return pd.DataFrame(data)

def get_macro_indicators():
    """
    Retorna indicadores macroeconômicos para o Dashboard.
    Pode ser expandido para coletar via API do BCB futuramente.
    """
    return {
        'Selic': '10.75%',
        'IPCA_12m': '4.50%',
        'Ibovespa': '130.000 pts',
        'Dolar': 'R$ 5.10'
    }

def get_wealth_data():
    data = {
        'Estado': ['Distrito Federal', 'São Paulo', 'Mato Grosso', 'Santa Catarina', 'Rio de Janeiro', 'Paraná', 'Goiás'],
        'Região': ['Centro-Oeste', 'Sudeste', 'Centro-Oeste', 'Sul', 'Sudeste', 'Sul', 'Centro-Oeste'],
        'Renda_Media': [4257, 3520, 2850, 3122, 3354, 2987, 2490],
        'Publico_Alvo': ['Altos Funcionários Públicos', 'Executivos C-Level', 'Produtores Rurais', 'Empresários', 'Engenheiros/Herdeiros', 'Agroindustriais', 'Pecuaristas'],
        'Janela_Liquidez': ['Fevereiro (Bônus)', 'Março (Dividendos)', 'Abril (Safra)', 'Dezembro (Vendas)', 'Janeiro (Royalties)', 'Maio (2ª Safra)', 'Junho (Leilões)'],
        'Dor_Principal': ['Sucessão Patrimonial', 'Eficiência Fiscal', 'Proteção Cambial', 'Blindagem (Holding)', 'Diversificação', 'Modernização Portfólio', 'Liquidez'],
        'Principais_Condominios': ['Lago Sul, Mansões Dom Bosco', 'Itaim Bibi, Tamboré, Jd. Europa', 'Portal da Mata, Carpe Diem', 'Brava Home, Jurerê', 'Leblon, Jd. Pernambuco', 'Batel, Ecoville', 'Aldeia do Vale, Setor Marista'],
        'Organizacoes': ['OAB, CRM, TCU', 'Fiesp, B3, Amcham', 'Aprosoja, Famato', 'Fiesc, Facisc', 'Clubes de Engenharia', 'Fiep, Ocepar', 'Fapeg, SGPA'],
        'Lat': [-15.79, -23.55, -12.64, -27.59, -22.90, -25.42, -16.68],
        'Lon': [-47.88, -46.63, -55.49, -48.54, -43.17, -49.27, -49.25]
    }
    return pd.DataFrame(data)