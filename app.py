import streamlit as st
import pandas as pd
import unicodedata
import re
import os
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN VISUAL (ESTÉTICA PADLET / PRIMER CICLO CABA)
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

    /* Reloj analógico animado */
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
# 2. NORMALIZACIÓN Y LÓGICA DE DATOS
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
                "ARCHIVO_DIBUJO": "auto.png"
            },
            {
                "ID": 2,
                "AUTOR": "CONRADO 👦",
                "ADIVINANZA": "CON ALAS METÁLICAS VOY POR EL CIELO, MI FUERTE MOTOR ME IMPULSA SIN PARAR. LLEVO PASAJEROS EN CADA VUELO. ¿QUÉ SOY?",
                "RESPUESTA": "AVION",
                "ARCHIVO_PISTA": "pista_avion.png",
                "ARCHIVO_DIBUJO": "avion.png"
            }
        ])
