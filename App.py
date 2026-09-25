import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ============================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Projeto Recupere Rio — Simulador Técnico",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---- Paleta de Cores Institucionais de Alto Contraste ----
NAVY = "#1B3A5C"
GOLD = "#B8892F"
VERDE = "#15803D"
VERMELHO = "#B42318"
TXT_DARK = "#0F172A"
TXT_MUTED = "#475569"
BORDER_COLOR = "#CBD5E1"
BG_CARD = "#F8FAFC"

st.markdown(f"""
    <style>
    /* Força Fundo Branco Global */
    .stApp {{
        background-color: #FFFFFF !important;
        color: {TXT_DARK} !important;
    }}
    
    /* Oculta Sidebar completamente */
    [data-testid="stSidebar"] {{ display: none !important; }}

    /* Correção Global de Cores de Texto */
    p, span, div, label, h1, h2, h3, h4, h5, h6, li {{
        color: {TXT_DARK} !important;
    }}

    /* FIX DEFINITIVO PARA DROPDOWNS / SELECTBOX (OPÇÕES TOTALMENTE VISÍVEIS) */
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"], div[role="listbox"] {{
        background-color: #FFFFFF !important;
        border: 2px solid {NAVY} !important;
        border-radius: 8px !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.15) !important;
    }}
    div[role="option"], li[data-baseweb="option"] {{
        background-color: #FFFFFF !important;
        color: {TXT_DARK} !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 10px 14px !important;
    }}
    div[role="option"] *, li[data-baseweb="option"] * {{
        color: {TXT_DARK} !important;
        background-color: transparent !important;
    }}
    div[role="option"]:hover, li[data-baseweb="option"]:hover, 
    div[role="option"][aria-selected="true"], li[data-baseweb="option"][aria-selected="true"] {{
        background-color: #E2E8F0 !important;
        color: {NAVY} !important;
    }}
    div[data-baseweb="select"] > div {{
        background-color: #F8FAFC !important;
        border: 1.5px solid {BORDER_COLOR} !important;
        border-radius: 8px !important;
    }}
    div[data-baseweb="select"] * {{
        color: {TXT_DARK} !important;
        font-weight: 600 !important;
    }}

    /* CAPÍTULOS DESTAQUE E CENTRALIZADOS */
    .capitulo-box {{
        text-align: center;
        background: linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 100%);
        border-top: 3px solid {NAVY};
        border-bottom: 3px solid {GOLD};
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 35px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}
    .capitulo-title {{
        color: {NAVY} !important;
        font-size: 19px !important;
        font-weight: 800 !important;
        letter-spacing: 0.8px;
        margin: 0 !important;
        text-transform: uppercase;
    }}

    /* CABEÇALHO OFICIAL */
    .gov-badge {{
        background: linear-gradient(135deg, #002147 0%, #244B72 100%);
        border: 1.5px solid {GOLD};
        border-radius: 12px;
        padding: 22px 18px;
        text-align: center;
        margin-bottom: 22px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }}
    .gov-header-top {{
        color: {GOLD} !important; font-size: 11px; font-weight: 800; letter-spacing: 2px;
        text-transform: uppercase; margin-bottom: 6px;
    }}
    .main-title {{ color: #FFFFFF !important; font-size: 26px; font-weight: 800; margin-bottom: 4px; }}
    .sub-title {{ color: #DCE6F0 !important; font-size: 14px; }}
    .proto-tag {{
        display: inline-block; margin-top: 10px; background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.4); color: #F1F5F9 !important; font-size: 11px; font-weight: 600;
        padding: 4px 12px; border-radius: 20px;
    }}

    /* CARTÕES DA MATRIZ SETORIAL (SEÇÃO 3) */
    .trilha-card-container {{
        background-color: {BG_CARD};
        border: 1.5px solid {BORDER_COLOR};
        border-radius: 12px;
        padding: 18px;
        margin-top: 10px;
        margin-bottom: 15px;
    }}
    .trilha-item-box {{
        background: #FFFFFF;
        border-left: 4px solid {NAVY};
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        border: 1px solid {BORDER_COLOR};
    }}
    .trilha-item-label {{
        color: {TXT_MUTED} !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        margin-bottom: 2px;
    }}
    .trilha-item-value {{
        color: {NAVY} !important;
        font-size: 15px !important;
        font-weight: 700 !important;
    }}

    /* CARTÕES DE MÉTRICA DO SIMULADOR */
    .metric-card {{
        background: {BG_CARD}; border-radius: 10px; padding: 14px; text-align: center;
        border: 1.5px solid {BORDER_COLOR}; margin-bottom: 10px;
    }}
    .metric-val {{ font-size: 23px; font-weight: 800; }}
    .metric-lbl {{ color: {TXT_MUTED} !important; font-size: 12px; font-weight: 600; margin-top: 3px; }}

    /* LINHA INFORMATIVA */
    .info-line {{
        background: #F1F5F9; border: 1px solid {BORDER_COLOR}; border-radius: 8px;
        padding: 12px 16px; font-size: 13.5px; color: {NAVY} !important; margin-top: 10px;
    }}

    div[data-testid="stExpander"] {{
        background-color: {BG_CARD} !important;
        border: 1px solid {BORDER_COLOR} !important;
        border-radius: 8px !important;
    }}
    </style>
""", unsafe_allow_html=True)


