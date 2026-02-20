import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="RC TECH - Asesor IA", page_icon="🛠️")

# 2. TU API KEY (Asegurate de pegarla entre las comillas)
API_KEY = "AIzaSyCS5CXCzrLoGr2FjwgynL0u_1DpCvm9IeE" 
genai.configure(api_key=API_KEY)

# 3. ADN DE TU NEGOCIO
PROMPT_SISTEMA = """
Sos RCTECH, experto en tecnología de Tucumán, Argentina. 
Tu misión es asesorar y vender servicios de instalación de cámaras, alarmas, sonido, redes, Starlink y paneles solares.

REGLAS DE PRECIO:
- Mano de obra: $50.000 por cada 'boca' de instalación.
- 1 cámara = 1 boca ($50.000).
- 1 parlante = 1 boca ($50.000).
- 1 potencia = 2 bocas ($100.000).
- 1 toma corriente o lámpara (desde cero) = 1 boca ($50.000).

TONO:
- Sos de Tucumán: profesional, directo y amable. 
- Usás expresiones como 'De una', 'Es un golazo', 'Quedate tranquilo'.
- Siempre intentás cerrar la venta pidiendo fotos del lugar para un presupuesto final.
"""

# 4. INTERFAZ VISUAL
st.title("🛠️ RC TECH - Asesor Tecnológico")
st.markdown("### El futuro de tu hogar o negocio en Tucumán")
st.markdown("---")

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("¿En qué proyecto te ayudo hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Forzamos el modelo 1.5-flash para evitar errores de cuota
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Combinamos la instrucción con la pregunta
        full_query = f"{PROMPT_SISTEMA}\n\nCliente: {prompt}"
        
        response = model.generate_content(full_query)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
