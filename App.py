import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ============================================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS
# ============================================================
st.set_page_config(
    page_title="Projeto Recupere Rio — Simulador Técnico",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Paleta de Cores Institucionais
NAVY = "#1B3A5C"
GOLD = "#B8892F"
VERDE = "#15803D"
AZUL_ROYAL = "#2563EB"
ROXO = "#7C3AED"
VERMELHO = "#B42318"
TXT_DARK = "#0F172A"
TXT_MUTED = "#475569"

css_code = """
    <style>
    .stApp {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    
    [data-testid="stSidebar"] { display: none !important; }

    p, span, div, label, h1, h2, h3, h4, h5, h6, li {
        color: #0F172A !important;
    }

    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"], div[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 2px solid #1B3A5C !important;
        border-radius: 8px !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.15) !important;
    }
    div[role="option"], li[data-baseweb="option"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 10px 14px !important;
    }
    div[role="option"] *, li[data-baseweb="option"] * {
        color: #0F172A !important;
        background-color: transparent !important;
    }
    div[role="option"]:hover, li[data-baseweb="option"]:hover, 
    div[role="option"][aria-selected="true"], li[data-baseweb="option"][aria-selected="true"] {
        background-color: #E2E8F0 !important;
        color: #1B3A5C !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #F8FAFC !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] * {
        color: #0F172A !important;
        font-weight: 600 !important;
    }

    .capitulo-box {
        text-align: center;
        background: linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 100%);
        border-top: 3px solid #1B3A5C;
        border-bottom: 3px solid #B8892F;
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 35px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .capitulo-title {
        color: #1B3A5C !important;
        font-size: 19px !important;
        font-weight: 800 !important;
        letter-spacing: 0.8px;
        margin: 0 !important;
        text-transform: uppercase;
    }

    .gov-badge {
        background: linear-gradient(135deg, #002147 0%, #244B72 100%);
        border: 1.5px solid #B8892F;
        border-radius: 12px;
        padding: 22px 18px;
        text-align: center;
        margin-bottom: 22px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    .gov-header-top {
        color: #B8892F !important; font-size: 11px; font-weight: 800; letter-spacing: 2px;
        text-transform: uppercase; margin-bottom: 6px;
    }
    .main-title { color: #FFFFFF !important; font-size: 26px; font-weight: 800; margin-bottom: 4px; }
    .sub-title { color: #DCE6F0 !important; font-size: 14px; }
    .proto-tag {
        display: inline-block; margin-top: 10px; background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.4); color: #F1F5F9 !important; font-size: 11px; font-weight: 600;
        padding: 4px 12px; border-radius: 20px;
    }

    .trilha-card-container {
        background-color: #F8FAFC;
        border: 1.5px solid #CBD5E1;
        border-radius: 12px;
        padding: 18px;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .trilha-item-box {
        background: #FFFFFF;
        border-left: 4px solid #1B3A5C;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        border: 1px solid #CBD5E1;
    }
    .trilha-item-label {
        color: #475569 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        margin-bottom: 2px;
    }
    .trilha-item-value {
        color: #1B3A5C !important;
        font-size: 15px !important;
        font-weight: 700 !important;
    }

    .metric-card {
        background: #F8FAFC; border-radius: 10px; padding: 14px; text-align: center;
        border: 1.5px solid #CBD5E1; margin-bottom: 10px;
    }
    .metric-val { font-size: 23px; font-weight: 800; }
    .metric-lbl { color: #475569 !important; font-size: 12px; font-weight: 600; margin-top: 3px; }

    .info-line {
        background: #F1F5F9; border: 1px solid #CBD5E1; border-radius: 8px;
        padding: 12px 16px; font-size: 13.5px; color: #1B3A5C !important; margin-top: 10px;
    }

    div[data-testid="stExpander"] {
        background-color: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    </style>
"""
st.markdown(css_code, unsafe_allow_html=True)


def fmt_moeda(val):
    if val is None:
        return "R$ 0"
    v = round(val)
    return "R$ " + f"{v:,.0f}".replace(",", ".")


def fmt_num(val):
    if val is None:
        return "0"
    v = round(val)
    return f"{v:,.0f}".replace(",", ".")


def render_card(valor, legenda, cor="#1B3A5C"):
    html = f'<div class="metric-card"><div class="metric-val" style="color:{cor};">{valor}</div><div class="metric-lbl">{legenda}</div></div>'
    st.markdown(html, unsafe_allow_html=True)


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
        "iss_pct": 0.02, "icms_pct": 0.03, "itbi_pct": 0.0,
        "extra": "Isenção de 3 anos em alvará, licenciamento e TCL.",
        "contrapartida": "Cota de contratação local pontua como critério no leilão saneado.",
        "justificativa": "Retrofit comercial rápido (6 a 18 meses). Seis anos dá fôlego frente ao e-commerce sem virar vantagem permanente.",
    },
    "Saúde": {
        "emoji": "🏥", "obra": 5, "escada": ESCADA_SAUDE,
        "emprego_m2": 20, "faturamento_m2": 8000,
        "iss_pct": 0.04, "icms_pct": 0.01, "itbi_pct": 0.0,
        "extra": "Prazo de obra estendido de até 5 anos devido a normas da Anvisa.",
        "contrapartida": "10% da capacidade de exames e consultas para o SUS (Sisreg).",
        "justificativa": "Exigência da Anvisa (gases medicinais, subestação dedicada) alonga o prazo de obra. Retorno longo por equipamentos e convênios.",
    },
    "Educação": {
        "emoji": "🎓", "obra": 3, "escada": ESCADA_EDUCACAO,
        "emprego_m2": 45, "faturamento_m2": 3500,
        "iss_pct": 0.045, "icms_pct": 0.005, "itbi_pct": 0.0,
        "extra": "Após o ano 10, desconto permanente de 30% sobre o IPTU total (revisado a cada 5 anos).",
        "contrapartida": "10% das vagas em bolsas de estudo integrais via CadÚnico.",
        "justificativa": "Muda de natureza após o ano 10: desconto condicionado à manutenção da nota no MEC.",
    },
    "Habitação": {
        "emoji": "🏠", "obra": 3, "escada": ESCADA_PADRAO,
        "emprego_m2": 200, "faturamento_m2": None,
        "iss_pct": 0.0, "icms_pct": 0.0, "itbi_pct": 0.03,
        "extra": "20% de bônus de potencial construtivo adicional via Operação Interligada.",
        "contrapartida": "20% das unidades residenciais destinadas à Locação Social por 30 anos.",
        "justificativa": "Tempo de absorção do mercado para comercializar as unidades residenciais na planta (Reviver Centro).",
    },
}

