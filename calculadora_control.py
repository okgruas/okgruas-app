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
st.markdown("<p style='color: #888; margin-top: 0;'>Cotizador Directo - Monterrey</p>", unsafe_allow_html=True)
st.divider()

# 4. ENTRADA DE DATOS
col_in, col_res = st.columns([3, 2])

with col_in:
    st.markdown("<h3 style='color: #00FF00;'>📍 DATOS DEL SERVICIO</h3>", unsafe_allow_html=True)
    
    cliente_nombre = st.text_input("Nombre del Cliente:")
    
    col_km1, col_km2 = st.columns(2)
    with col_km1:
        km = st.number_input("Kilómetros Recorridos:", min_value=0.0, value=0.0, step=1.0)
    with col_km2:
        costo_km_personalizado = st.number_input("Costo por KM Extra ($):", min_value=0.0, value=25.0, step=1.0)
    
    tipo_falla = st.selectbox("Tipo de Falla:", [
        "Falla Mecánica", "Choque / Siniestro", "Llanta Ponchada", 
        "Sin Batería", "Auto Bloqueado", "Maniobra Especial"
    ])

    st.markdown("---")
    st.markdown("**🔧 Maniobras Extras ($350 c/u)**")
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1: m_volante = st.checkbox("Volante/Llantas trabadas")
    with c_m2: m_neutral = st.checkbox("No entra Neutral")
    with c_m3: m_especial = st.checkbox("Maniobra Especial")

    st.markdown("---")
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        sotano = st.checkbox("🔦 ¿Es Sótano?")
    with col_s2:
        pisos = st.number_input("¿Cuántos niveles de sótano?", min_value=0, step=1) if sotano else 0

# LÓGICA DE CÁLCULOS (SIN IVA)
BANDERAZO = 800.0
COSTO_RECORRIDO = km * costo_km_personalizado
COSTO_MANIOBRAS = (350.0 if m_volante else 0) + (350.0 if m_neutral else 0) + (350.0 if m_especial else 0)
COSTO_SOTANO = pisos * 350.0

total_final = BANDERAZO + COSTO_RECORRIDO + COSTO_MANIOBRAS + COSTO_SOTANO

# 5. RESULTADOS VISIBLES
with col_res:
    st.markdown("<h3 style='color: #00FF00;'>📋 DESGLOSE NETO</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🏁 Banderazo: <b>$800.00</b></div>", unsafe_allow_html=True)
    
    if km > 0:
        st.markdown(f"<div class='price-tag'>🛣️ Recorrido ({km} km x ${costo_km_personalizado}): <b>${COSTO_RECORRIDO:,.2f}</b></div>", unsafe_allow_html=True)
    
    if COSTO_MANIOBRAS > 0:
        st.markdown(f"<div class='price-tag'>🔧 Maniobras extras: <b>${COSTO_MANIOBRAS:,.2f}</b></div>", unsafe_allow_html=True)
    
    if pisos > 0:
        st.markdown(f"<div class='price-tag'>🔦 Sótano ({pisos} pisos): <b>${COSTO_SOTANO:,.2f}</b></div>", unsafe_allow_html=True)
    
    st.divider()
    st.metric("TOTAL A COBRAR", f"${total_final:,.2f}")
    st.caption("Precios netos (Sin IVA)")

# 6. WHATSAPP
st.divider()
fecha_txt = datetime.now().strftime("%d/%m/%Y")
mi_numero = "528143029578"

texto_ws = (f"*OKGRUAS RS - COTIZACIÓN*\n"
            f"📅 Fecha: {fecha_txt}\n"
            f"👤 Cliente: {cliente_nombre if cliente_nombre else 'General'}\n"
            f"🛠️ Falla: {tipo_falla}\n"
            f"--------------------------\n"
            f"✅ Banderazo: $800\n"
            f"📍 KM ({km}): ${COSTO_RECORRIDO:,.2f}\n"
            f"🔧 Maniobras/Sótano: ${COSTO_MANIOBRAS + COSTO_SOTANO:,.2f}\n"
            f"--------------------------\n"
            f"💰 *TOTAL: ${total_final:,.2f}*")

link_ws = f"https://wa.me/{mi_numero}?text={urllib.parse.quote(texto_ws)}"
st.markdown(f'<a href="{link_ws}" target="_blank"><button style="width:100%; background-color:#25d366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer; font-size:18px;">📲 ENVIAR COTIZACIÓN WHATSAPP</button></a>', unsafe_allow_html=True)

# 7. ADMINISTRACIÓN
utilidad_yaja = total_final * 0.15
pago_socio = total_final - utilidad_yaja

with st.expander("📊 Rendimiento Privado"):
    clave_admin = st.text_input("Clave Admin", type="password")
    if clave_admin == "RS2014":
        c1, c2 = st.columns(2)
        with c1: st.metric("TU GANANCIA (15%)", f"${utilidad_yaja:,.2f}")
        with c2: st.metric("PAGO A SOCIO", f"${pago_socio:,.2f}")
        
        texto_admin = texto_ws + f"\n\n*INTERNO*\n💎 Ganancia: ${utilidad_yaja:,.2f}\n🚛 Socio: ${pago_socio:,.2f}"
        link_admin = f"https://wa.me/{mi_numero}?text={urllib.parse.quote(texto_admin)}"
        st.markdown(f'<a href="{link_admin}" target="_blank" style="color: #00FF00; text-decoration: none;">➡️ Reporte Interno</a>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #444; font-size: 10px;'>OKGRUAS RS v2.3 - Neto</p>", unsafe_allow_html=True)
