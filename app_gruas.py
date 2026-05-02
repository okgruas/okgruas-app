import streamlit as st
import urllib.parse

# 1. Configuración de página
st.set_page_config(page_title="OKGRUAS RS", page_icon="🚛")

# 2. Estilo RXS
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .stButton>button { background-color: #FF69B4; color: white; border-radius: 10px; font-weight: bold; width: 100%; }
    label { color: #FF69B4 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Menú Lateral
menu = st.sidebar.radio("Ir a:", ["📱 Cotizador Público", "📊 Panel RXS (Privado)"])

# --- SECCIÓN 1: COTIZADOR (PÚBLICO) ---
if menu == "📱 Cotizador Público":
    st.title("🚛 OKGRUAS RS")
    st.write("### Solicita tu grúa en Monterrey")
    
    with st.form("form_cliente"):
        nombre = st.text_input("¿A nombre de quién?")
        vehiculo = st.text_input("¿Qué auto es? (Modelo y Color)")
        ubicacion = st.text_input("¿Dónde se encuentra?")
        btn_cliente = st.form_submit_button("📩 SOLICITAR AHORA")
        
    if btn_cliente:
        msj = f"*NUEVA SOLICITUD*\nCliente: {nombre}\nAuto: {vehiculo}\nUbicación: {ubicacion}"
        link = f"https://wa.me/528143029578?text={urllib.parse.quote(msj)}"
        st.markdown(f' <a href="{link}" target="_blank"><button style="width:100%; background-color:#25D366; border:none; padding:10px; color:white; border-radius:10px; cursor:pointer;">✅ ENVIAR WHATSAPP</button></a>', unsafe_allow_html=True)

# --- SECCIÓN 2: PANEL ADMIN (CON CONTRASEÑA) ---
elif menu == "📊 Panel RXS (Privado)":
    if 'auth' not in st.session_state:
        st.session_state['auth'] = False

    if not st.session_state['auth']:
        st.subheader("🔐 Acceso Restringido")
        clave = st.text_input("Clave Maestra", type="password")
        if st.button("Entrar"):
            if clave == "RS2026":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Clave incorrecta")
    else:
        # AQUÍ TU DISEÑO DE LOS $1,914
        st.markdown("<h2 style='text-align: center; color: #FF69B4;'>💖 RESUMEN RXS 💖</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        col1.metric("Servicios Hoy", "12")
        col2.metric("Total en Cuenta", "$1,914.00")
        
        if st.button("Cerrar Sesión"):
            st.session_state['auth'] = False
            st.rerun()
