import streamlit as st

# Configuración de la página (DEBE SER LO PRIMERO)
st.set_page_config(page_title="OKGRUAS RS", page_icon="🚛", layout="centered")

# Estilo personalizado para el color rosa y fondo oscuro
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    .stButton>button { background-color: #FF69B4; color: white; border-radius: 10px; }
    h1 { color: #FF69B4; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# Lógica del Logo (Si falla, la app sigue adelante)
try:
    st.image("logo.png", width=200) # Asegúrate que se llame exactamente logo.png
except:
    st.write("### OKGRUAS RS")

st.title("🚛 Calculadora de Servicios")

# Formulario simple para probar
with st.form("servicio_form"):
    nombre = st.text_input("Nombre del Cliente")
    modelo = st.text_input("Modelo del Auto")
    destino = st.text_input("Punto de Entrega")
    
    enviar = st.form_submit_button("Generar Cotización")

if enviar:
    st.success(f"¡Listo! Preparando mensaje para {nombre}...")
    # Aquí irá el link de WhatsApp una vez que confirmemos que esto carga
