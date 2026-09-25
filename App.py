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
    .card-box { background-color: #1E2229; padding: 15px; border-radius: 10px; border-left: 5px solid #1B3A5C; margin-bottom: 15px; }
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
col1.error("📄 **1. Notificação**\n\nIPTU progressivo (6 meses)")
col2.warning("🔨 **2. Leilão Saneado**\n\nAquisição do ativo")
col3.info("💻 **3. Seleção da Trilha**\n\nNo sistema Reconverte")
col4.success("📈 **4. Escada de Isenção**\n\nInício pós-Habite-se")
st.caption("Ao arrematar o imóvel, o investidor seleciona a trilha no sistema Reconverte e o benefício é calculado automaticamente.")

st.divider()

# ---------------- SECÇÃO 3: TRILHAS SETORIAIS ----------------
st.header("3. Matriz de Trilhas Setoriais")
tab1, tab2, tab3, tab4 = st.tabs(["🛒 Varejo & Indústria", "🏥 Saúde", "🎓 Educação", "🏠 Habitação"])

with tab1:
    st.subheader("🛒 Varejo, Indústria Leve e Logística")
    c1, c2, c3 = st.columns(3)
    c1.metric("🏗️ Isenção na Obra", "Até 3 Anos")
    c2.metric("📉 Escada Incremental", "6 Anos")
    c3.metric("🎁 Benefício Extra", "Alvará + TCL Isentos (3 yrs)")
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

# ---------------- SECÇÃO 4: SIMULADOR FISCAL DINÂMICO ----------------
st.header("4. Simulador de Economia Fiscal")
st.write("Ajuste os valores abaixo para calcular a economia de caixa gerada pelo programa.")

# Painel de Controle (Inputs interativos)
c_in1, c_in2, c_in3 = st.columns([1, 1, 1])

with c_in1:
    iptu_base = st.slider("IPTU Atual (Base - R$):", min_value=1000, max_value=100000, value=10000, step=1000)

with c_in2:
    iptu_novo = st.slider("IPTU Estimado Pós-Obra (R$):", min_value=iptu_base, max_value=300000, value=50000, step=5000)

with c_in3:
    trilha = st.selectbox("Selecione a Trilha Setorial:", ["Varejo/Indústria", "Saúde", "Educação", "Habitação"])

# Lógica dos Cálculos
incremental = iptu_novo - iptu_base
anos = list(range(1, 11))
pagamento_com = []
pagamento_sem = []

for ano in anos:
    pagamento_sem.append(iptu_novo)
    
    if ano <= 6:
        taxa = 0.0
    elif ano in [7, 8]:
        taxa = 0.0 if trilha == "Saúde" else 0.25
    elif ano in [9, 10]:
        taxa = 0.25 if trilha == "Saúde" else 0.50
    else:
        taxa = 1.0
        
    valor_pago = iptu_base + (incremental * taxa)
    pagamento_com.append(valor_pago)

total_sem_beneficio = sum(pagamento_sem)
total_com_beneficio = sum(pagamento_com)
economia_total = total_sem_beneficio - total_com_beneficio
pct_economia = (economia_total / total_sem_beneficio) * 100

# Exibição das Métricas de Destaque (KPIs)
m1, m2, m3 = st.columns(3)
m1.metric("💰 Economia Total (10 Anos)", f"R$ {economia_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
m2.metric("📉 Desconto Efetivo Acumulado", f"{pct_economia:.1f}%")
m3.metric("💳 Paga com Benefício", f"R$ {total_com_beneficio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.subheader("📊 Comparativo Anual do IPTU a Pagar (R$)")

# Criando tabela comparativa para o gráfico
df_grafico = pd.DataFrame({
    "Ano": [f"Ano {a}" for a in anos],
    "Com Recupere Rio": pagamento_com,
    "Sem Benefício (Cheio)": pagamento_sem
})
df_grafico.set_index("Ano", inplace=True)

# Gráfico de barras comparativo
st.bar_chart(df_grafico, color=["#1B3A5C", "#A9B7C6"])
st.caption("🟦 **Com Recupere Rio** vs ⬜ **Sem Benefício**: O espaço entre as barras representa o dinheiro economizado pelo investidor.")

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
