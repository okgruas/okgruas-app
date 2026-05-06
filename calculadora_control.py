import streamlit as st
import urllib.parse
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="OKGRUAS RS Control", page_icon="🚛", layout="wide")

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
st.divider()

# 4. ENTRADA DE DATOS
col_in, col_res = st.columns([3, 2])

with col_in:
    st.markdown("<h3 style='color: #00FF00;'>📍 DATOS DEL SERVICIO</h3>", unsafe_allow_html=True)
    
    c_nom, c_tel = st.columns(2)
    with c_nom:
        cliente_nombre = st.text_input("Nombre del Cliente:")
    with c_tel:
        # Aquí escribes el número
        cliente_whatsapp = st.text_input("WhatsApp del Cliente (10 dígitos):", placeholder="8112345678")
    
    col_km1, col_km2 = st.columns(2)
    with col_km1:
        km = st.number_input("Kilómetros Recorridos:", min_value=0.0, value=0.0, step=1.0)
    with col_km2:
        costo_km_personalizado = st.number_input("Costo por KM Extra ($):", min_value=0.0, value=25.0, step=1.0)
    
    tipo_falla = st.selectbox("Tipo de Falla:", ["Falla Mecánica", "Choque / Siniestro", "Llanta Ponchada", "Sin Batería", "Auto Bloqueado", "Maniobra Especial"])

    st.markdown("---")
    st.markdown("**🔧 Maniobras Extras ($350 c/u)**")
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1: m_volante = st.checkbox("Volante/Llantas trabadas")
    with c_m2: m_neutral = st.checkbox("No entra Neutral")
    with c_m3: m_especial = st.checkbox("Maniobra Especial")

    st.markdown("---")
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1: sotano = st.checkbox("🔦 ¿Es Sótano?")
    with col_s2: pisos = st.number_input("¿Cuántos niveles?", min_value=0, step=1) if sotano else 0

# LÓGICA DE CÁLCULOS
BANDERAZO = 800.0
COSTO_RECORRIDO = km * costo_km_personalizado
COSTO_MANIOBRAS = (350.0 if m_volante else 0) + (350.0 if m_neutral else 0) + (350.0 if m_especial else 0)
COSTO_SOTANO = pisos * 350.0
total_final = BANDERAZO + COSTO_RECORRIDO + COSTO_MANIOBRAS + COSTO_SOTANO

# 5. RESULTADOS
with col_res:
    st.markdown("<h3 style='color: #00FF00;'>📋 DESGLOSE NETO</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🏁 Banderazo: <b>$800.00</b></div>", unsafe_allow_html=True)
    if km > 0: st.markdown(f"<div class='price-tag'>🛣️ Recorrido: <b>${COSTO_RECORRIDO:,.2f}</b></div>", unsafe_allow_html=True)
    if (COSTO_MANIOBRAS + COSTO_SOTANO) > 0: st.markdown(f"<div class='price-tag'>🔧 Maniobras/Sótano: <b>${(COSTO_MANIOBRAS + COSTO_SOTANO):,.2f}</b></div>", unsafe_allow_html=True)
    st.divider()
    st.metric("TOTAL A COBRAR", f"${total_final:,.2f}")

# 6. ENVÍO WHATSAPP
st.divider()
fecha_txt = datetime.now().strftime("%d/%m/%Y")
mi_numero = "528143029578"

texto_base = (f"*OKGRUAS RS - COTIZACIÓN*\n"
            f"📅 Fecha: {fecha_txt}\n"
            f"👤 Cliente: {cliente_nombre if cliente_nombre else 'General'}\n"
            f"🛠️ Falla: {tipo_falla}\n"
            f"--------------------------\n"
            f"✅ Banderazo: $800\n"
            f"📍 KM ({km}): ${COSTO_RECORRIDO:,.2f}\n"
            f"🔧 Maniobras: ${COSTO_MANIOBRAS + COSTO_SOTANO:,.2f}\n"
            f"--------------------------\n"
            f"💰 *TOTAL: ${total_final:,.2f}*")

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    # Si hay algo escrito en el número, limpiamos y preparamos el link
    clean_phone = "".join(filter(str.isdigit, cliente_whatsapp))
    if len(clean_phone) >= 10:
        num_final = "52" + clean_phone if len(clean_phone) == 10 else clean_phone
        link_c = f"https://wa.me/{num_final}?text={urllib.parse.quote(texto_base)}"
        st.markdown(f'<a href="{link_c}" target="_blank"><button style="width:100%; background-color:#25d366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">📲 ENVIAR AL CLIENTE</button></a>', unsafe_allow_html=True)
    else:
        # Botón deshabilitado visualmente si no hay número
        st.markdown(f'<button style="width:100%; background-color:#555; color:#aaa; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:not-allowed;">⚠️ FALTA NÚMERO DE CLIENTE</button>', unsafe_allow_html=True)

with col_btn2:
    link_m = f"https://wa.me/{mi_numero}?text={urllib.parse.quote('*COPIA* ' + texto_base)}"
    st.markdown(f'<a href="{link_m}" target="_blank"><button style="width:100%; background-color:#1e1e1e; color:#00FF00; border:1px solid #00FF00; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">📩 GUARDAR MI COPIA</button></a>', unsafe_allow_html=True)

# 7. ADMINISTRACIÓN
utilidad_yaja = total_final * 0.15
pago_socio = total_final - utilidad_yaja
with st.expander("📊 Rendimiento Privado"):
    clave_admin = st.text_input("Clave Admin", type="password")
    if clave_admin == "RS2014":
        c1, c2 = st.columns(2)
        with c1: st.metric("TU GANANCIA (15%)", f"${utilidad_yaja:,.2f}")
        with c2: st.metric("PAGO A SOCIO", f"${pago_socio:,.2f}")
        link_a = f"https://wa.me/{mi_numero}?text={urllib.parse.quote(texto_base + f' - Ganancia: ${utilidad_yaja}')}"
        st.markdown(f'<a href="{link_a}" target="_blank" style="color:#00FF00;">➡️ Reporte Completo</a>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #444; font-size: 10px;'>OKGRUAS RS v2.6</p>", unsafe_allow_html=True)
