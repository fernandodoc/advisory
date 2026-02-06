import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render_credit_analyzer():
    st.title("⚖️ Comparador de Aquisição: Financiamento vs Consórcio vs Investimento")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📝 Dados do Bem")
        valor_bem = st.number_input("Valor do Bem (R$)", min_value=100000.0, value=500000.0, step=50000.0)
        prazo_meses = st.slider("Prazo (Meses)", 12, 240, 60)
        
        st.divider()
        st.subheader("🏦 1. Financiamento (SAC)")
        taxa_juros_anual = st.number_input("Taxa de Juros Financiamento (% a.a.)", value=10.5)
        
        st.subheader("🤝 2. Consórcio")
        taxa_adm_total = st.number_input("Taxa de Adm. Total (%)", value=15.0)
        lance_embutido_pct = st.slider("Lance Embutido (%)", 0, 30, 0)

        st.subheader("💎 3. Investimento (Sua Gestão)")
        rentabilidade_anual = st.number_input("Rentabilidade da Carteira (% a.a.)", value=12.0)

    # --- LÓGICA DE CÁLCULO ---
    
    # 1. Financiamento (SAC)
    juros_mensal = (1 + taxa_juros_anual/100)**(1/12) - 1
    amortizacao = valor_bem / prazo_meses
    total_financiado = 0
    for i in range(prazo_meses):
        juros_do_mes = (valor_bem - (i * amortizacao)) * juros_mensal
        total_financiado += amortizacao + juros_do_mes
    
    # 2. Consórcio (Custo Real com Lance Embutido)
    # O lance embutido reduz o crédito recebido mas mantém a taxa sobre o valor total da carta
    valor_credito_real = valor_bem * (1 - lance_embutido_pct/100)
    total_consorcio = valor_bem * (1 + taxa_adm_total/100)
    
    # 3. Investimento (Patrimônio acumulado investindo o valor da parcela do financiamento)
    parcela_media_fin = total_financiado / prazo_meses
    r_mensal_inv = (1 + rentabilidade_anual/100)**(1/12) - 1
    patrimonio_investido = 0
    for _ in range(prazo_meses):
        patrimonio_investido = (patrimonio_investido + parcela_media_fin) * (1 + r_mensal_inv)

    with col2:
        st.subheader("📊 Resultado Comparativo")
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Total Financiado", f"R$ {total_financiado:,.2f}", delta="Custo Juros", delta_color="inverse")
        m_col2.metric("Total Consórcio", f"R$ {total_consorcio:,.2f}", delta="Taxa Adm", delta_color="inverse")
        m_col3.metric("Patrimônio Final", f"R$ {patrimonio_investido:,.2f}", delta="Ganho Juros")

        # Gráfico de Barras Comparativo
        fig = go.Figure(data=[
            go.Bar(name='Custo Total de Saída', x=['Financiamento', 'Consórcio'], 
                   y=[total_financiado, total_consorcio], marker_color=['#E74C3C', '#F1C40F']),
            go.Bar(name='Patrimônio Final Acumulado', x=['Estratégia Investimento'], 
                   y=[patrimonio_investido], marker_color=['#2ECC71'])
        ])
        
        fig.update_layout(
            barmode='group', 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.info(f"💡 **Veredito Final:** Se não houver urgência imediata, a estratégia de investimento entrega um excedente patrimonial de **R$ {patrimonio_investido - total_financiado:,.2f}** frente ao financiamento.")

        with st.expander("📝 Explicação Estratégica para o Cliente"):
            st.write(f"""
            * **Financiamento (SAC):** Você compra o tempo. É a posse imediata, mas o custo dos juros consome parte do seu patrimônio futuro.
            * **Consórcio:** É um autofinanciamento com taxa de administração. O custo é menor que o financiamento, porém sem a garantia de posse imediata.
            * **Investimento:** Invertemos a lógica bancária. Em vez de pagar juros, você os recebe. Em {prazo_meses} meses, você tem capital para comprar o bem à vista e ainda mantém uma reserva robusta.
            """)

        st.markdown("---")
        st.subheader("📲 Finalização da Consultoria")
        
        # Campo para digitar o WhatsApp do cliente
        celular_cliente = st.text_input("WhatsApp do Cliente (Apenas números com DDD):", placeholder="Ex: 11999999999")
        
        # Gerador de proposta formatada
        texto_proposta = (
            f"*PROPOSTA PATRIMONIAL EXCLUSIVA* 💎\n"
            f"------------------------------------------\n"
            f"Olá! Analisei os cenários de aquisição para o seu projeto de *R$ {valor_bem:,.2f}*:\n\n"
            f"1️⃣ *FINANCIAMENTO:* Custo de R$ {total_financiado:,.2f} (Posse imediata).\n"
            f"2️⃣ *CONSÓRCIO:* Custo de R$ {total_consorcio:,.2f} (Depende de contemplação).\n"
            f"3️⃣ *ESTRUTURA DE INVESTIMENTO:* Investindo a mesma parcela, em {prazo_meses} meses seu patrimônio seria de *R$ {patrimonio_investido:,.2f}*.\n\n"
            f"👉 *Conclusão:* A estratégia de investimento gera uma preservação de capital de *R$ {patrimonio_investido - total_financiado:,.2f}*.\n\n"
            f"Faz sentido agendarmos uma breve reunião para detalhar essa estrutura?\n"
            f"------------------------------------------\n"
            f"_Fernando - Especialista de Investimentos_"
        )

        if st.button("📝 Gerar Prévia da Proposta"):
            st.text_area("Mensagem para conferência:", value=texto_proposta, height=250)
            
            if celular_cliente:
                link_whatsapp = f"https://wa.me/{celular_cliente}?text={texto_proposta.replace(' ', '%20').replace('*', '%2A').replace('\n', '%0A')}"
                st.link_button("🚀 Enviar Direto para o WhatsApp", link_whatsapp)
            else:
                st.warning("Insira o número do WhatsApp acima para habilitar o envio direto.")