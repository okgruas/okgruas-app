import streamlit as st
import urllib.parse

# 1. Configuración de la página (¡Vital para evitar pantalla blanca!)
st.set_page_config(page_title="OKGRUAS RS", page_icon="🚛", layout="centered")

# 2. Estilo Visual (Rosa y Oscuro)
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .stButton>button { 
        background-color: #FF69B4; 
        color: white; 
        border-radius: 10px; 
        width: 100%;
        border: none;
        padding: 10px;
        font-weight: bold;
    }
    .stTextInput>div>div>input { background-color: #262626; color: white; border: 1px solid #FF69B4; }
    label { color: #FF69B4 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logo (Ajustado a logo.png)
try:
    st.image("logo.png", width=250)
except:
    st.markdown("<h1 style='color: #FF69B4;'>OKGRUAS RS</h1>", unsafe_allow_html=True)

# 4. Menú Lateral
menu = st.sidebar.radio("Menú", ["📱 Cotizador", "📊 Admin"])

if menu == "📱 Cotizador":
    st.title("Cotizador de Servicio")
    st.write("Completa los datos para enviar la cotización por WhatsApp.")

    with st.form("cotizador"):
        nombre = st.text_input("Nombre del Cliente")
        modelo = st.text_input("Modelo del Vehículo")
        origen = st.text_input("Ubicación de Recolección")
        destino = st.text_input("Punto de Entrega")
        notas = st.text_area("Notas adicionales (opcional)")
        
        btn_enviar = st.form_submit_button("📩 ENVIAR POR WHATSAPP")

    if btn_enviar:
        if nombre and modelo and destino:
            # Tu mensaje personalizado
            mensaje = f"Hola, soy {nombre}. Solicito servicio de grúa para un {modelo}.\n📍 De: {origen}\n🏁 A: {destino}\n📝 Notas: {notas}"
            mensaje_url = urllib.parse.quote(mensaje)
            # AQUÍ VA TU NÚMERO (Ya está listo)
            whatsapp_link = f"https://wa.me/528143029578?text={mensaje_url}"
            
            st.success("¡Cotización lista! Haz clic abajo para abrir WhatsApp.")
            st.markdown(f'''
                <a href="{whatsapp_link}" target="_blank">
                    <button style="background-color: #25D366; color: white; padding: 15px; border: none; border-radius: 10px; width: 100%; cursor: pointer; font-weight: bold;">
                        ✅ ABRIR MI WHATSAPP
                    </button>
                </a>
            ''', unsafe_allow_html=True)
        else:
            st.error("Por favor llena los campos principales (Nombre, Modelo y Destino).")

elif menu == "📊 Admin":
    st.title("Panel de Administración")
    password = st.text_input("Contraseña", type="password")
    
    if password == "RS2026":
        st.success("Acceso concedido")
        st.write("### Resumen de Operaciones")
        st.info("Aquí aparecerán tus estadísticas de servicios conforme los vayas registrando.")
        # Aquí puedes agregar más funciones después
    elif password != "":
        st.error("Contraseña incorrecta")
