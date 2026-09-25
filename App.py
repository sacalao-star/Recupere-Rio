import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Projeto Recupere Rio", layout="wide", page_icon="🏙️")

# Estilização CSS customizada
st.markdown("""
    <style>
    .titulo { color: #1B3A5C; font-size: 32px; font-weight: bold; text-align: center; }
    .subtitulo { color: #5C6772; font-size: 18px; font-style: italic; text-align: center; margin-bottom: 20px; }
    .kicker { color: #1B3A5C; font-size: 14px; text-align: center; font-weight: bold; }
    .metric-pago { color: #D15A39; font-size: 26px; font-weight: bold; margin-top: 10px; }
    .metric-econ { color: #2E7D32; font-size: 26px; font-weight: bold; margin-top: 10px; }
    .metric-label { color: #5C6772; font-size: 13px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# Função para formatar valores no padrão com pontos (ex: 8.800.000)
def fmt_moeda(valor):
    return f"R$ {valor:,.0f}".replace(",", ".")

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
col1.error("📄 **1. Notificação**\n\nIPTU progressivo (6 meses)")
col2.warning("🔨 **2. Leilão Saneado**\n\nAquisição do ativo")
col3.info("💻 **3. Seleção da Trilha**\n\nNo sistema Reconverte")
col4.success("📈 **4. Escada de Isenção**\n\nInício pós-Habite-se")
st.caption("Ao arrematar o imóvel, o investidor seleciona a trilha no sistema Reconverte e o benefício é calculated automaticamente.")

st.divider()

# ---------------- SECÇÃO 3: TRILHAS SETORIAIS ----------------
st.header("3. Matriz de Trilhas Setoriais")
tab1, tab2, tab3, tab4 = st.tabs(["🛒 Varejo & Indústria", "🏥 Saúde", "🎓 Educação", "🏠 Habitação"])

with tab1:
    st.subheader("🛒 Varejo, Indústria Leve e Logística")
    c1, c2, c3 = st.columns(3)
    c1.metric("🏗️ Isenção na Obra", "Até 3 Anos")
    c2.metric("📉 Escada Incremental", "6 Anos")
    c3.metric("🎁 Benefício Extra", "Alvará + TCL Isentos (3 anos)")
    st.markdown("**🤝 Contrapartida Social:** Cota de contratação local serve como critério de desempate no leilão.")

with tab2:
    st.subheader("🏥 Saúde")
    c1, c2, c3 = st.columns(3)
    c1.metric("🏗️ Isenção na Obra", "Até 5 Anos", delta="Exigência Anvisa", delta_color="normal")
    c2.metric("📉 Escada Incremental", "8 Anos")
    c3.metric("🤝 Contrapartida", "10% Capacidade SUS")
    st.markdown("**📌 Detalhe:** Destinação de 10% de exames e consultas de alta complexidade para a regulação do SUS (Sisreg).")

with tab3:
    st.subheader("🎓 Educação")
    c1, c2, c3 = st.columns(3)
    c1.metric("🏗️ Isenção na Obra", "Até 3 Anos")
    c2.metric("📉 Escada Incremental", "6 Anos")
    c3.metric("♾️ Benefício Permanente", "30% Desconto Fixado")
    st.markdown("**🤝 Contrapartida Social:** 10% das vagas em bolsas integrais para moradores no CadÚnico.")

with tab4:
    st.subheader("🏠 Habitação")
    c1, c2, c3 = st.columns(3)
    c1.metric("🏗️ Isenção na Obra", "Até 3 Anos")
    c2.metric("📉 Escada Incremental", "6 Anos")
    c3.metric("🚀 Bônus Construtivo", "+20% Potencial")
    st.markdown("**🤝 Contrapartida Social:** 20% das unidades destinadas à Locação Social por 30 anos.")

st.divider()

# ---------------- SECÇÃO 4: SIMULADOR DE COBRANÇA DO IPTU ----------------
st.header("4. Modelagem Fiscal Incremental e Simulador")
st.write("Informe o Valor Venal do imóvel e selecione a trilha para gerar a escada de cobrança detalhada ano a ano (Anos 1 a 13).")

col_sel1, col_sel2 = st.columns([1, 1])

with col_sel1:
    trilha_calc = st.selectbox(
        "Escolha a trilha setorial:",
        ["Varejo / Indústria", "Saúde", "Educação", "Habitação"]
    )

with col_sel2:
    valor_venal = st.number_input(
        "Valor venal do imóvel após a obra (R$)",
        value=8800000,
        step=100000,
        format="%d"
    )
    st.caption(f"Valor inserido: **{fmt_moeda(valor_venal)}**")

st.caption("Durante a obra, o terreno tem isenção de IPTU por até 3 anos, antes desta escada começar a contar (a partir do Habite-se).")

# Alíquota comercial do IPTU: 2.5% ao ano
iptu_cheio_anual = valor_venal * 0.025

anos = list(range(1, 14))
cobranca_pct = []
iptu_pago = []

for ano in anos:
    if ano <= 6:
        pct = 0
    elif ano in [7, 8]:
        pct = 0 if trilha_calc == "Saúde" else 25
    elif ano in [9, 10]:
        pct = 25 if trilha_calc == "Saúde" else 50
    else: # Anos 11, 12, 13
        if trilha_calc == "Educação":
            pct = 70  # 30% de desconto permanente (paga 70%)
        elif trilha_calc == "Saúde" and ano in [11, 12]:
            pct = 50
        else:
            pct = 100
            
    valor_ano = iptu_cheio_anual * (pct / 100.0)
    cobranca_pct.append(f"{pct}%")
    iptu_pago.append(valor_ano)

# Construção da tabela formatada com pontos nos milhares
df_calculadora = pd.DataFrame({
    "Ano": [f"Ano {a}" for a in anos],
    "Cobrança": cobranca_pct,
    "IPTU no ano": [fmt_moeda(v) for v in iptu_pago]
})

st.table(df_calculadora)

# Totais Financeiros
total_pago = sum(iptu_pago)
total_sem_beneficio = iptu_cheio_anual * 13
economia_total = total_sem_beneficio - total_pago

m_col1, m_col2 = st.columns(2)
with m_col1:
    st.markdown(f'<div class="metric-pago">{fmt_moeda(total_pago)}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">pago acumulado em 13 anos</div>', unsafe_allow_html=True)

with m_col2:
    st.markdown(f'<div class="metric-econ">{fmt_moeda(economia_total)}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">economizado vs. cobrança cheia sem programa</div>', unsafe_allow_html=True)

st.divider()

# ---------------- SECÇÃO 5: JUSTIFICATIVAS TÉCNICAS ----------------
st.header("5. Justificativa Técnica dos Prazos")
df_just = pd.DataFrame({
    "Trilha": ["Varejo/Indústria", "Saúde (obra)", "Saúde (incremental)", "Educação (incremental)", "Educação (pós-escada)", "Habitação"],
    "Prazo": ["6 anos", "Até 5 anos", "8 anos", "6 anos", "Permanente*", "6 anos"],
    "Fundamentação Técnica": [
        "Retrofit comercial é rápido. 6 anos dá fôlego frente ao e-commerce sem gerar concorrência desleal.",
        "Exigências da Anvisa (gases, subestação) alongam o tempo real de obra sem receita.",
        "Ciclo de maturação longo de equipamentos de alta complexidade e credenciamento de convênios.",
        "Mesma lógica construtiva e de amortização do varejo.",
        "Muda de natureza: sustentar qualidade testada periodicamente pelo MEC.",
        "Tempo de absorção do mercado imobiliário para comercialização das unidades (Reviver Centro)."
    ]
})
st.dataframe(df_just, hide_index=True, use_container_width=True)

st.warning("⚠️ **Nota de Alerta:** O par 5+8 anos da trilha Saúde é a premissa menos testada e requer validação da Secretaria Municipal de Saúde.")
