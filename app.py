import streamlit as st
import pandas as pd
import unicodedata
import re
import os

# -----------------------------------------------------------------------------
# CONFIGURACIÓN VISUAL (ESTÉ TICA PADLET / PRIMER CICLO CABA)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TECNO ADIVINANZAS MACHINE 🤖",
    page_icon="🔮",
    layout="centered"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
        background-color: #E0F7FA !important;
        color: #1A237E !important;
    }
    
    .stApp {
        background-color: #E0F7FA;
    }

    .padlet-card {
        background-color: #FFFFFF;
        border: 4px solid #4DD0E1;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }

    .stButton > button {
        background-color: #FFD54F !important;
        color: #000000 !important;
        font-size: 24px !important;
        font-weight: bold !important;
        border: 3px solid #FFB300 !important;
        border-radius: 15px !important;
        padding: 10px 30px !important;
        box-shadow: 0 5px 0 #FF8F00 !important;
        width: 100%;
        text-transform: uppercase;
    }

    .stButton > button:hover {
        background-color: #FFE082 !important;
        transform: translateY(-2px);
    }

    .main-title {
        font-size: 38px;
        font-weight: 900;
        color: #0D47A1;
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .clock-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 15px 0;
    }
    .clock {
        width: 80px;
        height: 80px;
        border: 5px solid #0D47A1;
        border-radius: 50%;
        position: relative;
        background: #FFF;
    }
    .clock::after {
        content: '';
        position: absolute;
        width: 6px;
        height: 6px;
        background: #0D47A1;
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .hand-hour {
        position: absolute;
        width: 4px;
        height: 25px;
        background: #0D47A1;
        top: 18%;
        left: 48%;
        transform-origin: bottom;
        animation: spin 12s linear infinite;
    }
    .hand-minute {
        position: absolute;
        width: 3px;
        height: 32px;
        background: #E53935;
        top: 10%;
        left: 48%;
        transform-origin: bottom;
        animation: spin 2s linear infinite;
    }
    @keyframes spin {
        100% { transform: rotate(360deg); }
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# NORMALIZACIÓN Y LÓGICA DE DATOS
# -----------------------------------------------------------------------------
def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode("utf-8")
    texto = re.sub(r'[^a-zA-Z0-9\s]', '', texto)
    return texto.strip().upper()

@st.cache_data
def cargar_base_datos():
    if os.path.exists("adivinanzas.xlsx"):
        return pd.read_excel("adivinanzas.xlsx")
    else:
        return pd.DataFrame([
            {
                "ID": 1,
                "AUTOR": "CIRO 👦",
                "ADIVINANZA": "CON RUEDAS Y UN MOTOR, POR LAS CALLES VOY. CON COMBUSTIBLE MEJOR, A TU DESTINO TE LLEVO HOY. ¿QUÉ SOY?",
                "RESPUESTA": "AUTO",
                "ARCHIVO_PISTA": "pista_auto.png",
                "ARCHIVO_DIBUJO": "auto.png",
                "ARCHIVO_AUDIO": "audio_auto.mp3"
            }
        ])

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'INICIO'

if 'indice_adivinanza' not in st.session_state:
    st.session_state.indice_adivinanza = 0

df_adivinanzas = cargar_base_datos()
total_adivinanzas = len(df_adivinanzas)

# -----------------------------------------------------------------------------
# PÁGINA 1: INICIO
# -----------------------------------------------------------------------------
if st.session_state.pagina == 'INICIO':
    st.markdown("<div class='padlet-card'>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>🔮 TECNO ADIVINANZAS MACHINE 🤖</h1>", unsafe_allow_html=True)
    st.markdown("### 2° C - TRANSPORTES, MATERIALES Y ENERGÍAS 🚀🎨")
    st.markdown("---")
    st.markdown("## ¿ESTÁS LISTO PARA ADIVINAR? 🤔💭")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("¡VAMOS! 🚀"):
        st.session_state.pagina = 'JUEGO'
        st.rerun()

# -----------------------------------------------------------------------------
# PÁGINA 2: JUEGO / ADIVINANZA
# -----------------------------------------------------------------------------
elif st.session_state.pagina == 'JUEGO':
    adivinanza_actual = df_adivinanzas.iloc[st.session_state.indice_adivinanza]
    
    st.markdown(f"<h2 style='text-align:center;'>DESAFÍO #{st.session_state.indice_adivinanza + 1} DE {total_adivinanzas} ✨</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="clock-container">
            <div class="clock">
                <div class="hand-hour"></div>
                <div class="hand-minute"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='padlet-card'>", unsafe_allow_html=True)
    st.markdown(f"### 📝 ADIVINANZA DE {str(adivinanza_actual['AUTOR']).upper()}")
    st.markdown(f"## \"{str(adivinanza_actual['ADIVINANZA']).upper()}\"")
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 🔊 ESCUCHAR LA ADIVINANZA")
        ruta_audio = os.path.join("audios", str(adivinanza_actual['ARCHIVO_AUDIO']))
        if os.path.exists(ruta_audio):
            st.audio(ruta_audio)
        else:
            st.info("🎵 [AUDIO DE LECTURA DE ADIVINANZA]")

    with col2:
        st.markdown("#### 🧩 LÁMINA DE PISTAS")
        ruta_pista = os.path.join("pistas", str(adivinanza_actual['ARCHIVO_PISTA']))
        if os.path.exists(ruta_pista):
            st.image(ruta_pista, use_container_width=True)
        else:
            st.warning("🖼️ [LÁMINA DE PISTAS]")

    st.markdown("---")
    st.markdown("### ✍️ ESCRIBÍ TU RESPUESTA AQUÍ:")
    respuesta_ingresada = st.text_input("", key=f"input_{st.session_state.indice_adivinanza}", placeholder="ESCRIBÍ ACÁ TU RESPUESTA...")

    if st.button("VERIFICAR RESPUESTA 🔍"):
        respuesta_correcta = normalizar_texto(str(adivinanza_actual['RESPUESTA']))
        respuesta_usuario = normalizar_texto(respuesta_ingresada)

        if respuesta_usuario == respuesta_correcta and respuesta_usuario != "":
            st.session_state.pagina = 'EXITO'
            st.rerun()
        elif respuesta_usuario != "":
            st.error("❌ ¡CASI! INTENTÁ DE NUEVO O MIRÁ BIEN LAS PISTAS. 💡")

# -----------------------------------------------------------------------------
# PÁGINA 3: ÉXITO Y REVELACIÓN DEL DIBUJO
# -----------------------------------------------------------------------------
elif st.session_state.pagina == 'EXITO':
    adivinanza_actual = df_adivinanzas.iloc[st.session_state.indice_adivinanza]
    
    st.balloons()
    st.markdown("<div class='padlet-card'>", unsafe_allow_html=True)
    st.markdown("<h1>🎉 ¡EXCELENTE! ¡ADIVINASTE! 👏</h1>")
    st.markdown(f"<h2>EL PRODUCTO ES: {str(adivinanza_actual['RESPUESTA']).upper()} 🚀</h2>")
    st.markdown(f"### DIBUJO REALIZADO POR: {str(adivinanza_actual['AUTOR']).upper()}")
    
    ruta_dibujo = os.path.join("dibujos", str(adivinanza_actual['ARCHIVO_DIBUJO']))
    if os.path.exists(ruta_dibujo):
        st.image(ruta_dibujo, caption=f"Obra de {adivinanza_actual['AUTOR']}", use_container_width=True)
    else:
        st.info("🎨 [DIBUJO DEL ESTUDIANTE REVELADO]")
        
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("QUIERO OTRA ADIVINANZA ➡️"):
        if st.session_state.indice_adivinanza < total_adivinanzas - 1:
            st.session_state.indice_adivinanza += 1
        else:
            st.session_state.indice_adivinanza = 0
            
        st.session_state.pagina = 'JUEGO'
        st.rerun()