ALIQUOTA_IPTU = 0.025          # 2,5% a.a.

# ============================================================
# 3. CABEÇALHO OFICIAL
# ============================================================
gov_badge_html = """
<div class="gov-badge">
    <div class="gov-header-top">Prefeitura da Cidade do Rio de Janeiro · Reconversão Funcional de Ativos</div>
    <div class="main-title">PROJETO RECUPERE RIO</div>
    <div class="sub-title">Simulador de Trilhas Setoriais, Incentivo Fiscal e Impacto Econômico</div>
    <div class="proto-tag">🛠️ Simulação técnica em desenvolvimento — sem caráter oficial</div>
</div>
"""
st.markdown(gov_badge_html, unsafe_allow_html=True)

# ============================================================
# CAPÍTULO 1: DIRETRIZES GERAIS
# ============================================================
cap1_html = """
<div class="capitulo-box">
    <div class="capitulo-title">1. Diretrizes Gerais e Salvaguardas Operacionais</div>
</div>
"""
st.markdown(cap1_html, unsafe_allow_html=True)

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
cap2_html = """
<div class="capitulo-box">
    <div class="capitulo-title">2. Fluxo do Instrumento</div>
</div>
"""
st.markdown(cap2_html, unsafe_allow_html=True)
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
# CAPÍTULO 3: MATRIZ DE TRILHAS SETORIAIS
# ============================================================
cap3_html = """
<div class="capitulo-box">
    <div class="capitulo-title">3. Matriz de Trilhas Setoriais</div>
</div>
"""
st.markdown(cap3_html, unsafe_allow_html=True)

st.write("Escolha uma trilha abaixo para visualizar as diretrizes e contrapartidas completas:")

trilha_matriz_sel = st.radio(
    "Selecione a trilha para detalhamento:",
    options=list(TRILHAS.keys()),
    format_func=lambda x: TRILHAS[x]["emoji"] + " " + x,
    horizontal=True
)

