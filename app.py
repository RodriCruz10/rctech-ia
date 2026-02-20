import streamlit as st
import google.generativeai as genai

# 1. Configuración visual
st.set_page_config(page_title="RC TECH - Asesor IA", page_icon="🛠️")

# 2. Tu API KEY (Asegurate de que sea la correcta)
API_KEY = "AIzaSyCS5CXCzrLoGr2FjwgynL0u_1DpCvm9IeE" 
genai.configure(api_key=API_KEY)

# 3. ADN de RC TECH
PROMPT_SISTEMA = "Sos RCTECH, experto en tecnología de Tucumán. Cobrás $50.000 por boca de instalación. 1 cámara=1 boca, 1 parlante=1 boca. Sos un vendedor experto y usás tono tucumano profesional."

st.title("🛠️ RC TECH - Asesor Tecnológico")
st.markdown("Bienvenido al futuro de tu hogar o local.")

# Función para encontrar el modelo disponible automáticamente
@st.cache_resource
def get_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # Priorizamos flash o pro si están
            if '1.5-flash' in m.name or 'pro' in m.name:
                return m.name
    return 'gemini-pro' # Por defecto

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
        model_name = get_model()
        model = genai.GenerativeModel(model_name)
        
        full_query = f"{PROMPT_SISTEMA}\n\nCliente: {prompt}"
        response = model.generate_content(full_query)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error técnico: {e}")
        st.info("Tip: Verificá que tu API KEY esté activa en Google AI Studio.")