def fmt_moeda(val):
    if val is None: return "R$ 0"
    v = round(val)
    return f"R$ {v:,.0f}".replace(",", ".")


def fmt_num(val):
    if val is None: return "0"
    v = round(val)
    return f"{v:,.0f}".replace(",", ".")


# ============================================================
# 2. DADOS CENTRAIS DAS TRILHAS
# ============================================================
def pct_para_ano(ano, escada):
    for ano_max, pct in escada:
        if ano <= ano_max:
            return pct
    return escada[-1][1]


ESCADA_PADRAO = [(6, 0), (8, 25), (10, 50), (999, 100)]
ESCADA_SAUDE = [(8, 0), (9, 25), (10, 50), (999, 100)]
ESCADA_EDUCACAO = [(6, 0), (8, 25), (10, 50), (999, 70)]

TRILHAS = {
    "Varejo, Indústria e Logística": {
        "emoji": "🛒", "obra": 3, "escada": ESCADA_PADRAO,
        "emprego_m2": 25, "faturamento_m2": 6000,
        "extra": "Isenção de 3 anos em alvará, licenciamento e TCL.",
        "contrapartida": "Cota de contratação local pontua como critério no leilão saneado.",
        "justificativa": "Retrofit comercial é rápido (6 a 18 meses de obra) e a receita amadurece logo após abrir. Seis anos dá fôlego frente ao e-commerce sem virar vantagem permanente.",
    },
    "Saúde": {
        "emoji": "🏥", "obra": 5, "escada": ESCADA_SAUDE,
        "emprego_m2": 20, "faturamento_m2": 8000,
        "extra": "Prazo de obra estendido de até 5 anos devido a exigências regulatórias da Anvisa.",
        "contrapartida": "10% da capacidade de exames de alta complexidade e consultas para o SUS (Sisreg).",
        "justificativa": "Exigência da Anvisa (gases medicinais, subestação dedicada) alonga genuinamente o prazo de obra. O retorno é mais longo por conta dos equipamentos e credenciamento de convênios.",
    },
    "Educação": {
        "emoji": "🎓", "obra": 3, "escada": ESCADA_EDUCACAO,
        "emprego_m2": 45, "faturamento_m2": 3500,
        "extra": "Após o ano 10, desconto fixo permanente de 30% sobre o IPTU total (revisado a cada 5 anos).",
        "contrapartida": "10% das vagas em bolsas de estudo integrais via CadÚnico.",
        "justificativa": "Muda de natureza após o ano 10: deixa de ser sobre recuperar custo de obra e passa a desconto condicionado à manutenção da nota no MEC.",
    },
    "Habitação": {
        "emoji": "🏠", "obra": 3, "escada": ESCADA_PADRAO,
        "emprego_m2": 200, "faturamento_m2": None,
        "extra": "20% de bônus de potencial construtivo adicional via Operação Interligada.",
        "contrapartida": "20% das unidades residenciais destinadas à Locação Social por 30 anos.",
        "justificativa": "Não é sobre tempo de obra — é sobre o tempo de absorção do mercado para comercializar as unidades residenciais na planta (Reviver Centro).",
    },
}

ALIQUOTA_IPTU = 0.025          # 2,5% a.a.
ALIQUOTA_INDIRETA = 0.05       # 5% ISS/ICMS
ALIQUOTA_ITBI = 0.03           # 3% ITBI

