import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Projeto Recupere Rio — Portal Oficial",
    layout="wide",
    page_icon="🏛️"
)

# Estilização CSS Institucional — Governo do Estado & Prefeitura do Rio de Janeiro
st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Cabeçalho Institucional do Rio de Janeiro */
    .gov-badge {
        background: linear-gradient(135deg, #002147 0%, #003865 100%);
        border: 1px solid #C5A059;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    .gov-header-top {
        color: #C5A059;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .main-title {
        color: #FFFFFF;
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .sub-title {
        color: #CBD5E1;
        font-size: 15px;
        font-style: italic;
    }
    .sec-title {
        color: #FFFFFF;
        font-size: 22px;
        font-weight: 700;
        border-bottom: 2px solid #C5A059;
        padding-bottom: 6px;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    /* Cartões de Métricas Financeiras */
    .metric-box-econ {
        background-color: #1E293B;
        border: 1.5px solid #22C55E;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .metric-box-pago {
        background-color: #1E293B;
        border: 1.5px solid #C5A059;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .metric-box-sem {
        background-color: #1E293B;
        border: 1.5px solid #475569;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .val-econ { color: #22C55E; font-size: 28px; font-weight: 800; }
    .val-pago { color: #C5A059; font-size: 28px; font-weight: 800; }
    .val-sem { color: #94A3B8; font-size: 28px; font-weight: 800; }
    .lbl-metric { color: #94A3B8; font-size: 13px; font-weight: 600; margin-top: 4px; }
    
    .justificativa-box {
        background-color: #1E293B;
        border-left: 4px solid #C5A059;
        border-radius: 6px;
        padding: 16px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Função para formatar valores no padrão brasileiro com pontos nos milhares
def fmt_moeda(val):
    if val is None: return "R$ 0"
    v = round(val)
    return f"R$ {v:,.0f}".replace(",", ".")

def fmt_num(val):
    if val is None: return "0"
    v = round(val)
    return f"{v:,.0f}".replace(",", ".")

# ---------------- CABEÇALHO OFICIAL ----------------
st.markdown("""
<div class="gov-badge">
    <div class="gov-header-top">ESTADO DO RIO DE JANEIRO • PREFEITURA DA CIDADE DO RIO DE JANEIRO</div>
    <div class="main-title">PROJETO RECUPERE RIO</div>
    <div class="sub-title">Reconversão Funcional de Ativos — Memorial Técnico e Diretrizes de Engenharia Financeira</div>
    <div style="color: #94A3B8; font-size: 12px; margin-top: 8px;">
        Secretaria Municipal de Fazenda e Planejamento • Secretaria de Urbanismo e Desenvolvimento Econômico
    </div>
</div>
""", unsafe_allow_html=True)

st.info("📌 **Documento Oficial de Consolidação Técnica:** Diretrizes e parâmetros de incentivos fiscais para a reocupação de imóveis no Município do Rio de Janeiro.")

# ---------------- SECÇÃO 1: DIRETRIZES GERAIS ----------------
st.markdown('<div class="sec-title">1. Diretrizes Gerais e Salvaguardas Operacionais</div>', unsafe_allow_html=True)

with st.expander("1.1 Teste de Enquadramento Funcional (Regra 70/50)", expanded=True):
    st.write("O investidor só mantém o regime se comprovar anualmente que no mínimo **70% da área construída** e **50% do faturamento bruto** provêm da atividade setorial declarada.")
with st.expander("1.2 Lista de Exclusão Fechada"):
    st.write("Vedados em qualquer trilha: estacionamentos rotativos puros, depósitos de sucata/ferro-velho, templos religiosos, sedes partidárias e painéis publicitários/outdoors.")
with st.expander("1.3 Certificação Anual e Reversão Automática"):
    st.write("A Prefeitura tem direito de vistoria sem aviso prévio. Constatado descumprimento, o benefício é cassado e cobrado como Dívida Ativa corrigida por IPCA-E.")
with st.expander("1.4 Gatilho de Revisão Quinquenal"):
    st.write("Nenhum incentivo tributário opera em caráter perpétuo. Todos os descontos são submetidos a auditoria técnica e econômica a cada 5 anos.")
with st.expander("1.5 Fundamentação Quantitativa por Custo de Instalação"):
    st.write("A diferenciação de prazos entre trilhas é fundamentada em levantamentos de custo de instalação por m² e ciclo de maturação do setor.")

st.divider()

# ---------------- SECÇÃO 2: FLUXO DO INSTRUMENTO ----------------
st.markdown('<div class="sec-title">2. Fluxo do Instrumento</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.error("📄 **1. Notificação**\n\nIPTU progressivo (6 meses)")
col2.warning("🔨 **2. Leilão Saneado**\n\nAquisição do ativo")
col3.info("💻 **3. Seleção da Trilha**\n\nNo sistema Reconverte")
col4.success("📈 **4. Escada de Isenção**\n\nInício pós-Habite-se")
st.caption("Ao arrematar o imóvel no leilão saneado, o investidor seleciona a trilha no sistema Reconverte e a escada fiscal é gerada automaticamente.")

st.divider()

# ---------------- SECÇÃO 3: TRILHAS SETORIAIS ----------------
st.markdown('<div class="sec-title">3. Matriz de Trilhas Setoriais</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🛒 Varejo & Indústria", "🏥 Saúde", "🎓 Educação", "🏠 Habitação"])

with tab1:
    st.subheader("🛒 Varejo, Indústria Leve e Logística")
    c1, c2, c3 = st.columns(3)
    c1.metric("🏗️ Isenção na Obra", "Até 3 Anos")
    c2.metric("📉 Escada Incremental", "6 Anos")
    c3.metric("🎁 Benefício Extra", "Alvará + TCL Isentos (3 anos)")
    st.markdown("**🤝 Contrapartida Social:** Cota de contratação local pontua no leilão saneado.")

with tab2:
    st.subheader("🏥 Saúde")
    c1, c2, c3 = st.columns(3)
    c1.metric("🏗️ Isenção na Obra", "Até 5 Anos", delta="Exigência Anvisa", delta_color="normal")
    c2.metric("📉 Escada Incremental", "8 Anos")
    c3.metric("🤝 Contrapartida", "10% Capacidade SUS")
    st.markdown("**📌 Detalhe:** Destinação de 10% de exames de alta complexidade e consultas para a regulação do SUS (Sisreg).")

with tab3:
    st.subheader("🎓 Educação")
    c1, c2, c3 = st.columns(3)
    c1.metric("🏗️ Isenção na Obra", "Até 3 Anos")
    c2.metric("📉 Escada Incremental", "6 Anos")
    c3.metric("♾️ Benefício Permanente", "30% Desconto Fixado")
    st.markdown("**🤝 Contrapartida Social:** 10% das vagas em bolsas de estudo integrais para moradores no CadÚnico.")

with tab4:
    st.subheader("🏠 Habitação")
    c1, c2, c3 = st.columns(3)
    c1.metric("🏗️ Isenção na Obra", "Até 3 Anos")
    c2.metric("📉 Escada Incremental", "6 Anos")
    c3.metric("🚀 Bônus Construtivo", "+20% Potencial")
    st.markdown("**🤝 Contrapartida Social:** 20% das unidades destinadas à Locação Social por 30 anos.")

st.divider()

# ---------------- SECÇÃO 4: MODELAGEM FISCAL E SIMULADOR HÍBRIDO ----------------
st.markdown('<div class="sec-title">4. Modelagem Fiscal e Simulador de Engenharia Financeira</div>', unsafe_allow_html=True)
st.write("Ajuste a trilha setorial e o Valor Venal do imóvel após a obra para calcular o impacto financeiro exato ano a ano (Anos 1 a 13).")

# Entradas do Usuário
col_in1, col_in2 = st.columns([1, 1])

with col_in1:
    trilha_sel = st.selectbox(
        "Selecione a Trilha Setorial:",
        ["Varejo / Indústria", "Saúde", "Educação", "Habitação"]
    )

with col_in2:
    valor_venal = st.number_input(
        "Valor Venal do Imóvel pós-obra (R$):",
        value=8800000,
        step=100000,
        format="%d"
    )
    st.caption(f"Valor venal configurado: **{fmt_moeda(valor_venal)}**")

st.caption("Durante a obra, o terreno tem isenção de IPTU por até 3 anos, antes da escada iniciar a contagem a partir do Habite-se.")

# Lógica de Cálculo (Alíquota Comercial de 2,5% ao ano)
iptu_cheio_anual = valor_venal * 0.025
anos = list(range(1, 14))

pct_cobranca = []
val_pago_list = []
val_sem_list = []
val_econ_list = []

for ano in anos:
    val_sem = iptu_cheio_anual
    
    if trilha_sel in ["Varejo / Indústria", "Habitação"]:
        if ano <= 6: pct = 0
        elif ano in [7, 8]: pct = 25
        elif ano in [9, 10]: pct = 50
        else: pct = 100
    elif trilha_sel == "Saúde":
        if ano <= 8: pct = 0
        elif ano in [9, 10]: pct = 25
        elif ano in [11, 12]: pct = 50
        else: pct = 100
    elif trilha_sel == "Educação":
        if ano <= 6: pct = 0
        elif ano in [7, 8]: pct = 25
        elif ano in [9, 10]: pct = 50
        else: pct = 70  # Desconto permanente de 30% (paga 70%)

    val_pago = val_sem * (pct / 100.0)
    val_econ = val_sem - val_pago
    
    pct_cobranca.append(f"{pct}%")
    val_pago_list.append(val_pago)
    val_sem_list.append(val_sem)
    val_econ_list.append(val_econ)

tot_pago = sum(val_pago_list)
tot_sem = sum(val_sem_list)
tot_econ = sum(val_econ_list)

# Cartões de Destaque Financeiro
m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(f'<div class="metric-box-pago"><div class="val-pago">{fmt_moeda(tot_pago)}</div><div class="lbl-metric">Valor Pago Acumulado (13 Anos)</div></div>', unsafe_allow_html=True)

with m2:
    st.markdown(f'<div class="metric-box-econ"><div class="val-econ">{fmt_moeda(tot_econ)}</div><div class="lbl-metric">Economia Total vs. Cobrança Cheia</div></div>', unsafe_allow_html=True)

with m3:
    st.markdown(f'<div class="metric-box-sem"><div class="val-sem">{fmt_moeda(tot_sem)}</div><div class="lbl-metric">Custo sem Programa (IPTU Cheio)</div></div>', unsafe_allow_html=True)

st.write("")

# TABELA DETALHADA ANO A ANO
st.subheader("📋 Tabela Detalhada da Evolução Tributária (Ano a Ano)")

df_exibicao = pd.DataFrame({
    "Ano": [f"Ano {a}" for a in anos],
    "Cobrança (%)": pct_cobranca,
    "IPTU Pago no Ano": [fmt_moeda(v) for v in val_pago_list],
    "IPTU sem Benefício (Cheio)": [fmt_moeda(v) for v in val_sem_list],
    "Economia no Ano": [fmt_moeda(v) for v in val_econ_list]
})

st.table(df_exibicao)

# GRÁFICO COMPARATIVO EM REAIS
st.subheader("📊 Gráfico Comparativo Anual: Pago com Benefício vs. Cobrança Cheia (R$)")

df_chart = pd.DataFrame({
    "Ano": [f"Ano {a}" for a in anos],
    "Com Recupere Rio (Pago)": val_pago_list,
    "Sem Programa (Cobrança Cheia)": val_sem_list
})
df_chart.set_index("Ano", inplace=True)

st.bar_chart(df_chart, color=["#C5A059", "#475569"])
st.caption("🟡 **Com Recupere Rio (Pago)** vs 🔘 **Sem Programa (Cobrança Cheia)**: A diferença entre a barra dourada e a barra cinza representa o alívio financeiro direto para o investidor.")

st.divider()

# ---------------- SECÇÃO 5: JUSTIFICATIVA TÉCNICA DOS PRAZOS ----------------
st.markdown('<div class="sec-title">5. Justificativa Técnica dos Prazos</div>', unsafe_allow_html=True)

df_just = pd.DataFrame({
    "Trilha": ["Varejo / Indústria", "Saúde (obra)", "Saúde (incremental)", "Educação (incremental)", "Educação (pós-escada)", "Habitação"],
    "Prazo Adotado": ["6 anos", "Até 5 anos", "8 anos", "6 anos", "Permanente*", "6 anos"],
    "Fundamentação Técnica e Econômica": [
        "Retrofit comercial é rápido (6 a 18 meses de obra). Seis anos de escada garante fôlego para competir com o e-commerce sem gerar concorrência desleal.",
        "Exigências regulatórias da Anvisa (gases medicinais, subestação elétrica dedicada, blindagem) alongam genuinamente o tempo de obra sem receita.",
        "Ciclo de maturação longo de equipamentos de alta complexidade e credenciamento de redes de convênios.",
        "Mesma lógica construtiva e de amortização do setor de varejo.",
        "Muda de natureza: deixa de ser recuperação de custo de obra e passa a incentivo condicionado à manutenção da nota máxima no MEC.",
        "Tempo de absorção do mercado imobiliário para comercialização das unidades residenciais na planta (alinhado ao Reviver Centro)."
    ]
})
st.dataframe(df_just, hide_index=True, use_container_width=True)

st.warning("⚠️ **Nota de Ajuste de Risco:** O par 5 + 8 anos da trilha Saúde é a premissa menos testada e recomenda-se validação técnica formal com a Secretaria Municipal de Saúde.")