d_matriz = TRILHAS[trilha_matriz_sel]

card_matriz_html = f"""
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
"""
st.markdown(card_matriz_html, unsafe_allow_html=True)

# ============================================================
# CAPÍTULO 4: SIMULADOR DE ENGENHARIA FINANCEIRA
# ============================================================
cap4_html = """
<div class="capitulo-box">
    <div class="capitulo-title">4. Simulador de Engenharia Financeira</div>
</div>
"""
st.markdown(cap4_html, unsafe_allow_html=True)

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

info_line_html = f'<div class="info-line">📐 Valor venal calculado: <b>{fmt_moeda(valor_venal)}</b> &nbsp;·&nbsp; IPTU integral anual (2,5%): <b>{fmt_moeda(iptu_integral)}</b> &nbsp;·&nbsp; Isenção na obra: <b>até {t["obra"]} anos</b> (antes da escada iniciar no Habite-se).</div>'
st.markdown(info_line_html, unsafe_allow_html=True)
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
with m1:
    render_card(fmt_moeda(tot_pago), "Pago em 13 anos", GOLD)
with m2:
    render_card(fmt_moeda(tot_econ), "Economia vs. cobrança cheia", VERDE)
with m3:
    render_card(fmt_moeda(tot_sem), "Quanto pagaria sem o programa", VERMELHO)

st.write("")
st.subheader("📊 Comparativo Anual de Cobrança de IPTU (R$)")

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
st.caption("💡 **Como ler o gráfico:** A altura total de cada barra é o IPTU cheio. A parte **dourada** é o IPTU pago e a parte **verde** é a economia concedida pelo programa.")

col_exp1, col_exp2 = st.columns([3, 1])
with col_exp1:
    with st.expander("📋 Ver tabela detalhada ano a ano"):
        df_anos = pd.DataFrame({
            "Ano": [f"Ano {a}" for a in anos],
            "Cobrança (%)": [f"{pct_para_ano(a, t['escada'])}%" for a in anos],
            "IPTU Pago": [fmt_moeda(v) for v in pagos],
            "Sem Benefício (Cheio)": [fmt_moeda(v) for v in sem_beneficio],
            "Economia Gerada": [fmt_moeda(v) for v in economias],
        })
        st.dataframe(df_anos, hide_index=True, use_container_width=True)

with col_exp2:
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

* Simulação técnica em desenvolvimento — sem caráter oficial."""
    
    st.download_button(
        label="📥 Baixar Simulação (.txt)",
        data=relatorio_txt,
        file_name=f"simulacao_recupere_rio_{trilha_sel.lower().replace(' ', '_')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# ============================================================
# ============================================================
# CAPÍTULO 5: IMPACTOS ECONÔMICOS PROJETADOS
# ============================================================
cap5_html = """
<div class="capitulo-box">
    <div class="capitulo-title">5. Impactos Econômicos Projetados</div>
