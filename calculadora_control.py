import streamlit as st
import urllib.parse
from datetime import datetime

# 1. CONFIGURACIÓN PROFESIONAL
st.set_page_config(page_title="OKGRUAS RS Control", page_icon="🚛", layout="wide")

# Candado de seguridad (Con los colores de antes)
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.markdown("<h1 style='color: #FF69B4; text-align: center;'>🔐 Acceso Administrativo</h1>", unsafe_allow_html=True)
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

# Estilos (Modo Oscuro y Neón Rosa Recuperados)
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .stMetric { background-color: #1e1e1e; border: 1px solid #FF69B4; padding: 15px; border-radius: 10px; color: white; }
    .stNumberInput, .stCheckbox { background-color: #1e1e1e; color: white; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# TÍTULO LIMPIO (Sin corazoncito)
st.markdown("<h1 style='color: #FF69B4;'>🚛 OKGRUAS RS - Panel de Control</h1>", unsafe_allow_html=True)

# --- ENTRADA DE DATOS ---
col_in, col_res = st.columns(2)

with col_in:
    st.markdown("<h3 style='color: #FF69B4;'>📍 Detalles del Servicio</h3>", unsafe_allow_html=True)
    km = st.number_input("Kilómetros totales:", min_value=0.0, value=10.0)
    col1, col2 = st.columns(2)
    with col1:
        sotano = st.checkbox("📍 ¿Es Sótano?")
    with col2:
        falla = st.checkbox("🔧 ¿Falla Mecánica?")
    
    pisos = st.number_input("Niveles de sótano:", min_value=0) if sotano else 0

# --- LÓGICA DE CÁLCULOS ---
subtotal = 900.0 + (km * 25.0) + (pisos * 350.0) + (350.0 if falla else 0)
total_iva = subtotal * 1.16
utilidad_yaja = subtotal * 0.15
pago_socio = subtotal - utilidad_yaja

with col_res:
    st.markdown("<h3 style='color: #FF69B4;'>💰 Resumen para Cobro</h3>", unsafe_allow_html=True)
    st.metric("TOTAL A COBRAR (IVA)", f"${total_iva:,.2f}")
    st.caption(f"Subtotal: ${subtotal:,.2f}")

# --- PROTECCIÓN DE GANANCIA (Tú lo ves, él no) ---
if modo == "💎 Modo Administrador":
    st.divider()
    st.markdown("<h3 style='color: #FF69B4;'>📊 Rendimiento Real (Privado)</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.metric("TU UTILIDAD (15%)", f"${utilidad_yaja:,.2f}")
    with c2:
        st.metric("PAGO A SOCIO", f"${pago_socio:,.2f}")
else:
    # Si no es modo admin, no se ve nada de dinero extra
    st.info("🔒 Los datos de rendimiento están ocultos en esta vista.")

# --- WHATSAPP (Con tu número 8143029578 y modo admin protegido) ---
st.divider()
fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
numero_whatsapp = "528143029578" # Número actualizado

# Texto que se enviará
texto_ws = f"*TICKET OKGRUAS RS*\n📅 Fecha: {fecha_actual}\n📍 KM: {km}\n💵 Cobro Total: ${total_iva:,.2f}"

# Si estás en modo admin, el WhatsApp que te manden también dirá cuánto ganaste
if modo == "💎 Modo Administrador":
    texto_ws += f"\n\n*REPORTE INTERNO*\n💎 Ganancia: ${utilidad_yaja:,.2f}\n🚛 Socio: ${pago_socio:,.2f}"

link_ws = f"https://wa.me/{numero_whatsapp}?text={urllib.parse.quote(texto_ws)}"
st.markdown(f'<a href="{link_ws}" target="_blank"><button style="width:100%; background-color:#25d366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">📲 ENVIAR REPORTE</button></a>', unsafe_allow_html=True)