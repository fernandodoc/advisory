import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render_wealth_calculator():
    st.title("🧮 O Impacto da Gestão de Elite")
    st.subheader("Simulação de Longo Prazo: Assessoria vs Estrutura Bancária")
    st.markdown("---")

    # Layout de colunas para os parâmetros e o gráfico
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### ⚙️ Parâmetros da Simulação")
        patrimonio_inicial = st.number_input("Patrimônio Inicial (R$)", min_value=100000.0, value=300000.0, step=50000.0)
        aporte_mensal = st.number_input("Aporte Mensal (R$)", min_value=0.0, value=5000.0, step=1000.0)
        prazo_anos = st.slider("Prazo de Simulação (Anos)", 1, 30, 10)
        
        st.markdown("---")
        st.markdown("### 🏦 Cenário A - Bancos")
        taxa_banco = st.slider("Taxa Média (Adm + Custódia) % a.a.", 1.5, 4.0, 2.5)
        
        st.markdown("---")
        st.markdown("### 💎 Cenário B - Assessoria de Elite")
        taxa_elite = st.slider("Taxa de Gestão Alvo % a.a.", 0.5, 1.5, 0.8)

    with col2:
        st.markdown("### 📈 Projeção de Acúmulo de Patrimônio")
        
        # Lógica de Cálculo (Retorno bruto fixado em 10% para isolar o efeito da taxa)
        meses = prazo_anos * 12
        r_banco = (1 + 0.10 - (taxa_banco/100))**(1/12) - 1 
        r_elite = (1 + 0.10 - (taxa_elite/100))**(1/12) - 1
        
        v_banco = []
        v_elite = []
        saldo_banco = patrimonio_inicial
        saldo_elite = patrimonio_inicial

        for _ in range(meses):
            saldo_banco = (saldo_banco + aporte_mensal) * (1 + r_banco)
            saldo_elite = (saldo_elite + aporte_mensal) * (1 + r_elite)
            v_banco.append(saldo_banco)
            v_elite.append(saldo_elite)

        # Gráfico Comparativo Dinâmico
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=v_elite, name='Assessoria de Elite', line=dict(color='#FFD700', width=4)))
        fig.add_trace(go.Scatter(y=v_banco, name='Banco de Varejo', line=dict(color='#808080', width=2, dash='dash')))
        
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Patrimônio Acumulado (R$)",
            xaxis_title="Meses"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Insights de Impacto Real
        diferenca = saldo_elite - saldo_banco
        st.success(f"💰 **Diferença após {prazo_anos} anos:** R$ {diferenca:,.2f}")
        st.info(f"💡 Esta diferença representa o custo de oportunidade perdido em taxas bancárias ineficientes.")

    # Tabela de Detalhamento Anual Comparativo
    st.markdown("---")
    with st.expander(f"📄 Ver detalhamento anual comparando cenário A (Banco) e B (Assessoria de Elite)"):
        anos_list = list(range(1, prazo_anos + 1))
        dados_detalhes = pd.DataFrame({
            "Ano": anos_list,
            "Cenário A (Banco)": [v_banco[i*12-1] for i in anos_list],
            "Cenário B (Elite)": [v_elite[i*12-1] for i in anos_list]
        })
        
        # Cálculo da coluna de benefício acumulado
        dados_detalhes["Diferença Acumulada"] = dados_detalhes["Cenário B (Elite)"] - dados_detalhes["Cenário A (Banco)"]
        
        st.dataframe(
            dados_detalhes.style.format({
                "Cenário A (Banco)": "R$ {:,.2f}",
                "Cenário B (Elite)": "R$ {:,.2f}",
                "Diferença Acumulada": "R$ {:,.2f}"
            }), 
            use_container_width=True,
            hide_index=True
        )