</div>
"""
st.markdown(cap5_html, unsafe_allow_html=True)

st.caption("Estimativa ilustrativa a partir de coeficientes médios de mercado — não é uma projeção oficial de arrecadação. O coeficiente de emprego do Varejo toma como referência o setor de shopping centers (≈1 emprego a cada 17 m² de área bruta locável, ABRASCE/BNB).")

empregos_est = tamanho_m2 / t["emprego_m2"]

# Cálculos de impostos específicos por trilha
if t["faturamento_m2"] is not None:
    faturamento_est = tamanho_m2 * t["faturamento_m2"]
    iss_est = faturamento_est * t["iss_pct"]
    icms_est = faturamento_est * t["icms_pct"]
    itbi_est = 0
    impostos_indiretos_totais = iss_est + icms_est
    
    i1, i2, i3 = st.columns(3)
    with i1:
        render_card(fmt_num(empregos_est), "Empregos estimados gerados", NAVY)
    with i2:
        render_card(fmt_moeda(faturamento_est), "Faturamento anual estimado", NAVY)
    with i3:
        render_card(fmt_moeda(impostos_indiretos_totais), "Impostos indiretos estimados/ano (ISS + ICMS)", NAVY)
else:
    faturamento_est = 0
    iss_est = 0
    icms_est = 0
    itbi_est = valor_venal * t["itbi_pct"]
    impostos_indiretos_totais = itbi_est
    
    i1, i2, i3 = st.columns(3)
    with i1:
        render_card(fmt_num(empregos_est), "Empregos estimados gerados", NAVY)
    with i2:
        render_card(fmt_moeda(itbi_est), "ITBI estimado na comercialização (3%)", NAVY)
    with i3:
        render_card("—", "Habitação gera receita por ITBI e consumo local", TXT_MUTED)

# --- GRÁFICO DE LINHAS 📈 SEPARADO POR IMPOSTO (DO ANO 0 ATÉ A COBRANÇA INTEGRAL) ---
st.write("")
st.subheader("📈 Projeção Detalhada por Imposto (do Ano 0 até a Cobrança Integral)")

# Descobrir o ano em que o IPTU atinge a cobrança integral (100%)
ano_integral = 11
for a in anos:
    if pct_para_ano(a, t["escada"]) == 100:
        ano_integral = a
        break

# Eixo X do Ano 0 até o Ano de cobrança integral
anos_projecao = list(range(0, ano_integral + 1))
eixo_x = [f"Ano {a}" for a in anos_projecao]

# Linhas de valores por imposto
iptu_proj = [0] + [pagos[a - 1] for a in range(1, ano_integral + 1)]

fig_imp = go.Figure()

# 1. Linha do IPTU Pago (Dourado)
fig_imp.add_trace(go.Scatter(
    x=eixo_x,
    y=iptu_proj,
    mode="lines+markers",
    name="IPTU Arrecadado (com Isenção)",
    line=dict(color=GOLD, width=4, shape="spline"),
    marker=dict(size=8, color=GOLD),
    hovertemplate="%{x}<br>IPTU Pago: R$ %{y:,.0f}/ano<extra></extra>"
))

if t["faturamento_m2"] is not None:
    # 2. Linha do ISS (Azul Royal)
    iss_proj = [0] + [iss_est for _ in range(1, ano_integral + 1)]
    fig_imp.add_trace(go.Scatter(
        x=eixo_x,
        y=iss_proj,
        mode="lines+markers",
        name="ISS (Imposto Sobre Serviços)",
        line=dict(color=AZUL_ROYAL, width=4, shape="spline"),
        marker=dict(size=8, color=AZUL_ROYAL),
        hovertemplate="%{x}<br>ISS: R$ %{y:,.0f}/ano<extra></extra>"
    ))

    # 3. Linha do ICMS (Verde)
    icms_proj = [0] + [icms_est for _ in range(1, ano_integral + 1)]
    fig_imp.add_trace(go.Scatter(
        x=eixo_x,
        y=icms_proj,
        mode="lines+markers",
        name="ICMS (Retorno de VAF)",
        line=dict(color=VERDE, width=4, shape="spline"),
        marker=dict(size=8, color=VERDE),
        hovertemplate="%{x}<br>ICMS (VAF): R$ %{y:,.0f}/ano<extra></extra>"
    ))
else:
    # Trilha Habitação: Linha do ITBI (no Ano 1 da venda)
    itbi_proj = [0, itbi_est] + [0 for _ in range(2, ano_integral + 1)]
    fig_imp.add_trace(go.Scatter(
        x=eixo_x,
        y=itbi_proj,
        mode="lines+markers",
        name="ITBI (Comercialização Inicial)",
        line=dict(color=VERDE, width=4, shape="spline"),
        marker=dict(size=8, color=VERDE),
        hovertemplate="%{x}<br>ITBI: R$ %{y:,.0f}<extra></extra>"
    ))

fig_imp.update_layout(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font=dict(color=TXT_DARK)),
    margin=dict(l=5, r=5, t=10, b=10),
    height=400,
    xaxis=dict(tickfont=dict(color=TXT_DARK), showgrid=True, gridcolor="#F1F5F9"),
    yaxis=dict(gridcolor="#E2E8F0", tickprefix="R$ ", tickfont=dict(color=TXT_DARK))
)

st.plotly_chart(fig_imp, use_container_width=True)
st.caption(f"💡 **Análise de Balanço Fiscal:** No **Ano 0** (fase de reformas), todas as arrecadações partem do ponto zero R$ 0. A partir do **Ano 1** (operação), os tributos indiretos entram em vigor de forma contínua, enquanto o **IPTU (linha dourada)** evolui gradualmente até atingir a cobrança integral (100%) no **Ano {ano_integral}**.")

st.write("")
msg_info = "💡 **Fundamentação Técnica desta Trilha:** " + str(t["justificativa"])
st.info(msg_info)

# ============================================================
# CAPÍTULO 6: JUSTIFICATIVA TÉCNICA DOS PRAZOS
# ============================================================
cap6_html = """
<div class="capitulo-box">
    <div class="capitulo-title">6. Justificativa Técnica dos Prazos</div>
