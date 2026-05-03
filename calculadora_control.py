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
    div[data-testid="stExpander"] {
        border: 1px solid #333;
        background-color: #1a1a1a;
        border-radius: 10px;
    }
    .option-box {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #00FF00;
        margin-bottom: 10px;
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
col_header1, col_header2 = st.columns([1, 4])
with col_header1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        st.markdown("<h2 style='color: #00FF00;'>RS</h2>", unsafe_allow_html=True)

with col_header2:
    st.markdown("<h1 style='color: #00FF00; margin-bottom: 0;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; margin-top: 0;'>Panel de Control Ejecutivo</p>", unsafe_allow_html=True)

st.divider()

# 4. ENTRADA DE DATOS
col_in, col_res = st.columns(2)

with col_in:
    st.markdown("<h3 style='color: #00FF00;'>📍 DATOS DEL SERVICIO</h3>", unsafe_allow_html=True)
    
    # Campo para el nombre del cliente (opcional para el reporte)
    cliente_nombre = st.text_input("Nombre del Cliente (Opcional):")
    
    km = st.number_input("Kilómetros Recorridos:", min_value=0.0, value=10.0, step=1.0)
    
    # NUEVA SECCIÓN: TIPO DE FALLA (Con la flechita / Dropdown)
    tipo_falla = st.selectbox("Selecciona el Tipo de Falla:", [
        "Falla Mecánica",
        "Choque / Siniestro",
        "Llanta Ponchada",
        "Sin Batería",
        "Auto Bloqueado",
        "Maniobra Especial"
    ])
    
    st.markdown("<div class='option-box'>", unsafe_allow_html=True)
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        sotano = st.checkbox("🔦 ¿Es Sótano?")
    with col_opt2:
        falla_extra = st.checkbox("🔧 ¿Falla en Ruedas/Eje?")
    st.markdown("</div>", unsafe_allow_html=True)
    
    pisos = st.number_input("Niveles de sótano:", min_value=0) if sotano else 0

# LÓGICA DE CÁLCULOS
# Nota: La lógica suma el extra de falla si se marca el checkbox manual
subtotal = 900.0 + (km * 25.0) + (pisos * 350.0) + (350.0 if falla_extra else 0)
total_iva = subtotal * 1.16
utilidad_yaja = subtotal * 0.15
pago_socio = subtotal - utilidad_yaja

with col_res:
    st.markdown("<h3 style='color: #00FF00;'>💰 COTIZACIÓN CLIENTE</h3>", unsafe_allow_html=True)
    st.metric("TOTAL A COBRAR (C/IVA)", f"${total_iva:,.2f}")
    st.markdown(f"<p style='color: #888;'>Subtotal: ${subtotal:,.2f}</p>", unsafe_allow_html=True)
    st.write(f"**Servicio:** {tipo_falla}")

# 5. WHATSAPP (Configurado al 8143029578)
st.divider()
fecha_txt = datetime.now().strftime("%d/%m/%Y")
mi_numero = "528143029578"

# Texto del reporte mejorado con el tipo de falla
texto_ws = f"*OKGRUAS RS - REPORTE*\n📅 Fecha: {fecha_txt}\n👤 Cliente: {cliente_nombre if cliente_nombre else 'General'}\n🛠️ Servicio: {tipo_falla}\n📍 KM: {km}\n💵 Total: ${total_iva:,.2f}"

link_ws = f"https://wa.me/{mi_numero}?text={urllib.parse.quote(texto_ws)}"
st.markdown(f'<a href="{link_ws}" target="_blank"><button style="width:100%; background-color:#25d366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer; font-size:18px;">📲 ENVIAR REPORTE WHATSAPP</button></a>', unsafe_allow_html=True)

# 6. ACCESO ADMINISTRATIVO
st.write("")
with st.expander("🔐 Acceso Administrativo (Solo Yajaira)"):
    clave_admin = st.text_input("Introduce Clave Administrativa", type="password", key="admin_key")
    if clave_admin == "RS2014":
        st.markdown("<h3 style='color: #00FF00;'>📊 RENDIMIENTO PRIVADO</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("TU UTILIDAD (15%)", f"${utilidad_yaja:,.2f}")
        with c2:
            st.metric("PAGO A SOCIO", f"${pago_socio:,.2f}")
        
        texto_privado = texto_ws + f"\n\n*INFO PRIVADA*\n💎 Ganancia: ${utilidad_yaja:,.2f}\n🚛 Socio: ${pago_socio:,.2f}"
        link_privado = f"https://wa.me/{mi_numero}?text={urllib.parse.quote(texto_privado)}"
        st.markdown(f'<a href="{link_privado}" target="_blank" style="color: #00FF00; text-decoration: none;">➡️ Enviar Reporte con Ganancia</a>', unsafe_allow_html=True)
    elif clave_admin != "":
        st.error("Clave de administrador incorrecta")

st.markdown("<p style='text-align: center; color: #444; font-size: 10px;'>OKGRUAS RS v2.1 - 2026</p>", unsafe_allow_html=True)
