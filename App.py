import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Projeto Recupere Rio", layout="wide", page_icon="🏙️")

# Estilização básica via CSS injetado
st.markdown("""
    <style>
    .titulo { color: #1B3A5C; font-size: 36px; font-weight: bold; text-align: center; }
    .subtitulo { color: #5C6772; font-size: 20px; font-style: italic; text-align: center; margin-bottom: 30px; }
    .kicker { color: #1B3A5C; font-size: 16px; text-align: center; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# CAPA
st.markdown('<div class="titulo">PROJETO RECUPERE RIO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Reconversão Funcional de Ativos</div>', unsafe_allow_html=True)
st.markdown('<div class="kicker">MEMORIAL TÉCNICO E DIRETRIZES DE ENGENHARIA FINANCEIRA<br>Parte 1 — O Instrumento de Reocupação</div>', unsafe_allow_html=True)
st.divider()

st.info("Documento de consolidação técnica preparado para subsídio às Secretarias Municipais de Fazenda, Urbanismo e Desenvolvimento Econômico do Rio de Janeiro.")

# NAVEGAÇÃO LATERAL (SUMÁRIO)
st.sidebar.title("Sumário")
st.sidebar.markdown("""
- [1. Diretrizes Gerais](#1-diretrizes-gerais-e-salvaguardas)
- [2. Fluxo do Instrumento](#2-fluxo-do-instrumento)
- [3. Matriz de Trilhas](#3-matriz-de-trilhas-setoriais)
- [4. Modelagem Fiscal](#4-modelagem-fiscal-incremental)
- [5. Justificativas](#5-justificativa-t-cnica-dos-prazos)
""")

# 1. DIRETRIZES GERAIS (Usando Expansores para não poluir a tela)
st.header("1. Diretrizes Gerais e Salvaguardas")
st.write("Regras transversais de aplicação obrigatória às quatro trilhas setoriais.")

regras = {
    "1.1 Teste de Enquadramento Funcional (Regra 70/50)": "O investidor só mantém o regime se comprovar anualmente que 70% da área e 50% do faturamento provêm da atividade declarada...",
    "1.2 Lista de Exclusão Fechada": "Ficam vedados: estacionamentos rotativos puros, ferros-velhos, templos, sedes partidárias e outdoors.",
    "1.3 Certificação Anual e Reversão": "A Prefeitura tem direito de vistoria sem aviso prévio. Constatado descumprimento, o benefício é cassado e cobrado como Dívida Ativa.",
    "1.4 Gatilho de Revisão Quinquenal": "Nenhum incentivo opera em caráter perpétuo. Todo desconto é submetido a auditoria a cada 5 anos.",
    "1.5 Fundamentação Quantitativa": "A diferença de prazo entre trilhas deve ser sustentada por levantamento de custo de instalação."
}

for titulo, desc in regras.items():
    with st.expander(titulo):
        st.write(desc)

st.divider()

# 2. FLUXO (Usando colunas para simular um diagrama de blocos)
st.header("2. Fluxo do Instrumento")
col1, col2, col3, col4 = st.columns(4)
col1.success("📄 1. Notificação\n(IPTU progressivo, 6 meses)")
col2.warning("🔨 2. Leilão saneado")
col3.info("💻 3. Seleção da trilha no sistema")
col4.primary("📈 4. Escada de isenção pós-Habite-se")

st.caption("Ao arrematar o imóvel no leilão saneado, o investidor seleciona a trilha setorial de destinação no sistema Reconverte...")
st.divider()

# 3. MATRIZ DE TRILHAS SETORIAIS (Usando Abas Interativas)
st.header("3. Matriz de Trilhas Setoriais")
tab1, tab2, tab3, tab4 = st.tabs(["🛒 Varejo & Indústria", "🏥 Saúde", "🎓 Educação", "🏠 Habitação"])

with tab1:
    st.subheader("Varejo, Indústria Leve e Logística")
    st.markdown("**Escopo:** Retrofit comercial, polos varejistas, logística de última milha.")
    st.markdown("**Isenção na Obra:** Até 3 anos.")
    st.markdown("**Isenção Incremental:** 6 anos.")
    st.markdown("**Contrapartida:** Cota de contratação local pontua no leilão.")

with tab2:
    st.subheader("Saúde")
    st.markdown("**Escopo:** Hospitais, prontos-socorros, laboratórios.")
    st.markdown("**Isenção na Obra:** Até 5 anos (complexidade Anvisa).")
    st.markdown("**Isenção Incremental:** 8 anos.")
    st.markdown("**Contrapartida:** 10% da capacidade de exames/consultas para o Sisreg (SUS).")

with tab3:
    st.subheader("Educação")
    st.markdown("**Escopo:** Faculdades, escolas técnicas, CTs em tecnologia.")
    st.markdown("**Isenção na Obra:** Até 3 anos.")
    st.markdown("**Isenção Incremental:** 6 anos + 30% permanente condicionado ao MEC.")
    st.markdown("**Contrapartida:** 10% de bolsas integrais para inscritos no CadÚnico.")

with tab4:
    st.subheader("Habitação")
    st.markdown("**Escopo:** Retrofit residencial puro ou misto.")
    st.markdown("**Isenção na Obra:** Até 3 anos.")
    st.markdown("**Isenção Incremental:** 6 anos.")
    st.markdown("**Adicional:** 20% de bônus de potencial construtivo.")
    st.markdown("**Contrapartida:** 20% das unidades para Locação Social por 30 anos.")

st.divider()

# 4. TABELA COMPARATIVA (Usando DataFrame interativo)
st.header("4. Modelagem Fiscal Incremental")
st.write("Alíquota cobrada sobre o valor incremental, por ano, a partir do Habite-se.")

df_fiscal = pd.DataFrame({
    "Período": ["Anos 1 a 6", "Ano 7", "Ano 8", "Ano 9", "Ano 10", "Ano 11 em diante"],
    "Varejo/Indústria": ["Isento", "25%", "25%", "50%", "50%", "100%"],
    "Saúde": ["Isento", "Isento", "Isento", "25%", "50%", "100%"],
    "Educação": ["Isento", "25%", "25%", "50%", "50%", "70% (fixo)*"],
    "Habitação": ["Isento", "25%", "25%", "50%", "50%", "100%"]
})
# Mostra a tabela sem o index lateral
st.dataframe(df_fiscal, hide_index=True, use_container_width=True)
st.caption("* O desconto de 30% da trilha Educação incide sobre o IPTU total do imóvel.")
st.divider()

# 5. JUSTIFICATIVA (Usando DataFrame)
st.header("5. Justificativa Técnica dos Prazos")
df_just = pd.DataFrame({
    "Trilha/Fase": ["Varejo/Indústria", "Saúde (obra)", "Saúde (incremental)", "Educação (incremental)", "Educação (pós-escada)", "Habitação"],
    "Prazo": ["6 anos", "Até 5 anos", "8 anos", "6 anos", "Permanente*", "6 anos"],
    "Por Quê": [
        "Retrofit comercial é rápido. 6 anos dá fôlego frente ao e-commerce.",
        "Exigência da Anvisa alonga o prazo de obra genuinamente.",
        "Ciclo de retorno mais longo. Menos generoso que o CEBAS federal.",
        "Mesma lógica construtiva do Varejo.",
        "Muda de natureza: sustentar qualidade testada pelo MEC, e não custo de obra.",
        "Tempo de absorção do mercado para vender unidades (alinhado ao Reviver Centro)."
    ]
})
st.table(df_just)
st.warning("Nota: O par 5+8 anos da trilha Saúde é a premissa menos testada e requer validação da Secretaria de Saúde.")