# ============================================================
# 3. CABEÇALHO OFICIAL
# ============================================================
st.markdown("""
<div class="gov-badge">
    <div class="gov-header-top">Prefeitura da Cidade do Rio de Janeiro · Reconversão Funcional de Ativos</div>
    <div class="main-title">PROJETO RECUPERE RIO</div>
    <div class="sub-title">Simulador de Trilhas Setoriais, Incentivo Fiscal e Impacto Econômico</div>
    <div class="proto-tag">🛠️ Simulação técnica em desenvolvimento — sem caráter oficial</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CAPÍTULO 1: DIRETRIZES GERAIS
# ============================================================
st.markdown("""
<div class="capitulo-box">
    <div class="capitulo-title">1. Diretrizes Gerais e Salvaguardas Operacionais</div>
</div>
""", unsafe_allow_html=True)

with st.expander("1.1 Teste de Enquadramento Funcional (Regra 70/50)", expanded=True):
    st.write("O investidor só mantém o regime se comprovar anualmente que no mínimo **70% da área construída** e **50% do faturamento bruto** provêm da atividade setorial declarada.")
with st.expander("1.2 Lista de Exclusão Fechada"):
    st.write("Vedados em qualquer trilha: estacionamentos rotativos puros, depósitos de sucata/ferro-velho, templos religiosos, sedes partidárias e painéis publicitários.")
with st.expander("1.3 Certificação Anual e Reversão Automática"):
    st.write("A Prefeitura tem direito de vistoria sem aviso prévio. Constatado descumprimento, o benefício é cassado e cobrado como Dívida Ativa, corrigido por IPCA-E.")
with st.expander("1.4 Gatilho de Revisão Quinquenal"):
    st.write("Nenhum incentivo opera em caráter perpétuo. Todos os descontos são auditados a cada 5 anos.")
with st.expander("1.5 Fundamentação Quantitativa por Custo de Instalação"):
    st.write("A diferenciação de prazos entre trilhas é sustentada por levantamento de custo de instalação por m² e ciclo de maturação de cada setor.")

# ============================================================
# CAPÍTULO 2: FLUXO DO INSTRUMENTO
# ============================================================
st.markdown("""
<div class="capitulo-box">
    <div class="capitulo-title">2. Fluxo do Instrumento</div>
</div>
""", unsafe_allow_html=True)
st.caption("👇 Toque em qualquer uma das etapas para ver o detalhamento técnico do processo:")

col_f1, col_f2 = st.columns(2)

with col_f1:
    with st.expander("📄 **1. Notificação** *(IPTU Progressivo)*", expanded=False):
        st.write("**O que acontece:** O imóvel subutilizado ou abandonado é notificado pela Prefeitura.")
        st.write("**Prazo:** 6 meses para apresentação de projeto ou início de atividade.")
        st.write("**Consequência:** Aplicação de alíquotas progressivas de IPTU em caso de inércia.")

    with st.expander("🔨 **2. Leilão Saneado** *(Aquisição do Ativo)*", expanded=False):
        st.write("**O que acontece:** O imóvel é levado a leilão público com perdão/saneamento das dívidas tributárias anteriores.")
        st.write("**Vantagem:** O investidor adquire o ativo sem o passivo fiscal histórico.")

with col_f2:
    with st.expander("💻 **3. Seleção da Trilha** *(No Sistema Reconverte)*", expanded=False):
        st.write("**O que acontece:** Ao arrematar, o investidor cadastra o projeto e seleciona a trilha setorial adequada.")
        st.write("**Regra:** Vinculação automática às regras de contrapartida e prazos de isenção durante a obra.")

    with st.expander("📈 **4. Escada de Isenção** *(Início Pós-Habite-se)*", expanded=False):
        st.write("**O que acontece:** A concessão do Habite-se dispara a contagem da escada de benefícios (Anos 1 a 13).")
        st.write("**Acompanhamento:** Vistoria anual da regra 70/50 para manutenção dos descontos.")

# ============================================================
# CAPÍTULO 3: MATRIZ DE TRILHAS SETORIAIS (REFORMULADO E DESTACADO)
# ============================================================
st.markdown("""
<div class="capitulo-box">
    <div class="capitulo-title">3. Matriz de Trilhas Setoriais</div>
</div>
""", unsafe_allow_html=True)

st.write("Escolha uma trilha abaixo para visualizar as diretrizes e contrapartidas completas (sem texto cortado):")

# Seletor de Trilhas em Destaque
trilha_matriz_sel = st.radio(
    "Selecione a trilha para detalhamento:",
    options=list(TRILHAS.keys()),
    format_func=lambda x: f"{TRILHAS[x]['emoji']} {x}",
    horizontal=True
)

d_matriz = TRILHAS[trilha_matriz_sel]

# Exibição da Matriz em Cartões Verticais de Largura Total
st.markdown(f"""
<div class="trilha-card-container">
    <div style="color: #1B3A5C; font-size: 20px; font-weight: 800; margin-bottom: 15px;">
        {d_matriz['emoji']} {trilha_matriz_sel}
    </div>
    
    <div class="trilha-item-box">
        <div class="trilha-item-label">🏗️ Isenção na Obra</div>
        <div class="trilha-item-value">Até {d_matriz['obra']} anos de isenção total durante o período de reformas.</div>
    </div>
    
    <div class="trilha-item-box">
        <div class="trilha-item-label">📉 Isenção Total pós-Habite-se</div>
        <div class="trilha-item-value">{d_matriz['escada'][0][0]} anos com 100% de isenção de IPTU após a conclusão da obra.</div>
    </div>
    
    <div class="trilha-item-box">
        <div class="trilha-item-label">🎁 Benefício Extra</div>
        <div class="trilha-item-value">{d_matriz['extra']}</div>
    </div>
    
    <div class="trilha-item-box">
        <div class="trilha-item-label">🤝 Contrapartida Social Obrigatória</div>
        <div class="trilha-item-value">{d_matriz['contrapartida']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CAPÍTULO 4: SIMULADOR DE ENGENHARIA FINANCEIRA
# ============================================================
st.markdown("""
<div class="capitulo-box">
    <div class="capitulo-title">4. Simulador de Engenharia Financeira</div>
</div>
""", unsafe_allow_html=True)

col_in1, col_in2, col_in3 = st.columns([1.2, 1, 1])
with col_in1:
    trilha_sel = st.selectbox("Trilha setorial:", list(TRILHAS.keys()))
with col_in2:
    tamanho_m2 = st.slider("Tamanho do imóvel (m²):", min_value=500, max_value=15000, value=3500, step=100)
with col_in3:
    valor_m2 = st.number_input("Valor por m² (R$):", min_value=200, max_value=20000, value=2500, step=100)

t = TRILHAS[trilha_sel]
valor_venal = tamanho_m2 * valor_m2
iptu_integral = valor_venal * ALIQUOTA_IPTU

st.markdown(
    f'<div class="info-line">📐 Valor venal calculado: <b>{fmt_moeda(valor_venal)}</b> &nbsp;·&nbsp; '
    f'IPTU integral anual (2,5%): <b>{fmt_moeda(iptu_integral)}</b> &nbsp;·&nbsp; '
    f'Isenção na obra: <b>até {t["obra"]} anos</b> (antes da escada iniciar no Habite-se).</div>', 
    unsafe_allow_html=True
)
st.write("")

anos = list(range(1, 14))
pagos, sem_beneficio, economias = [], [], []
for ano in anos:
    pct = pct_para_ano(ano, t["escada"])
    pago = iptu_integral * pct / 100
    pagos.append(pago)
    sem_beneficio.append(iptu_integral)
    economias.append(iptu_integral - pago)

tot_pago, tot_sem, tot_econ = sum(pagos), sum(sem_beneficio), sum(economias)

m1, m2, m3 = st.columns(3)
m1.markdown(f'<div class="metric-card" style="border-color:{GOLD};"><div class="metric-val" style="color:{GOLD}">{fmt_moeda(tot_pago)}</div>'
            f'<div class="metric-lbl">Pago em 13 anos</div></div>', unsafe_allow_html=True)
m2.markdown(f'<div class="metric-card" style="border-color:{VERDE};"><div class="metric-val" style="color:{VERDE}">{fmt_moeda(tot_econ)}</div>'
            f'<div class="metric-lbl">Economia vs. cobrança cheia</div></div>', unsafe_allow_html=True)
m3.markdown(f'<div class="metric-card" style="border-color:{VERMELHO};"><div class="metric-val" style="color:{VERMELHO}">{fmt_moeda(tot_sem)}</div>'
            f'<div class="metric-lbl">Quanto pagaria sem o programa</div></div>', unsafe_allow_html=True)

st.write("")
st.subheader("📊 Comparativo Anual de Cobrança (R$)")

# GRÁFICO EMPILHADO (STACKED BAR) - LIMPÍSSIMO PARA TELEMÓVEL
fig = go.Figure()

fig.add_bar(
    x=[f"Ano {a}" for a in anos],
    y=pagos,
    name="IPTU Pago",
    marker_color=GOLD,
    hovertemplate="Ano %{x}<br>IPTU Pago: R$ %{y:,.0f}<extra></extra>"
)

fig.add_bar(
    x=[f"Ano {a}" for a in anos],
    y=economias,
    name="Economia Gerada (Isenção)",
    marker_color=VERDE,
    hovertemplate="Ano %{x}<br>Economia: R$ %{y:,.0f}<extra></extra>"
)

fig.update_layout(
    barmode="stack",
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font=dict(color=TXT_DARK)),
    margin=dict(l=5, r=5, t=10, b=10),
    height=360,
    xaxis=dict(tickfont=dict(color=TXT_DARK)),
    yaxis=dict(gridcolor="#E2E8F0", tickprefix="R$ ", tickfont=dict(color=TXT_DARK))
)

st.plotly_chart(fig, use_container_width=True)
st.caption("💡 **Como ler o gráfico:** A altura total de cada barra é o IPTU cheio. A parte **dourada** é o que o investidor paga e a parte **verde** é o dinheiro economizado pelo programa.")

# Botão de Exportar
relatorio_txt = f"""PROJETO RECUPERE RIO — RELATÓRIO DE SIMULAÇÃO TÉCNICA
------------------------------------------------------------
Trilha Setorial: {trilha_sel}
Área Construída: {fmt_num(tamanho_m2)} m²
Valor por m²: {fmt_moeda(valor_m2)}
Valor Venal Calculado: {fmt_moeda(valor_venal)}
IPTU Integral Anual (2,5%): {fmt_moeda(iptu_integral)}

RESUMO FINANCEIRO (13 ANOS PÓS-HABITE-SE):
------------------------------------------------------------
- Valor Total Pago com Benefício: {fmt_moeda(tot_pago)}
- Economia Total Gerada: {fmt_moeda(tot_econ)}
- Custo sem Programa (IPTU Cheio): {fmt_moeda(tot_sem)}

* Simulação técnica em desenvolvimento — sem caráter oficial.
"""

col_exp1, col_exp2 = st.columns([3, 1])
with col_exp1:
    with st.expander("📋 Ver tabela detalhada ano a ano"):
        df = pd.DataFrame({
            "Ano": [f"Ano {a}" for a in anos],
            "Cobrança (%)": [f"{pct_para_ano(a, t['escada'])}%" for a in anos],
            "IPTU Pago": [fmt_moeda(v) for v in pagos],
            "Sem Benefício (Cheio)": [fmt_moeda(v) for v in sem_beneficio],
            "Economia Gerada": [fmt_moeda(v) for v in economias],
        })
        st.dataframe(df, hide_index=True, use_container_width=True)

with col_exp2:
    st.download_button(
        label="📥 Baixar Simulação (.txt)",
        data=relatorio_txt,
        file_name=f"simulacao_recupere_rio_{trilha_sel.lower().replace(' ', '_')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# ============================================================
# CAPÍTULO 5: IMPACTOS ECONÔMICOS PROJETADOS
# ============================================================
st.markdown("""
<div class="capitulo-box">
    <div class="capitulo-title">5. Impactos Econômicos Projetados</div>
</div>
""", unsafe_allow_html=True)

st.caption("Estimativa ilustrativa a partir de coeficientes médios de mercado — não é uma projeção oficial de arrecadação. "
           "O coeficiente de emprego do Varejo toma como referência o setor de shopping centers (≈1 emprego a cada 17 m² de área bruta locável, ABRASCE/BNB).")

empregos_est = tamanho_m2 / t["emprego_m2"]

i1, i2, i3 = st.columns(3)
i1.markdown(f'<div class="metric-card"><div class="metric-val" style="color:{NAVY}">{fmt_num(empregos_est
