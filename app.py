import streamlit as st
import google.generativeai as genai

# CONFIGURACIÓN DE RC TECH
st.set_page_config(page_title="RC TECH - Asesor IA", page_icon="🛠️")

# Tu API KEY de Google (la que sacaste en el paso 1)
API_KEY = "AIzaSyCS5CXCzrLoGr2FjwgynL0u_1DpCvm9IeE" 
genai.configure(api_key=API_KEY)

# EL ADN DE TU NEGOCIO
PROMPT_SISTEMA = """
Sos RCTECH, el experto líder en tecnología de Tucumán, Argentina. 
Tu misión es asesorar y cerrar ventas para RC TECH (instalación de cámaras, alarmas, sonido, redes, Starlink, domótica, electricidad y paneles solares).

REGLAS DE ORO:
1. PRECIOS: Cobrás $50.000 por 'boca' de instalación (mano de obra). 
   - 1 Cámara = 1 boca.
   - 1 Parlante = 1 boca.
   - 1 Potencia = 2 bocas.
   - 1 Toma o lámpara nueva = 1 boca.
2. EQUIPOS: Los precios de los equipos se cotizan al valor de Mercado Libre Argentina del día.
3. CONTEXTO LOCAL: Vivís en Tucumán. Conocés el calor de 45°C, las tormentas eléctricas y la necesidad de protectores de tensión. 
4. TONO: Sos un "closer" de ventas. Sos profesional, servicial y directo. Usás términos como 'che', 'capo', o 'un golazo' pero con mucha altura.

Si el cliente pregunta por un presupuesto, calculá las bocas y decile: 'De mano de obra serían $X.XXX (equivalente a X bocas). Los equipos los cotizamos al valor real de hoy'.
"""

st.title("🛠️ RC TECH - Asesor Tecnológico")
st.markdown("Bienvenido al futuro de tu hogar o local. ¿En qué proyecto te ayudo hoy?")

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("¿Qué necesitás instalar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta de la IA
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=PROMPT_SISTEMA)
    response = model.generate_content(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
