import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ============================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Projeto Recupere Rio — Simulador",
    layout="wide",
    page_icon="🏛️"
)

# ---- Cores centrais (mesma paleta do Memorial Técnico e do simulador HTML) ----
NAVY = "#1B3A5C"
GOLD = "#B8892F"
VERDE = "#15803D"
VERDE_BG = "#EAF6EE"
VERMELHO = "#B42318"
VERMELHO_BG = "#FDEDEB"
CINZA_TXT = "#5C6772"
LINHA = "#E4E1D6"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #FFFFFF; }}
    .block-container {{ padding-top: 1.2rem; max-width: 1100px; }}

    .gov-badge {{
        background: linear-gradient(135deg, {NAVY} 0%, #244B72 100%);
        border-radius: 14px;
        padding: 26px 30px;
        margin-bottom: 22px;
        box-shadow: 0 6px 20px rgba(27,58,92,0.18);
    }}
    .gov-header-top {{
        color: {GOLD}; font-size: 11.5px; font-weight: 700; letter-spacing: 2px;
        text-transform: uppercase; margin-bottom: 8px;
    }}
    .main-title {{ color: #FFFFFF; font-size: 32px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 4px; }}
    .sub-title {{ color: #DCE6F0; font-size: 15px; }}
    .proto-tag {{
        display: inline-block; margin-top: 14px; background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.35); color: #F1F5F9; font-size: 11.5px;
        padding: 4px 10px; border-radius: 20px;
    }}

    .sec-title {{
        color: {NAVY}; font-size: 21px; font-weight: 700; border-bottom: 2px solid {GOLD};
        padding-bottom: 7px; margin-top: 30px; margin-bottom: 14px;
    }}

    .flow-step {{
        background: #F8F9FB; border: 1px solid {LINHA}; border-left: 4px solid {NAVY};
        border-radius: 8px; padding: 12px 14px; height: 100%;
    }}
    .flow-step b {{ color: {NAVY}; }}

    .metric-card {{ border-radius: 12px; padding: 18px; text-align: center; border: 1.5px solid; }}
    .metric-pago {{ background: #FBF7EE; border-color: {GOLD}; }}
    .metric-econ {{ background: {VERDE_BG}; border-color: {VERDE}; }}
    .metric-sem {{ background: {VERMELHO_BG}; border-color: {VERMELHO}; }}
    .metric-val {{ font-size: 26px; font-weight: 800; }}
    .metric-lbl {{ color: {CINZA_TXT}; font-size: 12.5px; font-weight: 600; margin-top: 4px; }}

    .info-line {{ background: #F4F6F8; border-radius: 8px; padding: 10px 14px; font-size: 13.5px; color: {NAVY}; }}
    .impact-card {{
        background: #FAFAF8; border: 1px solid {LINHA}; border-radius: 12px; padding: 18px;
    }}
    .impact-val {{ font-size: 24px; font-weight: 800; color: {NAVY}; }}
    .impact-lbl {{ color: {CINZA_TXT}; font-size: 12.5px; }}
    </style>
""", unsafe_allow_html=True)


def fmt_moeda(val):
    if val is None:
        return "R$ 0"
    v = round(val)
    return f"R$ {v:,.0f}".replace(",", ".")


def fmt_num(val):
    if val is None:
        return "0"
    return f"{round(val):,.0f}".replace(",", ".")


# ============================================================
# 2. DADOS CENTRAIS DAS TRILHAS (única fonte da verdade —
#    escada, obra, cor e coeficientes de impacto econômico)
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
        "emoji": "🛒", "obra": 3, "escada": ESCADA_PADRAO, "cor": "#9A3F1E", "cor_bg": "#F7E9E1",
        "emprego_m2": 25, "faturamento_m2": 6000,
        "extra": "Isenção de 3 anos em alvará, licenciamento e TCL.",
        "contrapartida": "Cota de contratação local pontua no leilão saneado.",
        "justificativa": "Retrofit comercial é rápido (6 a 18 meses de obra) e a receita amadurece logo "
                          "após abrir. Seis anos dá fôlego frente ao e-commerce sem virar vantagem "
                          "permanente sobre o comércio vizinho fora do programa.",
    },
    "Saúde": {
        "emoji": "🏥", "obra": 5, "escada": ESCADA_SAUDE, "cor": "#0B6B4F", "cor_bg": "#E2F0EA",
        "emprego_m2": 20, "faturamento_m2": 8000,
        "extra": "Prazo de obra estendido pela exigência regulatória da Anvisa.",
        "contrapartida": "10% da capacidade de exames de alta complexidade para o SUS (Sisreg).",
        "justificativa": "Exigência da Anvisa (gases medicinais, subestação dedicada, blindagem) alonga "
                          "genuinamente o prazo de obra. Depois de aberto, o retorno também é mais lento: "
                          "equipamento caro, credenciamento de convênio, maturação de carteira de pacientes.",
    },
    "Educação": {
        "emoji": "🎓", "obra": 3, "escada": ESCADA_EDUCACAO, "cor": "#5B3E8A", "cor_bg": "#ECE6F5",
        "emprego_m2": 45, "faturamento_m2": 3500, "permanente": True,
        "extra": "Após o ano 10, desconto fixo de 30% sobre o IPTU total, revisado a cada 5 anos.",
        "contrapartida": "10% das vagas em bolsa integral via CadÚnico.",
        "justificativa": "Segue a lógica construtiva do Varejo, mas depois do ano 10 muda de natureza: "
                          "não é mais sobre recuperar custo de obra, é sobre sustentar qualidade — por "
                          "isso vira um desconto condicionado, não uma contagem de anos que termina.",
    },
    "Habitação": {
        "emoji": "🏠", "obra": 3, "escada": ESCADA_PADRAO, "cor": "#8A6D1D", "cor_bg": "#F5EFDD",
        "emprego_m2": 200, "faturamento_m2": None,
        "extra": "20% de bônus de potencial construtivo via Operação Interligada.",
        "contrapartida": "20% das unidades em Locação Social por 30 anos.",
        "justificativa": "Não é sobre tempo de obra — é sobre o tempo que o mercado leva para absorver e "
                          "vender as unidades novas, mesmo raciocínio do Reviver Centro.",
    },
}

ALIQUOTA_IPTU = 0.025          # 2,5% a.a. sobre o valor venal (não residencial edificado)
ALIQUOTA_INDIRETA = 0.05       # estimativa ilustrativa de ISS/ICMS(VAF) sobre o faturamento gerado
ALIQUOTA_ITBI = 0.03           # 3% — alíquota de ITBI no Rio

# ============================================================
# 3. CABEÇALHO
# ============================================================
st.markdown(f"""
<div class="gov-badge">
    <div class="gov-header-top">Prefeitura da Cidade do Rio de Janeiro · Reconversão Funcional de Ativos</div>
    <div class="main-title">Projeto Recupere Rio</div>
    <div class="sub-title">Simulador de trilhas setoriais, incentivo fiscal e impacto econômico</div>
    <div class="proto-tag">🛠️ Simulação técnica em desenvolvimento — sem caráter oficial</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 4. DIRETRIZES GERAIS
# ============================================================
st.markdown('<div class="sec-title">1. Diretrizes Gerais e Salvaguardas Operacionais</div>', unsafe_allow_html=True)

with st.expander("1.1 Teste de Enquadramento Funcional (Regra 70/50)", expanded=True):
    st.write("O investidor só mantém o regime se comprovar anualmente que no mínimo **70% da área "
             "construída** e **50% do faturamento bruto** provêm da atividade setorial declarada.")
with st.expander("1.2 Lista de Exclusão Fechada"):
    st.write("Vedados em qualquer trilha: estacionamentos rotativos puros, depósitos de sucata/ferro-velho, "
             "templos religiosos, sedes partidárias e painéis publicitários.")
with st.expander("1.3 Certificação Anual e Reversão Automática"):
    st.write("A Prefeitura tem direito de vistoria sem aviso prévio. Constatado descumprimento, o benefício "
             "é cassado e cobrado como Dívida Ativa, corrigido por IPCA-E.")
with st.expander("1.4 Gatilho de Revisão Quinquenal"):
    st.write("Nenhum incentivo opera em caráter perpétuo. Todos os descontos são auditados a cada 5 anos.")
with st.expander("1.5 Fundamentação Quantitativa por Custo de Instalação"):
    st.write("A diferenciação de prazos entre trilhas é sustentada por levantamento de custo de instalação "
             "por m² e ciclo de maturação de cada setor.")

# ============================================================
# 5. FLUXO DO INSTRUMENTO
# ============================================================
st.markdown('<div class="sec-title">2. Fluxo do Instrumento</div>', unsafe_allow_html=True)
passos = [
    ("1", "Notificação", "IPTU progressivo, 6 meses"),
    ("2", "Leilão saneado", "Aquisição do ativo"),
    ("3", "Seleção da trilha", "No sistema Reconverte"),
    ("4", "Escada de isenção", "Início pós-Habite-se"),
]
cols = st.columns(4)
for c, (n, t, d) in zip(cols, passos):
    c.markdown(f'<div class="flow-step"><b>{n}. {t}</b><br><span style="color:{CINZA_TXT};font-size:13px;">{d}</span></div>',
               unsafe_allow_html=True)
st.caption("Ao arrematar o imóvel no leilão saneado, o investidor seleciona a trilha no sistema Reconverte "
           "e a escada fiscal é gerada automaticamente.")

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
# 7. SIMULADOR
# ============================================================
st.markdown('<div class="sec-title">4. Simulador de Engenharia Financeira</div>', unsafe_allow_html=True)
st.write("Escolha a trilha, o tamanho do imóvel e o valor por m² — o valor venal e o IPTU integral são "
         "calculados automaticamente.")

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
    f'IPTU integral anual (pré-definido, {ALIQUOTA_IPTU*100:.1f}%): <b>{fmt_moeda(iptu_integral)}</b> '
    f'&nbsp;·&nbsp; Isenção de obra desta trilha: <b>até {t["obra"]} anos</b> antes da escada começar, '
    f'a partir do Habite-se.</div>', unsafe_allow_html=True)
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
m1.markdown(f'<div class="metric-card metric-pago"><div class="metric-val" style="color:{GOLD}">{fmt_moeda(tot_pago)}</div>'
            f'<div class="metric-lbl">Pago em 13 anos</div></div>', unsafe_allow_html=True)
m2.markdown(f'<div class="metric-card metric-econ"><div class="metric-val" style="color:{VERDE}">{fmt_moeda(tot_econ)}</div>'
            f'<div class="metric-lbl">Economia vs. cobrança cheia</div></div>', unsafe_allow_html=True)
m3.markdown(f'<div class="metric-card metric-sem"><div class="metric-val" style="color:{VERMELHO}">{fmt_moeda(tot_sem)}</div>'
            f'<div class="metric-lbl">Quanto pagaria sem o programa</div></div>', unsafe_allow_html=True)

st.write("")
st.subheader("📊 Comparativo ano a ano")
fig = go.Figure()
fig.add_bar(x=[f"Ano {a}" for a in anos], y=sem_beneficio, name="Sem o programa (cobrança cheia)", marker_color=VERMELHO)
fig.add_bar(x=[f"Ano {a}" for a in anos], y=pagos, name="Pago com o Recupere Rio", marker_color=GOLD)
fig.add_bar(x=[f"Ano {a}" for a in anos], y=economias, name="Economia no ano", marker_color=VERDE)
fig.update_layout(barmode="group", plot_bgcolor="white", paper_bgcolor="white",
                   legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
                   margin=dict(l=10, r=10, t=10, b=10), height=380,
                   yaxis=dict(gridcolor="#EEEDE6", tickprefix="R$ "))
st.plotly_chart(fig, use_container_width=True)

with st.expander("📋 Ver tabela detalhada ano a ano"):
    df = pd.DataFrame({
        "Ano": [f"Ano {a}" for a in anos],
        "Cobrança": [f"{pct_para_ano(a, t['escada'])}%" for a in anos],
        "Pago": [fmt_moeda(v) for v in pagos],
        "Sem benefício": [fmt_moeda(v) for v in sem_beneficio],
        "Economia": [fmt_moeda(v) for v in economias],
    })
    st.dataframe(df, hide_index=True, use_container_width=True)

# ============================================================
# 8. IMPACTOS ECONÔMICOS PROJETADOS (empregos + impostos indiretos)
# ============================================================
st.markdown('<div class="sec-title">5. Impactos Econômicos Projetados</div>', unsafe_allow_html=True)
st.caption("Estimativa ilustrativa a partir de coeficientes médios de mercado — não é uma projeção oficial "
           "de arrecadação. O coeficiente de emprego do Varejo toma como referência o setor de shopping "
           "centers (≈1 emprego a cada 17 m² de área bruta locável, ABRASCE/BNB).")

empregos_est = tamanho_m2 / t["emprego_m2"]

i1, i2, i3 = st.columns(3)
i1.markdown(f'<div class="impact-card"><div class="impact-val">{fmt_num(empregos_est)}</div>'
            f'<div class="impact-lbl">Empregos estimados gerados</div></div>', unsafe_allow_html=True)

if t["faturamento_m2"] is not None:
    faturamento_est = tamanho_m2 * t["faturamento_m2"]
    impostos_indiretos = faturamento_est * ALIQUOTA_INDIRETA
    i2.markdown(f'<div class="impact-card"><div class="impact-val">{fmt_moeda(faturamento_est)}</div>'
                f'<div class="impact-lbl">Faturamento anual estimado</div></div>', unsafe_allow_html=True)
    i3.markdown(f'<div class="impact-card"><div class="impact-val">{fmt_moeda(impostos_indiretos)}</div>'
                f'<div class="impact-lbl">Impostos indiretos estimados/ano (ISS/ICMS via VAF)</div></div>',
                unsafe_allow_html=True)
else:
    itbi_est = valor_venal * ALIQUOTA_ITBI
    i2.markdown(f'<div class="impact-card"><div class="impact-val">{fmt_moeda(itbi_est)}</div>'
                f'<div class="impact-lbl">ITBI estimado na comercialização (única vez, 3%)</div></div>',
                unsafe_allow_html=True)
    i3.markdown(f'<div class="impact-card"><div class="impact-val">—</div>'
                f'<div class="impact-lbl">Habitação não gera faturamento recorrente; ganho indireto vem do '
                f'ITBI e do consumo dos novos moradores no bairro</div></div>', unsafe_allow_html=True)

st.write("")
st.markdown(f"**Por que essa trilha tem esse prazo?** {t['justificativa']}")

# ============================================================
# 9. JUSTIFICATIVA TÉCNICA DOS PRAZOS
# ============================================================
st.markdown('<div class="sec-title">6. Justificativa Técnica dos Prazos</div>', unsafe_allow_html=True)
df_just = pd.DataFrame({
    "Trilha": ["Varejo/Indústria", "Saúde (obra)", "Saúde (incremental)", "Educação (incremental)",
               "Educação (pós-escada)", "Habitação"],
    "Prazo adotado": ["6 anos", "Até 5 anos", "8 anos", "6 anos", "Permanente*", "6 anos"],
    "Fundamentação técnica": [
        "Retrofit comercial é rápido (6 a 18 meses). Seis anos dá fôlego frente ao e-commerce sem virar "
        "vantagem permanente sobre o comércio vizinho.",
        "Exigência da Anvisa (gases medicinais, subestação dedicada, blindagem) alonga genuinamente o "
        "prazo de obra sem receita.",
        "Ciclo de maturação longo: equipamento caro, credenciamento de convênio, carteira de pacientes.",
        "Mesma lógica construtiva e de amortização do Varejo.",
        "Muda de natureza: não é mais sobre custo de obra, é sobre sustentar qualidade — desconto "
        "condicionado à nota do MEC, revisado a cada 5 anos.",
        "Tempo de absorção do mercado para vender as unidades na planta, alinhado ao Reviver Centro.",
    ],
})
st.dataframe(df_just, hide_index=True, use_container_width=True)
st.warning("⚠️ **Nota de ajuste de risco:** o par 5+8 anos da trilha Saúde é a premissa menos testada — "
           "recomenda-se validação técnica formal com a Secretaria Municipal de Saúde.")
