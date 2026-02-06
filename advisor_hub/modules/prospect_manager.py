import streamlit as st
import pandas as pd
import os

# --- FUNÇÕES DE DADOS ---

def load_leads():
    """Carrega a base de leads do ficheiro CSV ou cria uma nova se não existir."""
    file_path = 'leads.csv'
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except:
            return pd.DataFrame(columns=['Data Cadastro', 'Nome', 'Telefone', 'Região', 'Profissão', 'Banco Principal', 'Ticket Est.', 'Status', 'Notas'])
    else:
        return pd.DataFrame(columns=['Data Cadastro', 'Nome', 'Telefone', 'Região', 'Profissão', 'Banco Principal', 'Ticket Est.', 'Status', 'Notas'])

def save_lead(novo_lead):
    """Guarda o novo lead no ficheiro CSV."""
    df = load_leads()
    df = pd.concat([df, pd.DataFrame([novo_lead])], ignore_index=True)
    df.to_csv('leads.csv', index=False)

# --- INTERFACE PRINCIPAL ---

def render_prospect_manager(df_wealth):
    st.title("🎯 Gestor de Prospecção de Elite")
    st.markdown("---")

    # Carregar dados existentes
    df_leads = load_leads()

    # Divisão por abas para organização
    tab1, tab2, tab3 = st.tabs(["🔍 Inteligência de Alvos", "🆕 Cadastrar Prospect", "📋 Pipeline (CRM)"])

    # --- ABA 1: INTELIGÊNCIA E SCRIPTS ---
    with tab1:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("🕵️ Seleção de Alvo")
            estado_sel = st.selectbox("Estado Alvo:", df_wealth['Estado'].unique(), key="sel_estado_prospect")
            info = df_wealth[df_wealth['Estado'] == estado_sel].iloc[0]
            
            st.write(f"**Persona:** {info['Publico_Alvo']}")
            st.write(f"**Foco:** {info['Principais_Condominios']}")

            profissao_busca = st.text_input("Refinar Profissão para Busca:", value=info['Publico_Alvo'].split('/')[0].strip())

        with col2:
            st.subheader("🔗 Conexão Rápida")
            search_query = f"{profissao_busca} {info['Estado']}"
            linkedin_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query.replace(' ', '%20')}"
            
            st.info(f"Procurar tomadores de decisão em {estado_sel}:")
            st.link_button("🚀 Abrir LinkedIn (Filtro Sniper)", linkedin_url)
            
            maps_biz = f"empresas+perto+de+{info['Principais_Condominios']}+{info['Estado']}".replace(" ", "+")
            st.link_button("🏢 Mapear Empresas Locais", f"https://www.google.com/maps/search/{maps_biz}")

        st.divider()
        st.subheader("💬 Script de Abordagem (Copywriting Financeiro)")
        
        script_modelo = f"""Olá! Tenho acompanhado o setor de {info['Publico_Alvo']} em {estado_sel}. 

Notei que muitos profissionais desse segmento estão preocupados com {info['Dor_Principal']}, especialmente neste período de {info['Janela_Liquidez']}. 

Sou o Fernando, especialista em investimentos (C-PRO I, C-PRO R e ANCORD), e ajudo a estruturar estratégias de proteção e rentabilidade para tickets acima de R$ 300 mil. 

Faz sentido conversarmos sobre investimentos e como blindar seu patrimônio hoje?"""
        
        st.text_area("Copy para WhatsApp/LinkedIn:", value=script_modelo, height=220)
        st.caption("💡 Dica: Personalize o início mencionando uma notícia recente da região.")

    # --- ABA 2: CADASTRO ---
    with tab2:
        st.subheader("📥 Inserir Lead na Base de Dados")
        with st.form("form_prospect", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                nome = st.text_input("Nome Completo")
                telefone = st.text_input("Telefone (com DDD)")
                profissao = st.text_input("Profissão / Empresa")
            with c2:
                regiao = st.selectbox("Região do Lead", df_wealth['Estado'].unique())
                banco = st.selectbox("Banco Atual", ["Itaú Private", "BTG Pactual", "XP Wealth", "Bradesco Prime", "Santander Select", "Safra", "Outro"])
                ticket = st.number_input("Ticket Estimado (R$)", min_value=300000.0, step=100000.0)
            
            notas = st.text_area("Observações (Dores específicas, origem do contato)")
            status = st.selectbox("Status Inicial", ["Fila de Espera", "Contato Inicial", "Reunião Agendada", "Proposta Enviada"])
            
            if st.form_submit_button("✅ Salvar no CSV"):
                if nome and telefone:
                    novo_dado = {
                        'Data Cadastro': pd.Timestamp.now().strftime('%d/%m/%Y'),
                        'Nome': nome, 'Telefone': telefone, 'Região': regiao,
                        'Profissão': profissao, 'Banco Principal': banco,
                        'Ticket Est.': ticket, 'Status': status, 'Notas': notas
                    }
                    save_lead(novo_dado)
                    st.success(f"Lead {nome} arquivado com sucesso!")
                    st.rerun()
                else:
                    st.warning("Preencha Nome e Telefone para salvar.")

    # --- ABA 3: PIPELINE (CRM) ---
    with tab3:
        st.subheader("📊 Pipeline de Captação Privado")
        if not df_leads.empty:
            # Filtros Rápidos
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                filtro_status = st.multiselect("Status:", df_leads['Status'].unique(), default=df_leads['Status'].unique())
            with col_f2:
                filtro_banco = st.multiselect("Bancos:", df_leads['Banco Principal'].unique(), default=df_leads['Banco Principal'].unique())
            
            df_filtered = df_leads[(df_leads['Status'].isin(filtro_status)) & (df_leads['Banco Principal'].isin(filtro_banco))]
            
            st.dataframe(df_filtered, use_container_width=True, hide_index=True)
            
            # Métricas de Performance
            m1, m2, m3 = st.columns(3)
            m1.metric("Total de Leads", len(df_leads))
            m2.metric("Potencial (R$)", f"R$ {df_leads['Ticket Est.'].sum():,.2f}")
            m3.metric("Ticket Médio", f"R$ {df_leads['Ticket Est.'].mean():,.2f}")
            
            # Opções de limpeza
            with st.expander("⚙️ Opções Avançadas"):
                if st.button("🗑️ Apagar Todos os Leads"):
                    if os.path.exists('leads.csv'):
                        os.remove('leads.csv')
                        st.rerun()
        else:
            st.info("Sua base está vazia. Comece a prospectar alvos na primeira aba.")