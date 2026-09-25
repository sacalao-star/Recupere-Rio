import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ============================================================
# 1. CONFIGURAÇÃO DA PÁGINA (SEM SIDEBAR)
# ============================================================
st.set_page_config(
    page_title="Projeto Recupere Rio — Simulador Técnico",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---- Paleta de Cores de Alto Contraste para Fundo Claro ----
NAVY = "#1B3A5C"
GOLD = "#B8892F"
VERDE = "#15803D"
VERDE_BG = "#EAF6EE"
VERMELHO = "#B42318"
VERMELHO_BG = "#FDEDEB"
TXT_DARK = "#0F172A"
TXT_MUTED = "#475569"
BORDER_COLOR = "#CBD5E1"

st.markdown(f"""
    <style>
    /* Força Fundo Branco e Texto Escuro em Todos os Componentes */
    .stApp {{
        background-color: #FFFFFF !important;
        color: {TXT_DARK} !important;
    }}
    
    /* Remove a barra lateral completamente */
    [data-testid="stSidebar"] {{
        display: none !important;
    }}
    
    /* Correção Global de Cores de Texto */
    p, span, div, label, h1, h2, h3, h4, h5, h6, li {{
        color: {TXT_DARK} !important;
    }}
    
    /* Estilização dos Métricos do Streamlit */
    [data-testid="stMetricValue"] {{
        color: {NAVY} !important;
        font-weight: 800 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {TXT_MUTED} !important;
        font-weight: 600 !important;
    }}

    /* Estilização das Abas (Tabs) */
    button[data-baseweb="tab"] p {{
        color: {NAVY} !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }}

    /* Cabeçalho Oficial */
    .gov-badge {{
        background: linear-gradient(135deg, #002147 0%, #244B72 100%);
        border: 1px solid {GOLD};
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 22px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    .gov-header-top {{
        color: {GOLD} !important; font-size: 11px; font-weight: 800; letter-spacing: 2.5px;
        text-transform: uppercase; margin-bottom: 6px;
    }}
    .main-title {{ color: #FFFFFF !important; font-size: 28px; font-weight: 800; margin-bottom: 4px; }}
    .sub-title {{ color: #DCE6F0 !important; font-size: 14.5px; }}
    .proto-tag {{
        display: inline-block; margin-top: 12px; background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.4); color: #F1F5F9 !important; font-size: 11.5px; font-weight: 600;
        padding: 4px 12px; border-radius: 20px;
    }}
    
    /* Títulos de Seção */
    .sec-title {{
        color: {NAVY} !important; font-size: 21px; font-weight: 700; border-bottom: 2px solid {GOLD};
        padding-bottom: 6px; margin-top: 25px; margin-bottom: 15px;
    }}

    /* Cartões Métrica do Simulador */
    .metric-card {{
        background: #F8FAFC; border-radius: 10px; padding: 16px; text-align: center;
        border: 1.5px solid {BORDER_COLOR};
    }}
    .metric-val {{ font-size: 24px; font-weight: 800; }}
    .metric-lbl {{ color: {TXT_MUTED} !important; font-size: 12px; font-weight: 600; margin-top: 4px; }}

    /* Caixas Informativas */
    .info-line {{
        background: #F1F5F9; border: 1px solid {BORDER_COLOR}; border-radius: 8px;
        padding: 12px 16px; font-size: 13.5px; color: {NAVY} !important; margin-top: 10px;
    }}

    div[data-testid="stExpander"] {{
        background-color: #F8FAFC !important;
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
        "contrapartida": "Cota de contratação local pontua no leilão saneado.",
        "justificativa": "Retrofit comercial é rápido (6 a 18 meses de obra) e a receita amadurece logo após abrir. Seis anos dá fôlego frente ao e-commerce sem virar vantagem permanente.",
    },
    "Saúde": {
        "emoji": "🏥", "obra": 5, "escada": ESCADA_SAUDE,
        "emprego_m2": 20, "faturamento_m2": 8000,
        "extra": "Prazo de obra estendido pela exigência regulatória da Anvisa.",
        "contrapartida": "10% da capacidade de exames de alta complexidade para o SUS (Sisreg).",
        "justificativa": "Exigência da Anvisa (gases medicinais, subestação dedicada) alonga genuinamente o prazo de obra. O retorno é mais longo por conta dos equipamentos e credenciamento de convênios.",
    },
    "Educação": {
        "emoji": "🎓", "obra": 3, "escada": ESCADA_EDUCACAO,
        "emprego_m2": 45, "faturamento_m2": 3500,
        "extra": "Após o ano 10, desconto fixo de 30% sobre o IPTU total (revisado a cada 5 anos).",
        "contrapartida": "10% das vagas em bolsa integral via CadÚnico.",
        "justificativa": "Muda de natureza após o ano 10: deixa de ser sobre recuperar custo de obra e passa a desconto condicionado à manutenção da nota no MEC.",
    },
    "Habitação": {
        "emoji": "🏠", "obra": 3, "escada": ESCADA_PADRAO,
        "emprego_m2": 200, "faturamento_m2": None,
        "extra": "20% de bônus de potencial construtivo via Operação Interligada.",
        "contrapartida": "20% das unidades em Locação Social por 30 anos.",
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
    <div class="main-title">Projeto Recupere Rio</div>
    <div class="sub-title">Simulador de Trilhas Setoriais, Incentivo Fiscal e Impacto Econômico</div>
    <div class="proto-tag">🛠️ Simulação técnica em desenvolvimento — sem caráter oficial</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 4. DIRETRIZES GERAIS
# ============================================================
st.markdown('<div class="sec-title">1. Diretrizes Gerais e Salvaguardas Operacionais</div>', unsafe_allow_html=True)

with st.expander("1.1 Teste de Enquadramento Funcional (Regra 70/50)", expanded=True):
    st.write("O investidor só mantém o regime se comprovar anualmente que no mínimo **70% da área construída** e **50% do faturamento bruto** provêm da atividade setorial declarada.")
with st.expander("1.2 Lista de Exclusão Fechada"):
    st.write("Vedados em qualquer trilha: estacionamentos rotativos puros, depósitos de sucata/ferro-velho, templos religiosos, sedes partidárias e painéis publicitários.")
with st.expander("1.3 Certificação Anual e Reversão Automática"):
    st.write("A Prefeitura tem direito de vistoria sem aviso prévio. Constatado descumprimento, o benefício é cassado e cobrado como Dívida Ativa, corrigido por IPCA-E.")
with st.expander("1.4 Gatilho de Revisão Quinquenal"):
    st.write("Nenhum incentivo opera em caráter perpétuo. Todos os descontos são auditados a cada 5 anos.")
with st.expander("1.5 Fundamentação Quantitativa por Custo de Instalação"):
    st.write("A diferenciação de prazos entre trilhas é sustentada por levantamento de custo de installation por m² e ciclo de maturação de cada setor.")

# ============================================================
# 5. FLUXO DO INSTRUMENTO (CARTÕES INTERATIVOS - CLIQUE PARA VER)
# ============================================================
st.markdown('<div class="sec-title">2. Fluxo do Instrumento</div>', unsafe_allow_html=True)
st.caption("👇 Toque em qualquer uma das etapas do fluxo para ver o detalhamento técnico do processo:")

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
# 6. MATRIZ DE TRILHAS SETORIAIS
# ============================================================
st.markdown('<div class="sec-title">3. Matriz de Trilhas Setoriais</div>', unsafe_allow_html=True)
tabs = st.tabs([f"{d['emoji']} {n}" for n, d in TRILHAS.items()])
for tab, (nome, d) in zip(tabs, TRILHAS.items()):
    with tab:
        st.subheader(f"{d['emoji']} {nome}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Isenção na obra", f"Até {d['obra']} anos")
        c2.metric("Isenção total (100%)", f"{d['escada'][0][0]} anos")
        c3.metric("Benefício extra", d["extra"].split(".")[0])
        st.markdown(f"**🤝 Contrapartida social:** {d['contrapartida']}")

# ============================================================
# 7. SIMULADOR FISCAL
# ============================================================
st.markdown('<div class="sec-title">4. Simulador de Engenharia Financeira</div>', unsafe_allow_html=True)

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

# GRÁFICO EMPILHADO (STACKED BAR) - ULTRA LIMPO PARA TELEMÓVEL
fig = go.Figure()

# Base da barra: O que foi Pago (Dourado)
fig.add_bar(
    x=[f"Ano {a}" for a in anos],
    y=pagos,
    name="IPTU Pago",
    marker_color=GOLD,
    hovertemplate="Ano %{x}<br>IPTU Pago: R$ %{y:,.0f}<extra></extra>"
)

# Topo da barra empilhada: A Economia/Isenção (Verde)
fig.add_bar(
    x=[f"Ano {a}" for a in anos],
    y=economias,
    name="Economia Gerada (Isenção)",
    marker_color=VERDE,
    hovertemplate="Ano %{x}<br>Economia: R$ %{y:,.0f}<extra></extra>"
)

fig.update_layout(
    barmode="stack",  # Empilha as barras para formar o total do IPTU!
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
# 8. IMPACTOS ECONÔMICOS PROJETADOS
# ============================================================
st.markdown('<div class="sec-title">5. Impactos Econômicos Projetados</div>', unsafe_allow_html=True)
st.caption("Estimativa ilustrativa a partir de coeficientes médios de mercado — não é uma projeção oficial de arrecadação. "
           "O coeficiente de emprego do Varejo toma como referência o setor de shopping centers (≈1 emprego a cada 17 m² de área bruta locável, ABRASCE/BNB).")

empregos_est = tamanho_m2 / t["emprego_m2"]

i1, i2, i3 = st.columns(3)
i1.markdown(f'<div class="metric-card"><div class="metric-val" style="color:{NAVY}">{fmt_num(empregos_est)}</div>'
            f'<div class="metric-lbl">Empregos estimados gerados</div></div>', unsafe_allow_html=True)

if t["faturamento_m2"] is not None:
    faturamento_est = tamanho_m2 * t["faturamento_m2"]
    impostos_indiretos = faturamento_est * ALIQUOTA_INDIRETA
    i2.markdown(f'<div class="metric-card"><div class="metric-val" style="color:{NAVY}">{fmt_moeda(faturamento_est)}</div>'
                f'<div class="metric-lbl">Faturamento anual estimado</div></div>', unsafe_allow_html=True)
    i3.markdown(f'<div class="metric-card"><div class="metric-val" style="color:{NAVY}">{fmt_moeda(impostos_indiretos)}</div>'
                f'<div class="metric-lbl">Impostos indiretos estimados/ano (ISS/ICMS via VAF)</div></div>', unsafe_allow_html=True)
else:
    itbi_est = valor_venal * ALIQUOTA_ITBI
    i2.markdown(f'<div class="metric-card"><div class="metric-val" style="color:{NAVY}">{fmt_moeda(itbi_est)}</div>'
                f'<div class="metric-lbl">ITBI estimado na comercialização (3%)</div></div>', unsafe_allow_html=True)
    i3.markdown(f'<div class="metric-card"><div class="metric-val" style="color:{TXT_MUTED}">—</div>'
                f'<div class="metric-lbl">Habitação gera receita por ITBI e consumo local</div></div>', unsafe_allow_html=True)

st.write("")
st.info(f"💡 **Fundamentação Técnica desta Trilha:** {t['justificativa']}")

# ============================================================
# 9. JUSTIFICATIVA TÉCNICA DOS PRAZOS
# ============================================================
st.markdown('<div class="sec-title">6. Justificativa Técnica dos Prazos</div>', unsafe_allow_html=True)
df_just = pd.DataFrame({
    "Trilha": ["Varejo / Indústria", "Saúde (obra)", "Saúde (incremental)", "Educação (incremental)", "Educação (pós-escada)", "Habitação"],
    "Prazo Adotado": ["6 anos", "Até 5 anos", "8 anos", "6 anos", "Permanente*", "6 anos"],
    "Fundamentação Técnica": [
        "Retrofit comercial é rápido (6 a 18 meses). Seis anos dá fôlego frente ao e-commerce sem virar vantagem permanente.",
        "Exigência da Anvisa (gases medicinais, subestação dedicada) alonga genuinamente o prazo de obra sem receita.",
        "Ciclo de maturação longo: equipamento caro, credenciamento de convênios, carteira de pacientes.",
        "Mesma lógica construtiva e de amortização do Varejo.",
        "Muda de natureza: deixa de ser sobre custo de obra e passa a desconto condicionado à manutenção da nota no MEC.",
        "Tempo de absorção do mercado para vender as unidades residenciais na planta (Reviver Centro).",
    ],
})
st.dataframe(df_just, hide_index=True, use_container_width=True)
st.warning("⚠️ **Nota de Ajuste de Risco:** O par 5+8 anos da trilha Saúde é a premissa menos testada — recomenda-se validação técnica formal com a Secretaria Municipal de Saúde.")
