import streamlit as st
import plotly.express as px
import pandas as pd

# ==========================================
# 1. CONFIGURAÇÃO E ESTADO INICIAL
# ==========================================
st.set_page_config(page_title="Guerra Fria: Globo 3D", layout="wide")

ORDEM_DOS_BLOCOS = ["Bloco Ocidental", "Bloco Oriental", "Não Alinhados"]

if 'numero_turno' not in st.session_state:
    st.session_state.numero_turno = 1

if 'indice_bloco_atual' not in st.session_state:
    st.session_state.indice_bloco_atual = 0

if 'historico' not in st.session_state:
    st.session_state.historico = ["Início da Guerra Fria em formato 3D. O Bloco Ocidental inicia sua jogada."]

if 'dados_paises' not in st.session_state:
    st.session_state.dados_paises = pd.DataFrame([
        # BLOCO OCIDENTAL
        {"iso_code": "USA", "pais": "Estados Unidos", "bloco": "Bloco Ocidental", "influencia": 100, "tecnologia": 90, "terras_raras": 30},
        {"iso_code": "DEU", "pais": "Alemanha Ocidental", "bloco": "Bloco Ocidental", "influencia": 70, "tecnologia": 85, "terras_raras": 10},
        {"iso_code": "JPN", "pais": "Japão", "bloco": "Bloco Ocidental", "influencia": 65, "tecnologia": 88, "terras_raras": 5},
        {"iso_code": "GBR", "pais": "Reino Unido", "bloco": "Bloco Ocidental", "influencia": 80, "tecnologia": 85, "terras_raras": 15},
        
        # BLOCO ORIENTAL
        {"iso_code": "RUS", "pais": "União Soviética", "bloco": "Bloco Oriental", "influencia": 100, "tecnologia": 88, "terras_raras": 80},
        {"iso_code": "CHN", "pais": "China", "bloco": "Bloco Oriental", "influencia": 80, "tecnologia": 50, "terras_raras": 95},
        {"iso_code": "CUB", "pais": "Cuba", "bloco": "Bloco Oriental", "influencia": 50, "tecnologia": 30, "terras_raras": 20},
        
        # NÃO ALINHADOS
        {"iso_code": "BRA", "pais": "Brasil", "bloco": "Não Alinhados", "influencia": 50, "tecnologia": 40, "terras_raras": 85},
        {"iso_code": "IND", "pais": "Índia", "bloco": "Não Alinhados", "influencia": 60, "tecnologia": 45, "terras_raras": 60},
        {"iso_code": "EGY", "pais": "Egito", "bloco": "Não Alinhados", "influencia": 50, "tecnologia": 35, "terras_raras": 15},
        {"iso_code": "ZAF", "pais": "África do Sul", "bloco": "Não Alinhados", "influencia": 45, "tecnologia": 45, "terras_raras": 70},
    ])

bloco_atual = ORDEM_DOS_BLOCOS[st.session_state.indice_bloco_atual]

# ==========================================
# 2. LÓGICA DE TURNOS E AÇÕES
# ==========================================
def passar_turno():
    st.session_state.indice_bloco_atual = (st.session_state.indice_bloco_atual + 1) % len(ORDEM_DOS_BLOCOS)
    if st.session_state.indice_bloco_atual == 0:
        st.session_state.numero_turno += 1
        
    proximo_bloco = ORDEM_DOS_BLOCOS[st.session_state.indice_bloco_atual]
    st.session_state.historico.insert(0, f"⏳ Turno finalizado. Agora é a vez do **{proximo_bloco}**.")

def acao_investir_pesquisa(pais_nome):
    idx = st.session_state.dados_paises.index[st.session_state.dados_paises['pais'] == pais_nome].tolist()[0]
    st.session_state.dados_paises.at[idx, 'tecnologia'] += 5
    st.session_state.historico.insert(0, f"🔬 **{bloco_atual}**: {pais_nome} investiu em Pesquisa e Desenvolvimento (+5 Tec).")
    passar_turno()

def acao_expandir_influencia(pais_nome):
    idx = st.session_state.dados_paises.index[st.session_state.dados_paises['pais'] == pais_nome].tolist()[0]
    st.session_state.dados_paises.at[idx, 'influencia'] += 5
    st.session_state.historico.insert(0, f"📣 **{bloco_atual}**: {pais_nome} expandiu sua Influência Geopolítica (+5 Inf).")
    passar_turno()

# ==========================================
# 3. INTERFACE COM GLOBO 3D
# ==========================================
st.title("🌐 Guerra Fria: Globo Geopolítico 3D")

cores_blocos = {
    "Bloco Ocidental": "#1f77b4", # Azul
    "Bloco Oriental": "#d62728",  # Vermelho
    "Não Alinhados": "#7f7f7f"    # Cinza
}

col_painel, col_mapa = st.columns([1, 2.5])

# --- PAINEL DE CONTROLE ---
with col_painel:
    st.subheader(f"🔄 Rodada Global: {st.session_state.numero_turno}")
    
    if bloco_atual == "Bloco Ocidental":
        st.info(f"👉 Vez de Jogar: **{bloco_atual}**")
    elif bloco_atual == "Bloco Oriental":
        st.error(f"👉 Vez de Jogar: **{bloco_atual}**")
    else:
        st.warning(f"👉 Vez de Jogar: **{bloco_atual}**")

    paises_do_bloco = st.session_state.dados_paises[
        st.session_state.dados_paises['bloco'] == bloco_atual
    ]['pais'].tolist()

    st.markdown("### 🎯 Selecione a Ação")
    pais_escolhido = st.selectbox("Escolha um país sob seu controle:", paises_do_bloco)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔬 Avançar P&D", use_container_width=True):
            acao_investir_pesquisa(pais_escolhido)
            st.rerun()

    with col_btn2:
        if st.button("📣 Expandir Influência", use_container_width=True):
            acao_expandir_influencia(pais_escolhido)
            st.rerun()

    if st.button("⏭️ Passar a Vez", use_container_width=True):
        passar_turno()
        st.rerun()

    st.divider()
    st.subheader("📜 Diário do Conflito")
    for log in st.session_state.historico[:6]:
        st.markdown(log)

# --- MAPA 3D (GLOBO TERRESTRE) ---
with col_mapa:
    fig = px.choropleth(
        st.session_state.dados_paises,
        locations="iso_code",
        color="bloco",
        hover_name="pais",
        hover_data=["influencia", "tecnologia", "terras_raras"],
        color_discrete_map=cores_blocos,
        projection="orthographic"  # <-- ESTA PROJEÇÃO CRIA O GLOBO 3D
    )
    
    # Customizações estéticas para tornar o globo terrestre realista
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="black",
        showland=True,
        landcolor="#e5ecf6",
        showocean=True,
        oceancolor="#a2c4c9",     # Cor da água do oceano
        showlakes=True,
        lakecolor="#a2c4c9",
        bgcolor="rgba(0,0,0,0)"   # Fundo transparente em volta do globo
    )
    
    fig.update_layout(
        margin={"r":0, "t":10, "l":0, "b":0},
        height=600  # Aumenta a altura para destacar o formato do planeta
    )
    
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        st.session_state.dados_paises[['pais', 'bloco', 'influencia', 'tecnologia', 'terras_raras']],
        use_container_width=True
    )