import streamlit as st
import urllib.parse

# 1. Configuración base
st.set_page_config(page_title="OKGRUAS RS", page_icon="🚛", layout="centered")

# 2. Estilo de tu marca (RXS Rosa/Oscuro)
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .stButton>button { background-color: #FF69B4; color: white; border-radius: 10px; font-weight: bold; width: 100%; }
    label { color: #FF69B4 !important; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #262626 !important; color: white !important; border: 1px solid #FF69B4 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Menú de navegación
menu = st.sidebar.radio("Ir a:", ["📱 Cotizador Público", "📊 Panel RXS (Privado)"])

# --- SECCIÓN PÚBLICA: COTIZADOR ---
if menu == "📱 Cotizador Público":
    st.image("logo.png", width=200) if st.sidebar.button("Refrescar") else st.title("OKGRUAS RS")
    st.write("### Solicita tu Grúa")
    
    with st.form("form_publico"):
        nombre = st.text_input("Tu Nombre")
        modelo = st.text_input("Modelo del Auto")
        destino = st.text_input("¿A dónde lo llevamos?")
        btn_enviar = st.form_submit_button("📩 ENVIAR SOLICITUD")
        
    if btn_enviar:
        texto = f"Hola, soy {nombre}. Necesito grúa para un {modelo}. Destino: {destino}"
        st.markdown(f'<a href="https://wa.me/528143029578?text={urllib.parse.quote(texto)}" target="_blank"><button style="width:100%; background-color:#25D366; border:none; padding:10px; color:white; border-radius:10px; cursor:pointer;">✅ CONFIRMAR POR WHATSAPP</button></a>', unsafe_allow_html=True)

# --- SECCIÓN PRIVADA: PANEL DE CONTROL ---
elif menu == "📊 Panel RXS (Privado)":
    st.title("🔐 Acceso Restringido")
    
    if 'autorizado' not in st.session_state:
        st.session_state['autorizado'] = False

    if not st.session_state['autorizado']:
        clave = st.text_input("Clave Maestra", type="password")
        if st.button("Entrar al Panel"):
            if clave == "RS2026":
                st.session_state['autorizado'] = True
                st.rerun()
            else:
                st.error("Clave incorrecta")
    else:
        # AQUÍ APARECE TU DISEÑO PRO DE LOS CORAZONES Y LOS $1,914
        st.success("Bienvenida, Yajaira")
        st.markdown("<h2 style='text-align: center; color: #FF69B4;'>💖 RESUMEN RXS 💖</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        col1.metric("Servicios", "12")
        col2.metric("Total en Cuenta", "$1,914.00")
        
        st.write("---")
        if st.button("Cerrar Sesión"):
            st.session_state['autorizado'] = False
            st.rerun()
