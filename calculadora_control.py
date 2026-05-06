import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime
import os

# 1. CONFIGURACIÓN Y ESTILO PROFESIONAL
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

# 2. SISTEMA DE BASE DE DATOS MEJORADO
ARCHIVO_REGISTRO = "registro_asistencias.csv"

def inicializar_base_datos():
    # Creamos las columnas exactas para que el Excel sea profesional
    if not os.path.exists(ARCHIVO_REGISTRO):
        columnas = ["Folio", "Fecha", "Cliente", "WhatsApp", "Falla", "KM", "Maniobras", "Total", "Estado"]
        df_vacio = pd.DataFrame(columns=columnas)
        df_vacio.to_csv(ARCHIVO_REGISTRO, index=False)

def registrar_servicio(datos):
    inicializar_base_datos()
    df = pd.read_csv(ARCHIVO_REGISTRO)
    
    # Generar folio consecutivo real
    siguiente_num = len(df) + 1
    nuevo_folio = f"RS2014-{siguiente_num}"
    
    datos["Folio"] = nuevo_folio
    nuevo_df = pd.DataFrame([datos])
    # Guardar inmediatamente
    nuevo_df.to_csv(ARCHIVO_REGISTRO, mode='a', header=False, index=False)
    return nuevo_folio

# 3. ACCESO RESTRINGIDO
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    st.markdown("<h1 style='color: #00FF00; text-align: center;'>🔐 ACCESO RS</h1>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1,2,1])
    with col_l2:
        clave = st.text_input("Clave de Acceso", type="password")
        if st.button("ENTRAR"):
            if clave == "RS2026":
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# 4. INTERFAZ DE USUARIO
st.markdown("<h1 style='color: #00FF00; margin-bottom: 0;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #888;'>Panel de Control de Cotizaciones</p>", unsafe_allow_html=True)
st.divider()

col_in, col_res = st.columns([3, 2])

with col_in:
    st.markdown("<h3 style='color: #00FF00;'>📍 DATOS DEL SERVICIO</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: cliente = st.text_input("Nombre del Cliente:")
    with c2: tel_cliente = st.text_input("WhatsApp Cliente (10 dígitos):")
    
    ck1, ck2 = st.columns(2)
    with ck1: km = st.number_input("KM Recorridos:", min_value=0.0, step=1.0)
    with ck2: costo_km = st.number_input("Costo por KM ($):", min_value=0.0, value=25.0)
    
    falla = st.selectbox("Tipo de Falla:", ["Falla Mecánica", "Choque / Siniestro", "Llanta Ponchada", "Sin Batería", "Auto Bloqueado", "Maniobra Especial"])
    
    st.markdown("**🔧 Maniobras Extras ($350 c/u)**")
    cm1, cm2, cm3 = st.columns(3)
    with cm1: m1 = st.checkbox("Volante/Llantas")
    with cm2: m2 = st.checkbox("No entra Neutral")
    with cm3: m3 = st.checkbox("Especial")
    
    sotano = st.checkbox("🔦 ¿Es Sótano?")
    pisos = st.number_input("Niveles:", min_value=0, step=1) if sotano else 0

# CÁLCULOS
BANDERAZO = 800.0
TOTAL_KM = km * costo_km
TOTAL_MAN = (350.0 if m1 else 0) + (350.0 if m2 else 0) + (350.0 if m3 else 0) + (pisos * 350.0)
TOTAL_NETO = BANDERAZO + TOTAL_KM + TOTAL_MAN

with col_res:
    st.markdown("<h3 style='color: #00FF00;'>📋 DESGLOSE</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🏁 Banderazo: <b>$800.00</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🛣️ Recorrido: <b>${TOTAL_KM:,.2f}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🔧 Maniobras: <b>${TOTAL_MAN:,.2f}</b></div>", unsafe_allow_html=True)
    st.divider()
    st.metric("TOTAL NETO", f"${TOTAL_NETO:,.2f}")

# 5. REGISTRO Y ENVÍO AUTOMÁTICO
st.divider()
if len(tel_cliente) >= 10:
    # BOTÓN ÚNICO: Registra y luego permite enviar
    if st.button("🚀 REGISTRAR Y GENERAR WHATSAPP", use_container_width=True):
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Guardar en el Excel
        datos_para_excel = {
            "Folio": "", 
            "Fecha": fecha_actual,
            "Cliente": cliente if cliente else "General",
            "WhatsApp": tel_cliente,
            "Falla": falla,
            "KM": km,
            "Maniobras": TOTAL_MAN,
            "Total": TOTAL_NETO,
            "Estado": "Cotizado" # Aquí queda grabado que se hizo la cotización
        }
        
        folio_real = registrar_servicio(datos_para_excel)
        
        # Preparar mensaje para el socio/cliente
        texto_ws = (f"*OKGRUAS RS - COTIZACIÓN*\n"
                    f"🆔 *Folio: {folio_real}*\n"
                    f"📅 Fecha: {fecha_actual}\n"
                    f"👤 Cliente: {cliente if cliente else 'General'}\n"
                    f"🛠️ Falla: {falla}\n"
                    f"--------------------------\n"
                    f"✅ Banderazo: $800\n"
                    f"📍 KM ({km}): ${TOTAL_KM:,.2f}\n"
                    f"🔧 Maniobras: ${TOTAL_MAN:,.2f}\n"
                    f"--------------------------\n"
                    f"💰 *TOTAL: ${TOTAL_NETO:,.2f}*\n"
                    f"--------------------------\n"
                    f"Reportar a: 528143029578")
        
        num_dest = "52" + tel_cliente[-10:]
        link = f"https://wa.me/{num_dest}?text={urllib.parse.quote(texto_ws)}"
        
        st.success(f"✅ ¡Servicio {folio_real} grabado en el sistema!")
        st.link_button("📲 ENVIAR COTIZACIÓN POR WHATSAPP", link, type="primary", use_container_width=True)
else:
    st.warning("⚠️ Ingresa el número de WhatsApp para habilitar el botón.")

# 6. PANEL ADMIN YAJAIRA
with st.expander("🔐 PANEL DE AUDITORÍA"):
    adm_clave = st.text_input("Clave Admin", type="password")
    if adm_clave ==
