import streamlit as st
import urllib.parse
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="OKGRUAS RS Control", page_icon="🚛", layout="wide")

# Estilos CSS
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
    .price-tag {
        background-color: #262626;
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid #00FF00;
        margin-bottom: 5px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CANDADO INICIAL
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.markdown("<h1 style='color: #00FF00; text-align: center;'>🔐 ACCESO RESTRINGIDO</h1>", unsafe_allow_html=True)
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

# 3. CABECERA
st.markdown("<h1 style='color: #00FF00; margin-bottom: 0;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #888; margin-top: 0;'>Cotizador de Servicios Monterrey</p>", unsafe_allow_html=True)
st.divider()

# 4. ENTRADA DE DATOS
col_in, col_res = st.columns([3, 2])

with col_in:
    st.markdown("<h3 style='color: #00FF00;'>📍 DATOS DEL SERVICIO</h3>", unsafe_allow_html=True)
    
    cliente_nombre = st.text_input("Nombre del Cliente:")
    
    c_km, c_tipo = st.columns(2)
    with c_km:
        km = st.number_input("Kilómetros Recorridos:", min_value=0.0, value=0.0, step=1.0)
    with c_tipo:
        tipo_falla = st.selectbox("Tipo de Falla:", [
            "Falla Mecánica", "Choque / Siniestro", "Llanta Ponchada", 
            "Sin Batería", "Auto Bloqueado", "Maniobra Especial"
        ])

    st.markdown("---")
    st.markdown("**¿Requiere Maniobras Extras? ($350 c/u)**")
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        m_volante = st.checkbox("Volante/Llantas trabadas")
    with col_m2:
        m_neutral = st.checkbox("No se puede poner Neutral")
    with col_m3:
        m_especial = st.checkbox("Maniobra Especial")

    st.markdown("---")
    sotano = st.checkbox("🔦 ¿Es en Sótano?")
    pisos = st.number_input("¿Cuántos niveles de sótano?", min_value=0, step=1) if sotano else 0

# LÓGICA DE CÁLCULOS (PRECIOS VISIBLES)
BANDERAZO = 800.0
COSTO_KM = km * 25.0
# Sumamos 350 por cada maniobra seleccionada
total_maniobras = (350.0 if m_volante else 0) + (350.0 if m_neutral else 0) + (350.0 if m_especial else 0)
COSTO_SOTANO = pisos * 350.0

subtotal = BANDERAZO + COSTO_KM + total_maniobras + COSTO_SOTANO
total_iva = subtotal * 1.16

# 5. RESULTADOS VISIBLES
with col_res:
    st.markdown("<h3 style='color: #00FF00;'>📋 DESGLOSE</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🏁 Banderazo: <b>$800.00</b></div>", unsafe_allow_html=True)
    if km > 0:
        st.markdown(f"<div class='price-tag'>🛣️ Recorrido ({km} km): <b>${COSTO_KM:,.2f}</b></div>", unsafe_allow_html=True)
    if total_maniobras > 0:
        st.markdown(f"<div class='price-tag'>🔧 Maniobras extras: <b>${total_maniobras:,.2f}</b></div>", unsafe_allow_html=True)
    if pisos > 0:
        st.markdown(f"<div class='price-tag'>🔦 Sótano ({pisos} pisos): <b>${COSTO_SOTANO:,.2f}</b></div>", unsafe_allow_html=True)
    
    st.divider()
    st.metric("TOTAL A COBRAR (C/IVA)", f"${total_iva:,.2f}")
    st.write(f"**Subtotal:** ${subtotal:,.2f}")

# 6. WHATSAPP
st.divider()
fecha_txt = datetime.now().strftime("%d/%m/%Y")
mi_numero = "528143029578"

# Texto del reporte para el cliente
texto_ws = (f"*OKGRUAS RS - COTIZACIÓN*\n"
            f"📅 Fecha: {fecha_txt}\n"
            f"👤 Cliente: {cliente_nombre if cliente_nombre else 'General'}\n"
            f"🛠️ Servicio: {tipo_falla}\n"
            f"--------------------------\n"
            f"✅ Banderazo: $800\n"
            f"📍 KM ({km}): ${COSTO_KM}\n"
            f"🔧 Maniobras: ${total_maniobras + COSTO_SOTANO}\n"
            f"--------------------------\n"
            f"💰 *TOTAL C/IVA: ${total_iva:,.2f}*")

link_ws = f"https://wa.me/{mi_numero}?text={urllib.parse.quote(texto_ws)}"
st.markdown(f'<a href="{link_ws}" target="_blank"><button style="width:100%; background-color:#25d366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer; font-size:18px;">📲 ENVIAR COTIZACIÓN A WHATSAPP</button></a>', unsafe_allow_html=True)

# 7. ACCESO ADMINISTRATIVO
utilidad_yaja = subtotal * 0.15
pago_socio = subtotal - utilidad_yaja

with st.expander("🔐 Acceso Administrativo (Yajaira)"):
    clave_admin = st.text_input("Clave Administrativa", type="password")
    if clave_admin == "RS2014":
        st.markdown("<h3 style='color: #00FF00;'>📊 RENDIMIENTO</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.metric("TU GANANCIA (15%)", f"${utilidad_yaja:,.2f}")
        with c2: st.metric("PAGO A SOCIO", f"${pago_socio:,.2f}")
        
        texto_privado = texto_ws + f"\n\n*INFO INTERNA*\n💎 Utilidad: ${utilidad_yaja:,.2f}\n🚛 Socio: ${pago_socio:,.2f}"
        link_privado = f"https://wa.me/{mi_numero}?text={urllib.parse.quote(texto_privado)}"
        st.markdown(f'<a href="{link_privado}" target="_blank" style="color: #00FF00; text-decoration: none;">➡️ Enviar Reporte con Ganancia</a>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #444; font-size: 10px;'>OKGRUAS RS v2.2 - Monterrey</p>", unsafe_allow_html=True)
