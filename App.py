import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Projeto Recupere Rio", layout="centered", page_icon="🏙️")

# Estilização CSS para replicar as cores e cartões escuros das imagens
st.markdown("""
    <style>
    .stApp { background-color: #11151C; }
    .main-title { color: #FFFFFF; font-size: 26px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .section-header { color: #FFFFFF; font-size: 20px; font-weight: bold; margin-top: 25px; margin-bottom: 15px; }
    .card-option { background-color: #1A1F29; border: 1px solid #2A3241; border-radius: 10px; padding: 12px; margin-bottom: 10px; }
    .card-selected { background-color: #1A1F29; border: 1.5px solid #D15A39; border-radius: 10px; padding: 12px; margin-bottom: 10px; }
    .accent-title { color: #D15A39; font-weight: bold; font-size: 16px; margin-bottom: 8px; }
    .big-metric-pago { color: #D15A39; font-size: 28px; font-weight: bold; margin-top: 15px; }
    .big-metric-econ { color: #D15A39; font-size: 28px; font-weight: bold; margin-top: 15px; }
    .metric-sub { color: #8C96A6; font-size: 13px; margin-bottom: 15px; }
    .box-justificativa { background-color: #1A1F29; border: 1px solid #D15A39; border-radius: 12px; padding: 18px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# ---------------- 1. ESCOLHA A TRILHA ----------------
st.markdown('<div class="section-header">1. Escolha a trilha</div>', unsafe_allow_html=True)

trilha_opcoes = {
    "Varejo / Indústria": "10 anos de escada",
    "Saúde": "10 anos de escada",
    "Educação": "até 10 anos + desconto fixo",
    "Habitação": "10 anos de escada"
}

trilha_selecionada = st.radio(
    "Selecione o setor:",
    options=list(trilha_opcoes.keys()),
    format_func=lambda x: f"{x} — {trilha_opcoes[x]}",
    label_visibility="collapsed"
)

st.divider()

# ---------------- CÁLCULOS DA TRILHA ----------------
if trilha_selecionada == "Varejo / Indústria":
    nome_trilha_extenso = "Varejo, Indústria e Logística"
    prazos_txt = "3 + 10 anos"
    justificativa = "Retrofit comercial é rápido — de 6 a 18 meses de obra — e a receita amadurece logo após abrir. Seis anos dá fôlego para competir com o e-commerce sem virar vantagem permanente sobre o comércio vizinho."
elif trilha_selecionada == "Saúde":
    nome_trilha_extenso = "Saúde"
    prazos_txt = "5 + 8 anos"
    justificativa = "Exigência regulatória da Anvisa alonga o prazo de obra (gases medicinais, subestação elétrica dedicada, blindagem radiológica). O ciclo de retorno é mais longo devido ao alto custo dos equipamentos."
elif trilha_selecionada == "Educação":
    nome_trilha_extenso = "Educação"
    prazos_txt = "3 + 6 anos + Desconto Permanente"
    justificativa = "O desconto permanente de 30% visa sustentar a qualidade do ensino ao longo do tempo, sendo condicionado à manutenção de nota máxima nos indicadores do MEC e revisado a cada 5 anos."
else:
    nome_trilha_extenso = "Habitação"
    prazos_txt = "3 + 6 anos"
    justificativa = "O prazo atende ao tempo de absorção do mercado para comercialização das unidades na planta, alinhado ao modelo do Reviver Centro."

# Caixa do Formulário de Entrada
st.markdown(f'<div class="accent-title">{nome_trilha_extenso}</div>', unsafe_allow_html=True)

valor_venal = st.number_input(
    "Valor venal do imóvel após a obra (R$)",
    value=8800000,
    step=100000,
    format="%d"
)

st.caption("Durante a obra, o terreno já tem isenção de IPTU por até 3 anos, antes desta escada começar a contar (a partir do Habite-se).")

# Cálculo do IPTU Padrão (Alíquota de 2.5% ao ano)
iptu_cheio_anual = valor_venal * 0.025

anos = list(range(1, 14))
cobrança_pct = []
iptu_pago = []

for ano in anos:
    if ano <= 6:
        pct = 0
    elif ano in [7, 8]:
        pct = 0 if trilha_selecionada == "Saúde" else 25
    elif ano in [9, 10]:
        pct = 25 if trilha_selecionada == "Saúde" else 50
    else: # Anos 11, 12, 13
        if trilha_selecionada == "Educação":
            pct = 70  # 30% de desconto permanente
        elif trilha_selecionada == "Saúde" and ano in [11, 12]:
            pct = 50
        else:
            pct = 100
            
    valor_ano = iptu_cheio_anual * (pct / 100.0)
    cobrança_pct.append(f"{pct}%")
    iptu_pago.append(valor_ano)

# Criação da Tabela Idêntica ao Print
df_tabela = pd.DataFrame({
    "Ano": [f"Ano {a}" for a in anos],
    "Cobrança": cobrança_pct,
    "IPTU no ano": [f"R$ {v:,.0f}".replace(",", ".") for v in iptu_pago]
})

st.table(df_tabela)

# Totais Financeiros
total_pago = sum(iptu_pago)
total_sem_beneficio = iptu_cheio_anual * 13
economia_total = total_sem_beneficio - total_pago

st.markdown(f'<div class="big-metric-pago">R$ {total_pago:,.0f}</div>'.replace(",", "."), unsafe_allow_html=True)
st.markdown('<div class="metric-sub">pago em 13 anos</div>', unsafe_allow_html=True)

st.markdown(f'<div class="big-metric-econ">R$ {economia_total:,.0f}</div>'.replace(",", "."), unsafe_allow_html=True)
st.markdown('<div class="metric-sub">economizado vs. cobrança cheia</div>', unsafe_allow_html=True)

st.divider()

# ---------------- 2. POR QUE ESSE PRAZO ----------------
st.markdown('<div class="section-header">2. Por que esse prazo</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="box-justificativa">
    <div style="color: #FFFFFF; font-weight: bold; margin-bottom: 8px;">
        • Por que {prazos_txt} na trilha {trilha_selecionada}?
    </div>
    <div style="color: #A3B1C2; font-size: 14px; line-height: 1.5;">
        {justificativa}
    </div>
</div>
""", unsafe_allow_html=True)
