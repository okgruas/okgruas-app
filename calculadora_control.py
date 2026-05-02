import streamlit as st
import urllib.parse
from datetime import datetime

# 1. CONFIGURACIÓN PROFESIONAL
st.set_page_config(page_title="OKGRUAS RS Control", page_icon="🚛", layout="wide")

# Candado de seguridad
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.markdown("<h2 style='text-align: center;'>🔐 Acceso Administrativo</h2>", unsafe_allow_html=True)
    col_lock1, col_lock2, col_lock3 = st.columns([1,2,1])
    with col_lock2:
        clave = st.text_input("Introduce la clave maestra", type="password")
        if st.button("Ingresar"):
            if clave == "RS2026":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Clave incorrecta")
    st.stop()

# --- MENÚ LATERAL ---
st.sidebar.header("CONFIGURACIÓN")
modo = st.sidebar.radio("Tipo de Vista:", ["📱 Calculadora Estándar", "💎 Modo Administrador"])

# Estilos
st.markdown("<style>.stApp { background-color: #f0f2f6; } .stMetric { background-color: white; border-radius: 10px; padding: 20px; }</style>", unsafe_allow_html=True)

st.title("OKGRUAS RS - Panel de Control")

# --- ENTRADA DE DATOS ---
col_in, col_res = st.columns(2)

with col_in:
    st.subheader("📍 Detalles del Servicio")
    km = st.number_input("Kilómetros totales:", min_value=0.0, value=10.0)
    sotano = st.checkbox("📍 ¿Es Sótano?")
    falla = st.checkbox("🔧 ¿Falla Mecánica?")
    pisos = st.number_input("Niveles de sótano:", min_value=0) if sotano else 0

# --- LÓGICA DE CÁLCULOS ---
subtotal = 900.0 + (km * 25.0) + (pisos * 350.0) + (350.0 if falla else 0)
total_iva = subtotal * 1.16
utilidad_yaja = subtotal * 0.15
pago_socio = subtotal - utilidad_yaja

with col_res:
    st.subheader("💰 Resumen para Cobro")
    st.metric("TOTAL A COBRAR (IVA)", f"${total_iva:,.2f}")

# --- PROTECCIÓN DE GANANCIA (Solo tú lo ves) ---
if modo == "💎 Modo Administrador":
    st.divider()
    st.subheader("📊 Rendimiento Real (Privado)")
    c1, c2 = st.columns(2)
    c1.metric("TU UTILIDAD (15%)", f"${utilidad_yaja:,.2f}")
    c2.metric("PAGO A SOCIO", f"${pago_socio:,.2f}")
else:
    st.info("🔒 Los datos de rendimiento están ocultos.")

# --- WHATSAPP (Con tu número 8143029578) ---
st.divider()
texto_ws = f"*TICKET OKGRUAS RS*\n📍 KM: {km}\n💵 Cobro Total: ${total_iva:,.2f}"

# Si tú mandas el reporte desde el modo admin, también te llegará cuánto ganaste
if modo == "💎 Modo Administrador":
    texto_ws += f"\n\n*INFO PRIVADA*\nGanancia: ${utilidad_yaja:,.2f}"

# Tu número configurado
mi_numero = "528143029578" 
link_ws = f"https://wa.me/{mi_numero}?text={urllib.parse.quote(texto_ws)}"

st.markdown(f'<a href="{link_ws}" target="_blank"><button style="width:100%; background-color:#25d366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">📲 ENVIAR REPORTE</button></a>', unsafe_allow_html=True)