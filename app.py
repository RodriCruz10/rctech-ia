import streamlit as st
import google.generativeai as genai

# Configuración visual
st.set_page_config(page_title="RC TECH - Asesor IA", page_icon="🛠️")

# PEGÁ ACÁ TU API KEY
API_KEY = "TU_API_KEY_AQUI" 
genai.configure(api_key=API_KEY)

# Instrucciones para la IA
PROMPT_SISTEMA = "Sos RCTECH, experto en tecnología de Tucumán. Cobrás $50.000 por boca de instalación (1 cámara=1 boca, 1 parlante=1 boca, 1 potencia=2 bocas). Sos un vendedor experto y usás tono tucumano profesional."

st.title("🛠️ RC TECH - Asesor Tecnológico")
st.markdown("Bienvenido al futuro de tu hogar o local. ¿En qué proyecto te ayudo hoy?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿Qué necesitás instalar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # CAMBIO CLAVE: Usamos gemini-pro que es más estable para este tipo de apps
        model = genai.GenerativeModel('gemini-pro')
        
        # Combinamos la instrucción con la pregunta para evitar el error de NotFound
        full_prompt = f"{PROMPT_SISTEMA}\n\nCliente pregunta: {prompt}"
        
        response = model.generate_content(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