</div>
"""
st.markdown(cap6_html, unsafe_allow_html=True)

# Tabela HTML para garantir renderização perfeita em dispositivos móveis e desktops
html_justificativa_table = """
<div style="overflow-x: auto; margin-top: 15px; margin-bottom: 20px;">
    <table style="width: 100%; border-collapse: collapse; background-color: #FFFFFF; border: 1.5px solid #CBD5E1; border-radius: 8px; font-size: 14px; text-align: left;">
        <thead style="background-color: #1B3A5C; color: #FFFFFF;">
            <tr>
                <th style="padding: 12px 14px; border: 1px solid #CBD5E1; color: #FFFFFF; font-weight: 700; width: 25%;">Trilha Setorial</th>
                <th style="padding: 12px 14px; border: 1px solid #CBD5E1; color: #FFFFFF; font-weight: 700; width: 18%;">Prazo Adotado</th>
                <th style="padding: 12px 14px; border: 1px solid #CBD5E1; color: #FFFFFF; font-weight: 700;">Fundamentação Técnica e Racional Econômico</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background-color: #F8FAFC;">
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; font-weight: 700; color: #1B3A5C;">Varejo, Indústria e Logística</td>
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; font-weight: 700; color: #B8892F;">6 anos</td>
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; color: #0F172A; line-height: 1.5;">Retrofit comercial é rápido (6 a 18 meses). Seis anos de benefício inicial dá fôlego operacional frente ao e-commerce sem virar subsídio permanente.</td>
            </tr>
            <tr style="background-color: #FFFFFF;">
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; font-weight: 700; color: #1B3A5C;">Saúde (Prazo de Obra)</td>
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; font-weight: 700; color: #B8892F;">Até 5 anos</td>
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; color: #0F172A; line-height: 1.5;">Exigências regulatórias complexas da Anvisa (gases medicinais, subestação dedicada, fluxo sanitário) alongam genuinamente o período de obra sem geração de receita.</td>
            </tr>
            <tr style="background-color: #F8FAFC;">
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; font-weight: 700; color: #1B3A5C;">Saúde (Ciclo Incremental)</td>
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; font-weight: 700; color: #B8892F;">8 anos</td>
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; color: #0F172A; line-height: 1.5;">Ciclo de maturação longo: equipamentos de alta complexidade demandam alto investimento inicial, credenciamento em convênios e tempo de formação da carteira de pacientes.</td>
            </tr>
            <tr style="background-color: #FFFFFF;">
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; font-weight: 700; color: #1B3A5C;">Educação (Ciclo Incremental)</td>
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; font-weight: 700; color: #B8892F;">6 anos</td>
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; color: #0F172A; line-height: 1.5;">Acompanha a lógica construtiva e de amortização do Varejo, cobrindo o período de implantação da instituição.</td>
            </tr>
            <tr style="background-color: #F8FAFC;">
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; font-weight: 700; color: #1B3A5C;">Educação (Fase Pós-Escada)</td>
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; font-weight: 700; color: #B8892F;">Desconto Permanente (30%)*</td>
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; color: #0F172A; line-height: 1.5;">Muda de natureza após o Ano 10: deixa de ser recuperação de custo de obra e torna-se incentivo condicionado à manutenção contínua das notas de excelência no MEC.</td>
            </tr>
            <tr style="background-color: #FFFFFF;">
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; font-weight: 700; color: #1B3A5C;">Habitação (Reviver Centro)</td>
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; font-weight: 700; color: #B8892F;">6 anos</td>
                <td style="padding: 12px 14px; border: 1px solid #CBD5E1; color: #0F172A; line-height: 1.5;">Tempo médio de absorção do mercado imobiliário para comercialização das unidades residenciais na planta e consolidação do adensamento populacional.</td>
            </tr>
        </tbody>
    </table>
</div>
"""

st.markdown(html_justificativa_table, unsafe_allow_html=True)
