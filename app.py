import streamlit as st
import pandas as pd
import unicodedata
import re
import os
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN VISUAL Y ESTÉTICA FIEL AL PADLET (VIOLETA Y AMARILLO)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TECNO ADIVINANZAS MACHINE 🤖",
    page_icon="🔮",
    layout="centered"
)

# Estilos CSS exactos según la carátula del Padlet
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&display=swap');

    /* Fondo amarillo vibrante de la carátula */
    html, body, [class*="css"]  {
        font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
        background-color: #FDF073 !important;
        color: #2D1B69 !important;
    }
    
    .stApp {
        background-color: #FDF073;
    }

    /* Tarjeta principal con fondo violeta claro y borde lila */
    .padlet-card {
        background-color: #E2D7F8;
        border: 4px solid #A88BEB;
        border-radius: 25px;
        padding: 30px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.15);
        text-align: center;
        margin-bottom: 25px;
    }

    /* Botones grandes en Amarillo Vibrante con bordes gruesos */
    .stButton > button {
        background-color: #FFDE38 !important;
        color: #1A0938 !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        border: 4px solid #F3B700 !important;
        border-radius: 20px !important;
        padding: 15px 30px !important;
        box-shadow: 0 6px 0 #D49B00 !important;
        width: 100%;
        text-transform: uppercase;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .stButton > button:hover {
        background-color: #FFE66D !important;
        transform: translateY(-2px);
    }

    .main-title {
        font-size: 52px;
        font-weight: 900;
        color: #6C4AB6;
        text-align: center;
        margin-bottom: 5px;
        line-height: 1.1;
    }

    .subtitle {
        font-size: 24px;
        color: #461578;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* Esfera mágica emulada en CSS */
    .crystal-ball {
        width: 160px;
        height: 160px;
        margin: 0 auto 20px auto;
        background: radial-gradient(circle at 35% 35%, #E9D5FF, #8B5CF6 60%, #4C1D95 100%);
        border-radius: 50%;
        box-shadow: inset -10px -10px 20px rgba(0,0,0,0.3), 0 0 25px #C084FC;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 900;
        font-size: 16px;
        text-align: center;
        padding: 15px;
        line-height: 1.2;
        border: 3px solid #DDD6FE;
    }

    .cloud-card {
        background-color: #FFFFFF;
        border: 5px solid #38BDF8;
        border-radius: 40px;
        padding: 30px;
        box-shadow: 0px 10px 25px rgba(56, 189, 248, 0.3);
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. FUNCIONES DE LECTURA DE AUDIO CON IA Y FLEXIBILIDAD DE RESPUESTAS
# -----------------------------------------------------------------------------
def reproducir_audio_ia(texto):
    """Genera un botón accesible para escuchar el texto en voz alta con IA."""
    texto_limpio = str(texto).replace('"', '').replace("'", "").replace('\n', ' ')
    html_code = f"""
        <div style="text-align: center; margin: 10px 0;">
            <button onclick="speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{texto_limpio}'); msg.lang = 'es-AR'; msg.rate = 0.85; speechSynthesis.speak(msg);" 
            style="
                background-color: #FFDE38;
                color: #1A0938;
                font-size: 20px;
                font-weight: 900;
                border: 3px solid #F3B700;
                border-radius: 16px;
                padding: 12px 24px;
                cursor: pointer;
                box-shadow: 0 4px #D49B00;
                width: 100%;
                font-family: 'Comic Sans MS', cursive, sans-serif;
            ">🔊 ESCUCHAR EN VOZ ALTA</button>
        </div>
    """
    components.html(html_code, height=70)

def normalizar_texto(texto):
    """Elimina tildes, signos y pasa todo a mayúsculas para tolerar errores ortográficos."""
    if not isinstance(texto, str):
        return ""
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode("utf-8")
    texto = re.sub(r'[^a-zA-Z0-9\s]', '', texto)
    return texto.strip().upper()

def buscar_imagen_existente(nombre_base, carpeta):
    """Busca automáticamente si la imagen existe como .png, .jpg, .jpeg o en minúsculas."""
    if not nombre_base or str(nombre_base).strip() == "":
        return None
        
    nombre_limpio = str(nombre_base).strip()
    # Si viene con extensión, quitársela para probar todas
    nombre_sin_ext = os.path.splitext(nombre_limpio)[0]
    
    extensiones = ["", ".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]
    carpetas_posibles = [carpeta, carpeta.lower(), carpeta.capitalize()]
    
    for c in carpetas_posibles:
        for ext in extensiones:
            posible_ruta = os.path.join(c, nombre_sin_ext + ext)
            if os.path.exists(posible_ruta) and not os.path.isdir(posible_ruta):
                return posible_ruta
    return None

# -----------------------------------------------------------------------------
# 3. CARGA SEGURA DE BASE DE DATOS EXCEL
# -----------------------------------------------------------------------------
@st.cache_data
def cargar_base_datos():
    archivos = ["Adivinanzas_Estudiantes_Padlet.xlsx", "adivinanzas.xlsx"]
    archivo_encontrado = None
    
    for arc in archivos:
        if os.path.exists(arc):
            archivo_encontrado = arc
            break

    if archivo_encontrado:
        df = pd.read_excel(archivo_encontrado)
        df.columns = df.columns.str.strip()
        return df
    else:
        return pd.DataFrame([
            {
                "NOMBRE DEL ESTUDIANTE": "CIRO",
                "ADIVINANZA": "CON RUEDAS Y UN MOTOR, POR LAS CALLES VOY CON COMBUSTIBLE MEJOR, A TU DESTINO TE LLEVO HOY ¿QUÉ SOY?",
                "Respuesta": "Auto",
                "ARCHIVO_PISTA": "Pista_Auto",
                "ARCHIVO_DIBUJO": "Auto"
            }
        ])

# Inicialización de Estados
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'INICIO'

if 'indice_adivinanza' not in st.session_state:
    st.session_state.indice_adivinanza = 0

if 'intentos_fallidos' not in st.session_state:
    st.session_state.intentos_fallidos = 0

df_adivinanzas = cargar_base_datos()
total_adivinanzas = len(df_adivinanzas)

# -----------------------------------------------------------------------------
# PÁGINA 1: CARÁTULA / INICIO FIEL A PADLET
# -----------------------------------------------------------------------------
if st.session_state.pagina == 'INICIO':
    st.markdown("<div class='padlet-card'>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>2° C</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Transportes, Materiales y Energías 🚀🎨</div>", unsafe_allow_html=True)
    
    # Esfera mágica de cristal
    st.markdown("""
        <div class="crystal-ball">
            TECNO<br>ADIVINANZAS<br>MACHINE
        </div>
    """, unsafe_allow_html=True)

    texto_bienvenida = "Las siguientes adivinanzas fueron hechas por los chicos de 2do Grado que analizaron los transportes y con la ayuda de la Seño Marcia usaron TecnoAdivinanza: un asistente para hacer rimas de adivinanza."
    st.markdown(f"### {texto_bienvenida}")
    
    reproducir_audio_ia(texto_bienvenida)
    
    st.markdown("---")
    pregunta_inicio = "¿Estás listo para adivinar?"
    st.markdown(f"## {pregunta_inicio} 🤔💭")
    reproducir_audio_ia(pregunta_inicio)
    
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("¡VAMOS! 🚀"):
        st.session_state.pagina = 'JUEGO'
        st.session_state.intentos_fallidos = 0
        st.rerun()

# -----------------------------------------------------------------------------
# PÁGINA 2: JUEGO / DESAFÍO
# -----------------------------------------------------------------------------
elif st.session_state.pagina == 'JUEGO':
    adivinanza_actual = df_adivinanzas.iloc[st.session_state.indice_adivinanza]
    
    col_autor = [c for c in adivinanza_actual.index if "NOMBRE" in c.upper() or "ESTUDIANTE" in c.upper() or "AUTOR" in c.upper()][0]
    col_texto = [c for c in adivinanza_actual.index if "ADIVINANZA" in c.upper()][0]
    col_resp = [c for c in adivinanza_actual.index if "RESPUESTA" in c.upper()][0]
    col_pista = [c for c in adivinanza_actual.index if "PISTA" in c.upper()][0]

    autor = str(adivinanza_actual[col_autor]).strip().upper()
    texto_adivinanza = str(adivinanza_actual[col_texto]).strip().upper()

    st.markdown(f"<h2 style='text-align:center;'>DESAFÍO #{st.session_state.indice_adivinanza + 1} DE {total_adivinanzas} ✨</h2>", unsafe_allow_html=True)

    st.markdown("<div class='padlet-card'>", unsafe_allow_html=True)
    st.markdown(f"### 📝 ADIVINANZA DE {autor}")
    st.markdown(f"## \"{texto_adivinanza}\"")
    reproducir_audio_ia(f"Adivinanza de {autor}. {texto_adivinanza}")
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 🧩 LÁMINA DE PISTAS")
        nombre_pista_raw = str(adivinanza_actual[col_pista])
        ruta_pista = buscar_imagen_existente(nombre_pista_raw, "Pistas")
        
        if ruta_pista:
            st.image(ruta_pista, use_container_width=True)
        else:
            st.warning(f"🖼️ [LÁMINA DE PISTA: {nombre_pista_raw}]")

    with col2:
        st.markdown("#### ✍️ ESCRIBÍ TU RESPUESTA")
        respuesta_ingresada = st.text_input("", key=f"input_{st.session_state.indice_adivinanza}", placeholder="Escribí acá tu respuesta...")

        if st.button("VERIFICAR RESPUESTA 🔍"):
            respuesta_correcta = normalizar_texto(str(adivinanza_actual[col_resp]))
            respuesta_usuario = normalizar_texto(respuesta_ingresada)

            if respuesta_usuario == respuesta_correcta and respuesta_usuario != "":
                st.session_state.pagina = 'EXITO'
                st.session_state.intentos_fallidos = 0
                st.rerun()
            elif respuesta_usuario != "":
                st.session_state.intentos_fallidos += 1
                st.rerun()

    # Retroalimentación por intentos fallidos
    if st.session_state.intentos_fallidos == 1:
        msg_1 = "Piensa un poquito más..."
        st.warning(f"💡 {msg_1}")
        reproducir_audio_ia(msg_1)
        
    elif st.session_state.intentos_fallidos >= 2:
        msg_2 = "Estuviste cerca. Inténtalo otra vez."
        st.error(f"❌ {msg_2}")
        reproducir_audio_ia(msg_2)
        
        msg_pregunta = "¿Quieres continuar con esta adivinanza o probar con otra?"
        st.markdown(f"### {msg_pregunta}")
        reproducir_audio_ia(msg_pregunta)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("CONTINUAR 🔄"):
                st.session_state.intentos_fallidos = 0
                st.rerun()
        with col_b:
            if st.button("PROBAR OTRA ADIVINANZA ➡️"):
                st.session_state.intentos_fallidos = 0
                if st.session_state.indice_adivinanza < total_adivinanzas - 1:
                    st.session_state.indice_adivinanza += 1
                else:
                    st.session_state.indice_adivinanza = 0
                st.rerun()

# -----------------------------------------------------------------------------
# PÁGINA 3: ÉXITO / REVELACIÓN EN NUBE GRANDE
# -----------------------------------------------------------------------------
elif st.session_state.pagina == 'EXITO':
    adivinanza_actual = df_adivinanzas.iloc[st.session_state.indice_adivinanza]
    
    col_autor = [c for c in adivinanza_actual.index if "NOMBRE" in c.upper() or "ESTUDIANTE" in c.upper() or "AUTOR" in c.upper()][0]
    col_resp = [c for c in adivinanza_actual.index if "RESPUESTA" in c.upper()][0]
    col_dibujo = [c for c in adivinanza_actual.index if "DIBUJO" in c.upper()][0]

    autor = str(adivinanza_actual[col_autor]).strip().upper()
    respuesta = str(adivinanza_actual[col_resp]).strip().upper()

    st.balloons()

    st.markdown("<div class='cloud-card'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #0284C7; font-size: 60px;'>☁️ ¡EXCELENTE! ☁️</h1>", unsafe_allow_html=True)
    reproducir_audio_ia("¡Excelente!")
    
    st.markdown(f"<h2>EL PRODUCTO ES: {respuesta} 🚀</h2>", unsafe_allow_html=True)
    st.markdown(f"### DIBUJO REALIZADO POR: {autor}", unsafe_allow_html=True)
    
    nombre_dibujo_raw = str(adivinanza_actual[col_dibujo])
    ruta_dibujo = buscar_imagen_existente(nombre_dibujo_raw, "Dibujos")
    
    if ruta_dibujo:
        st.image(ruta_dibujo, caption=f"Obra de {autor}", use_container_width=True)
    else:
        st.info(f"🎨 [DIBUJO REVELADO: {nombre_dibujo_raw}]")
        
    st.markdown("</div>", unsafe_allow_html=True)

    msg_volver = "¿Quieres volver a adivinar?"
    st.markdown(f"<h2 style='text-align:center;'>{msg_volver}</h2>", unsafe_allow_html=True)
    reproducir_audio_ia(msg_volver)

    if st.button("¡VAMOS! 🚀"):
        if st.session_state.indice_adivinanza < total_adivinanzas - 1:
            st.session_state.indice_adivinanza += 1
        else:
            st.session_state.indice_adivinanza = 0
            
        st.session_state.pagina = 'JUEGO'
        st.session_state.intentos_fallidos = 0
        st.rerun()
