import streamlit as st
from modules.geo_wealth_maps import render_geo_wealth_module
from modules.wealth_calculator import render_wealth_calculator
from modules.credit_analyzer import render_credit_analyzer
from modules.prospect_manager import render_prospect_manager
from backend_engine import get_wealth_data

st.set_page_config(page_title="Advisor Terminal", layout="wide", page_icon="💎")

# Sidebar
st.sidebar.title("💎 Advisor Hub")
st.sidebar.write("Inteligência aplicada à prospecção")
st.write("Você no comando, prospectando com inteligência e estratégia.")
menu = st.sidebar.radio("Navegação", ["GeoWealth", "Simulador", "Comparador", "Pipe Estratégico"])

# Carregamos o dado uma única vez aqui para evitar erros de variável local
df_principal = get_wealth_data()

if menu == "GeoWealth":
    render_geo_wealth_module(df_principal) # Passamos o df explicitamente
elif menu == "Simulador":
    render_wealth_calculator()
elif menu == "Comparador":
    render_credit_analyzer()
elif menu == "Pipe Estratégico":

    render_prospect_manager(df_principal)    
