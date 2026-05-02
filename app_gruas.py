import streamlit as st
import urllib.parse

# 1. Configuración de página
st.set_page_config(page_title="OKGRUAS RS", page_icon="🚛")

# 2. Estilo RXS (Colores de tu marca)
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .stButton>button { background-color: #FF69B4; color: white; border-radius: 10px; font-weight: bold; width: 100%; }
    label { color: #FF69B4 !important; font-weight: bold; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #FF69B4; }
    </style>
    """, unsafe_allow_html=True)

# 3. Menú Lateral
menu = st.sidebar.radio("Ir a:", ["📱 Cotizador Público", "📊 Panel RXS (Privado)"])

# --- SECCIÓN 1: COTIZADOR (PÚBLICO) ---
if menu == "📱 Cotizador Público":
    st.markdown("<h1 style='color: white;'>🚛 OKGRUAS RS</h1>", unsafe_allow_html=True)
    st.write("### Solicita tu grúa en Monterrey")
    
    with st.form("form_cliente"):
        nombre = st.text_input("¿A nombre de quién?")
        vehiculo = st.text_input("¿Qué auto es? (Modelo y Color)")
        ubicacion = st.text_input("¿Dónde se encuentra?")
        btn_cliente = st.form_submit_button("📩 SOLICITAR AHORA")
        
    if btn_cliente:
        msj = f"*NUEVA SOLICITUD*\nCliente: {nombre}\nAuto: {vehiculo}\nUbicación: {ubicacion}"
        link = f"https://wa.me/528143029578?text={urllib.parse.quote(msj)}"
        st.markdown(f' <a href="{link}" target="_blank"><button style="width:100%; background-color:#25D366; border:none; padding:10px; color:white; border-radius:10px; cursor:pointer; font-weight:bold;">✅ ENVIAR WHATSAPP</button></a>', unsafe_allow_html=True)

# --- SECCIÓN 2: PANEL ADMIN (DISEÑO RXS DE LA FOTO) ---
elif menu == "📊 Panel RXS (Privado)":
    if 'auth' not in st.session_state:
        st.session_state['auth'] = False

    if not st.session_state['auth']:
        st.subheader("🔐 Acceso Administrativo")
        clave = st.text_input("Clave Maestra", type="password")
        if st.button("Entrar"):
            if clave == "RS2026":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Clave incorrecta")
    else:
        # AQUÍ ESTÁ TU DISEÑO DE LA FOTO (Corazones y dinero)
        st.markdown("<h2 style='text-align: center; color: #FF69B4;'>💖 OKGRUAS RS - PANEL 💖</h2>", unsafe_allow_html=True)
        st.write("Panel de Control de Servicios | Monterrey")
        
        # El bloque de los $1,914 que querías proteger
        st.write("### 💰 Resumen de Cuenta")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("TOTAL A COBRAR (IVA)", "$1,914.00")
        with col2:
            st.metric("SUBTOTAL", "$1,650.00")
            
        st.write("---")
        st.write("📍 **Detalles del Viaje**")
        km = st.number_input("Kilómetros totales:", value=30)
        
        col_c1, col_c2 = st.columns(2)
        col_c1.checkbox("📍 ¿Es Sótano?")
        col_c2.checkbox("🔧 ¿Falla Mecánica?")

        if st.button("Cerrar Sesión"):
            st.session_state['auth'] = False
            st.rerun()
