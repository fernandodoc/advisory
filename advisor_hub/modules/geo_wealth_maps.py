import streamlit as st
import pandas as pd
import plotly.express as px
from backend_engine import get_wealth_data

def render_geo_wealth_module(df=None):
    """
    Renderiza o módulo de inteligência geográfica. 
    Se o df não for passado pelo app.py, ele busca direto no backend_engine.
    """
    st.title("💎 GeoWealth Intelligence: Prospecção")
    st.markdown("---")

    # 1. Garantir que os dados existam antes de qualquer visualização
    if df is None:
        df = get_wealth_data()
    
    # Adicionando a coluna de Região para garantir que o filtro funcione
    regioes_map = {
        'Distrito Federal': 'Centro-Oeste', 'São Paulo': 'Sudeste', 'Mato Grosso': 'Centro-Oeste',
        'Santa Catarina': 'Sul', 'Rio de Janeiro': 'Sudeste', 'Paraná': 'Sul', 'Goiás': 'Centro-Oeste'
    }
    df['Região'] = df['Estado'].map(regioes_map)

    # --- PARTE 1: MAPA INTERATIVO ---
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📍 Mapa de Concentração de Capital")
        fig = px.scatter_mapbox(
            df, lat="Lat", lon="Lon", size="Renda_Media", 
            color="Renda_Media", hover_name="Estado",
            hover_data=["Publico_Alvo", "Janela_Liquidez", "Dor_Principal"],
            color_continuous_scale=px.colors.sequential.YlOrBr,
            size_max=18, zoom=3, mapbox_style="open-street-map"
        )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🎯 Estratégia de Abordagem")
        # Uso de chaves únicas para evitar conflitos de widgets
        estado_sel = st.selectbox("Selecione o Estado para detalhes:", df['Estado'].unique(), key="sb_geo")
        info = df[df['Estado'] == estado_sel].iloc[0]
        
        st.info(f"📅 **Melhor Época:** {info['Janela_Liquidez']}")
        st.warning(f"⚠️ **Dor do Cliente:** {info['Dor_Principal']}")
        st.metric("Renda Média Est.", f"R$ {info['Renda_Media']:,.2f}")
        
        with st.expander("🏢 Bairros e Condomínios Alvo"):
            st.write(info['Principais_Condominios'])
            
        # Link Dinâmico Google Maps
        search_query = f"{info['Estado']} {info['Principais_Condominios']}".replace(" ", "+")
        st.link_button(f"🔍 Mapear {estado_sel}", f"https://www.google.com/maps/search/{search_query}")

    st.markdown("---")

    # --- PARTE 2: TARGET WEALTH SCANNER (ANÁLISE REGIONAL) ---
    st.subheader("🎯 Target Wealth Scanner: Filtro por Região")
    
    # Filtro Pills (Novo no Streamlit)
    regiao_sel = st.pills("Filtrar Região de Prospecção:", df['Região'].unique(), key="pills_geo")
    
    df_filtered = df[df['Região'] == regiao_sel] if regiao_sel else df

    for index, row in df_filtered.iterrows():
        with st.expander(f"📍 {row['Estado']} - Potencial de Captação"):
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**💼 Público:** {row['Publico_Alvo']}")
                # Verifica se a coluna Organizacoes existe no seu backend
                orgs = row.get('Organizacoes', 'Sindicatos e Conselhos Regionais')
                st.write(f"**🏛️ Organizações:** {orgs}")
            with c2:
                st.write(f"**🏠 Localização:** {row['Principais_Condominios']}")
                st.caption("🎯 **Foco:** Clientes com liquidez > R$ 300k")

    st.markdown("---")
    st.subheader("🏆 Ranking de Potencial (Ticket R$ 300k+)")
    st.dataframe(
        df[['Estado', 'Renda_Media', 'Publico_Alvo', 'Janela_Liquidez', 'Dor_Principal']], 
        use_container_width=True,
        hide_index=True

    )
