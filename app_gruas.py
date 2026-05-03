import streamlit as st
import urllib.parse
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="OKGRUAS RS Control", page_icon="🚛", layout="wide")

# Estilos CSS (Verde Neón y Tipografía Montserrat)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        background-color: #121212;
        color: #FFFFFF;
    }
    .stMetric {
        background-color: #1e1e1e;
        border: 1px solid #00FF00;
        padding: 15px;
        border-radius: 10px;
    }
    .option-box {
        background-color: #1e1e1e;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #00FF00;
        margin-bottom: 10px;
    }
    h1, h2, h3 {
        color: #00FF00 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CANDADO INICIAL
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.markdown("<h1 style='text-align: center;'>🔐 ACCESO RESTRINGIDO</h1>", unsafe_allow_html=True)
    col_lock1, col_lock2, col_lock3 = st.columns([1,2,1])
    with col_lock2:
        clave_maestra = st.text_input("Introduce Clave de Acceso", type="password")
        if st.button("INGRESAR"):
            if clave_maestra == "RS2026":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Clave incorrecta")
    st.stop()

# 3. CABECERA (LOGO + NOMBRE OKGRUAS RS)
col_head1, col_head2 = st.columns([1, 5])

with col_head1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=100)
    else:
        st.markdown("<h1 style='margin:0;'>🚛</h1>", unsafe_allow_html=True)

with col_head2:
    # AQUÍ REINCORPORAMOS EL NOMBRE EN GRANDE
    st.markdown("<h1 style='margin-bottom: 0px; padding-top: 10px;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; margin-top: 0px;'>Gestión y Control de Servicios</p>", unsafe_allow_html=True)

st.divider()

# 4. ENTRADA DE DATOS
col_in, col_res = st.columns(2)

with col_in:
    st.subheader("📍 DATOS DEL SERVICIO")
    km = st.number_input("Kilómetros Recorridos:", min_value=0.0, value=10.0, step=1.0)
    
    st.markdown("<div class='option-box'>", unsafe_allow_html=True)
    c_opt1, c_opt2 = st.columns(2)
    with c_opt1:
        sotano = st.checkbox("🔦 ¿Es Sótano?")
    with c_opt2:
        falla = st.checkbox("🔧 Falla Mecánica")
    st.markdown("</div>", unsafe_allow_html=True)
    
    pisos = st.number_input("Niveles de sótano:", min_value=0) if sotano else 0

# LÓGICA DE CÁLCULOS
subtotal = 900.0 + (km * 25.0) + (pisos * 350.0) + (350.0 if falla else 0)
total_iva = subtotal * 1.16
utilidad_yaja = subtotal * 0.15
pago_socio = subtotal - utilidad_yaja

with col_res:
    st.subheader("💰 COTIZACIÓN CLIENTE")
    st.metric("TOTAL A COBRAR (C/IVA)", f"${total_iva:,.2f}")
    st.markdown(f"<p style='color: #888;'>Subtotal: ${subtotal:,.2f}</p>", unsafe_allow_html=True)

# 5. WHATSAPP (Configurado al 8143029578)
st.divider()
mi_numero = "528143029578"
texto_ws = f"*OKGRUAS RS - REPORTE*\n📍 KM: {km}\n💵 Total: ${total_iva:,.2f}"

link_ws = f"https://wa.me/{mi_numero}?text={urllib.parse.quote(texto_ws)}"
st.markdown(f'<a href="{link_ws}" target="_blank"><button style="width:100%; background-color:#25d366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer; font-size:18px;">📲 ENVIAR REPORTE WHATSAPP</button></a>', unsafe_allow_html=True)

# 6. ACCESO ADMINISTRATIVO (Clave RS2014)
st.write("")
with st.expander("🔐 Configuración Avanzada"):
    clave_admin = st.text_input("Clave Administrativa", type="password", key="admin_key")
    if clave_admin == "RS2014":
        st.subheader("📊 RENDIMIENTO PRIVADO")
        c1, c2 = st.columns(2)
        c1.metric("TU UTILIDAD (15%)", f"${utilidad_yaja:,.2f}")
        c2.metric("PAGO A SOCIO", f"${pago_socio:,.2f}")
        
        texto_privado = texto_ws + f"\n\n*INFO PRIVADA*\n💎 Ganancia: ${utilidad_yaja:,.2f}"
        link_privado = f"https://wa.me/{mi_numero}?text={urllib.parse.quote(texto_privado)}"
        st.markdown(f'<a href="{link_privado}" target="_blank" style="color: #00FF00;">➡️ Enviar Reporte con Ganancia</a>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #444; font-size: 10px; margin-top: 50px;'>OKGRUAS RS v2.0</p>", unsafe_allow_html=True)
