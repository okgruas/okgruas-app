import streamlit as st
import os
import urllib.parse
from datetime import datetime

# 1. CONFIGURACIÓN
st.set_page_config(page_title="OKGRUAS RS - Auxilio Vial", page_icon="🚛")

# Estilos para que se vea como una App profesional
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'version' not in st.session_state:
    st.session_state.version = 0

# --- 2. LOGO ---
col_l, col_r = st.columns([1, 2])
with col_l:
    for f in ["logo.png", "logo.pgn"]:
        if os.path.exists(f):
            st.image(f, width=120)
            break

# --- 3. MENÚ LATERAL ---
with st.sidebar:
    st.title("Sistema de Control")
    modo = st.radio("Sección:", ["🆘 Pedir Grúa", "📊 Admin"])
    st.write("---")
    if modo == "📊 Admin":
        pw = st.text_input("Contraseña:", type="password")
        if pw != "RS2026": # <--- Tu clave para que nadie más entre
            st.warning("Acceso restringido")
            st.stop()

# --- 4. VISTA DEL CLIENTE ---
if modo == "🆘 Pedir Grúa":
    st.header("¡Estamos para ayudarte!")
    st.subheader("Solicita tu grúa en Monterrey y alrededores")
    
    nombre = st.text_input("¿A nombre de quién?")
    vehiculo = st.text_input("¿Qué auto es? (Modelo y Color)")
    falla_txt = st.selectbox("¿Qué problema tiene?", ["Se quedó parado", "Choque", "Sótano", "Otro"])

    st.warning("Al presionar el botón se abrirá WhatsApp. **Envía el mensaje y luego comparte tu ubicación en tiempo real.**")
    
    # CONFIGURA TU NÚMERO AQUÍ ABAJO
    mi_numero = "528143029578" 
    msj = f"🆘 *NUEVA SOLICITUD DE GRÚA*\n\n👤 Cliente: {nombre}\n🚗 Auto: {vehiculo}\n🔧 Falla: {falla_txt}\n\n📍 *Esperando ubicación del cliente...*"
    link = f"https://wa.me/{mi_numero}?text={urllib.parse.quote(msj)}"
    
    if st.button("🚨 SOLICITAR GRÚA AHORA"):
        st.markdown(f'<meta http-equiv="refresh" content="0;URL={link}">', unsafe_allow_html=True)

# --- 5. VISTA DE ADMIN (Yajaira) ---
else:
    st.header("💎 Panel Administrativo")
    st.info("Aquí solo tú puedes ver las ganancias y gestionar socios.")
    
    t1, t2 = st.tabs(["Calculadora", "Socios"])
    
    with t1:
        km = st.number_input("Kilómetros:", min_value=0.0, value=10.0, key=f"k_{st.session_state.version}")
        c1, c2 = st.columns(2)
        sotano = c1.checkbox("Sótano", key=f"s_{st.session_state.version}")
        falla = c2.checkbox("Falla Mecánica", key=f"f_{st.session_state.version}")
        
        # Lógica de cobro de Monterrey
        subtotal = 900 + (km * 25) + (350 if sotano else 0) + (350 if falla else 0)
        total_iva = subtotal * 1.16
        ganancia = subtotal * 0.15
        pago_socio = subtotal - ganancia
        
        st.metric("Total Cliente (c/IVA)", f"${total_iva:,.2f}")
        
        col_a, col_b = st.columns(2)
        col_a.success(f"Tu Ganancia: ${ganancia:,.2f}")
        col_b.error(f"Socio recibe: ${pago_socio:,.2f}")

        if st.button("🔄 NUEVA COTIZACIÓN"):
            st.session_state.version += 1
            st.rerun()

    with t2:
        st.subheader("Control de Socios")
        st.text_input("Nombre del nuevo socio:")
        st.text_input("Eco de la grúa:")
        if st.button("Registrar Socio"):
            st.success("Socio agregado (Simulación)")