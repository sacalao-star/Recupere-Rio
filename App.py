import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Projeto Recupere Rio", layout="wide", page_icon="🏙️")

# Estilização CSS
st.markdown("""
    <style>
    .titulo { color: #1B3A5C; font-size: 32px; font-weight: bold; text-align: center; }
    .subtitulo { color: #5C6772; font-size: 18px; font-style: italic; text-align: center; margin-bottom: 20px; }
    .kicker { color: #1B3A5C; font-size: 14px; text-align: center; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. CABEÇALHO
st.markdown('<div class="titulo">PROJETO RECUPERE RIO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Reconversão Funcional de Ativos</div>', unsafe_allow_html=True)
st.markdown('<div class="kicker">MEMORIAL TÉCNICO E DIRETRIZES DE ENGENHARIA FINANCEIRA</div>', unsafe_allow_html=True)
st.divider()

st.info("📌 **Objetivo:** Documento de consolidação técnica preparado para subsídio às Secretarias Municipais do Rio de Janeiro.")

# ---------------- SECÇÃO 1: DIRETRIZES GERAIS ----------------
st.header("1. Diretrizes Gerais e Salvaguardas")
st.write("Regras transversais de aplicação obrigatória às quatro trilhas setoriais.")

with st.expander("1.1 Teste de Enquadramento Funcional (Regra 70/50)", expanded=True):
    st.write("O investidor só mantém o regime se comprovar anualmente que no mínimo **70% da área construída** e **50% do faturamento bruto** provêm da atividade declarada.")
with st.expander("1.2 Lista de Exclusão Fechada"):
    st.write("Vedados: estacionamentos rotativos puros, depósitos de sucata, templos religiosos, sedes partidárias e outdoors.")
with st.expander("1.3 Certificação Anual e Reversão"):
    st.write("A Prefeitura tem direito de vistoria. Constatado descumprimento, o benefício é cassado e cobrado como Dívida Ativa.")
with st.expander("1.4 Gatilho de Revisão Quinquenal"):
    st.write("Nenhum incentivo opera em caráter perpétuo. Revisão a cada 5 anos.")

st.divider()

# ---------------- SECÇÃO 2: FLUXO DO INSTRUMENTO ----------------
st.header("2. Fluxo do Instrumento")
col1, col2, col3, col4 = st.columns(4)
col1.error("📄 1. Notificação\n(IPTU progressivo)")
col2.warning("🔨 2. Leilão Saneado")
col3.info("💻 3. Seleção da Trilha")
col4.success("📈 4. Escada de Isenção")
st.caption("Ao arrematar o imóvel, o investidor seleciona a trilha no sistema Reconverte. O sistema calcula a isenção da obra automaticamente.")

st.divider()

# ---------------- SECÇÃO 3: TRILHAS SETORIAIS ----------------
st.header("3. Matriz de Trilhas Setoriais")
tab1, tab2, tab3, tab4 = st.tabs(["🛒 Varejo & Ind.", "🏥 Saúde", "🎓 Educação", "🏠 Habitação"])

with tab1:
    st.subheader("Varejo, Indústria Leve e Logística")
    st.markdown("- **Isenção na Obra:** Até 3 anos.\n- **Isenção Pós-Obra:** 6 anos.\n- **Extra:** Isenção de alvará e TCL por 3 anos.")
with tab2:
    st.subheader("Saúde")
    st.markdown("- **Isenção na Obra:** Até 5 anos (Anvisa).\n- **Isenção Pós-Obra:** 8 anos.\n- **Contrapartida:** 10% da capacidade para o SUS via Sisreg.")
with tab3:
    st.subheader("Educação")
    st.markdown("- **Isenção na Obra:** Até 3 anos.\n- **Isenção Pós-Obra:** 6 anos + Desconto fixo permanente de 30%.\n- **Contrapartida:** 10% de bolsas (CadÚnico).")
with tab4:
    st.subheader("Habitação")
    st.markdown("- **Isenção na Obra:** Até 3 anos.\n- **Isenção Pós-Obra:** 6 anos.\n- **Contrapartida:** 20% das unidades para Locação Social.")

st.divider()

# ---------------- SECÇÃO 4: SIMULADOR FISCAL INTERATIVO ----------------
st.header("4. Simulador de Evolução do IPTU")
st.write("Simule como a escada de isenção afeta o valor do IPTU do investidor após o Habite-se.")

col_input, col_chart = st.columns([1, 1])

with col_input:
    iptu_base = st.number_input("IPTU Base (R$) - Antes da Obra", value=10000, step=1000)
    iptu_novo = st.number_input("IPTU Cheio (R$) - Pós-Retrofit", value=50000, step=1000)
    trilha = st.selectbox("Escolha a Trilha:", ["Varejo/Indústria", "Saúde", "Educação", "Habitação"])

with col_chart:
    incremental = iptu_novo - iptu_base
    anos = list(range(1, 13))
    pagamentos = []
    
    for ano in anos:
        if ano <= 6:
            taxa = 0.0
        elif ano in [7, 8]:
            taxa = 0.0 if trilha == "Saúde" else 0.25
        elif ano in [9, 10]:
            taxa = 0.25 if trilha == "Saúde" else 0.50
        else:
            if trilha == "Educação":
                iptu_final = iptu_novo * 0.70
                pagamentos.append(iptu_final)
                continue
            else:
                taxa = 1.0
        
        valor_pago = iptu_base + (incremental * taxa)
        pagamentos.append(valor_pago)
        
    df_grafico = pd.DataFrame({"Ano pós-Habite-se": anos, "Valor do IPTU a Pagar (R$)": pagamentos})
    df_grafico.set_index("Ano pós-Habite-se", inplace=True)
    
    st.bar_chart(df_grafico, color="#1B3A5C")
    st.caption(f"Projeção em reais (R$) para a trilha de **{trilha}**.")

st.divider()

# ---------------- SECÇÃO 5: JUSTIFICATIVAS TÉCNICAS ----------------
st.header("5. Justificativa Técnica dos Prazos")
df_just = pd.DataFrame({
    "Trilha": ["Varejo/Indústria", "Saúde", "Educação", "Habitação"],
    "Prazo": ["6 anos", "8 anos", "Permanente*", "6 anos"],
    "Por Quê": [
        "Retrofit comercial é rápido. Dá fôlego frente ao e-commerce.",
        "Ciclo de retorno mais longo. Equipamentos de alto custo.",
        "Desconto condicionado à manutenção da nota no MEC.",
        "Tempo de absorção do mercado imobiliário para vendas."
    ]
})
st.dataframe(df_just, hide_index=True, use_container_width=True)
