import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime
import os

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="OKGRUAS RS - Control Total", page_icon="🚛", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; background-color: #121212; color: #FFFFFF; }
    .stMetric { background-color: #1e1e1e; border: 1px solid #00FF00; padding: 15px; border-radius: 10px; }
    .price-tag { background-color: #262626; padding: 10px; border-radius: 5px; border-left: 3px solid #00FF00; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE ARCHIVOS (ANTI-ERRORES)
ARCHIVO_REGISTRO = "registro_asistencias.csv"
COLUMNAS = ["Folio", "Fecha", "Cliente", "WhatsApp", "Falla", "KM", "Maniobras", "Total"]

def inicializar_y_registrar(datos=None):
    try:
        if not os.path.exists(ARCHIVO_REGISTRO):
            pd.DataFrame(columns=COLUMNAS).to_csv(ARCHIVO_REGISTRO, index=False)
        df = pd.read_csv(ARCHIVO_REGISTRO)
    except:
        # Si el archivo falla (error rojo), lo reiniciamos limpio
        pd.DataFrame(columns=COLUMNAS).to_csv(ARCHIVO_REGISTRO, index=False)
        df = pd.read_csv(ARCHIVO_REGISTRO)
    
    if datos:
        siguiente_num = len(df) + 1
        folio_nuevo = f"RS2014-{siguiente_num}"
        datos["Folio"] = folio_nuevo
        # Convertimos a DataFrame asegurando el orden de las columnas
        nuevo_df = pd.DataFrame([datos])[COLUMNAS]
        nuevo_df.to_csv(ARCHIVO_REGISTRO, mode='a', header=False, index=False)
        return folio_nuevo
    
    return f"RS2014-{len(df) + 1}"

# 3. ACCESO RESTRINGIDO
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    st.markdown("<h1 style='color: #00FF00; text-align: center;'>🔐 ACCESO RS</h1>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1,2,1])
    with col_l2:
        if st.text_input("Clave", type="password") == "RS2026":
            if st.button("ENTRAR"):
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# 4. CAPTURA DE DATOS (CON TODAS LAS MANIOBRAS)
st.markdown("<h1 style='color: #00FF00;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
st.divider()

col_in, col_res = st.columns([3, 2])

with col_in:
    st.markdown("### 📍 DATOS DEL SERVICIO")
    c1, c2 = st.columns(2)
    with c1: cliente_input = st.text_input("Nombre del Cliente:")
    with c2: whatsapp_input = st.text_input("WhatsApp (10 dígitos):")
    
    ck1, ck2 = st.columns(2)
    with ck1: km_input = st.number_input("Kilómetros:", min_value=0.0, step=1.0)
    with ck2: falla_input = st.selectbox("Falla:", ["Falla Mecánica", "Choque / Siniestro", "Llanta Ponchada", "Sin Batería", "Sótano"])
    
    st.markdown("**🔧 Maniobras Extras ($350 c/u)**")
    cm1, cm2, cm3 = st.columns(3)
    with cm1: m_volante = st.checkbox("Volante/Llantas")
    with cm2: m_neutral = st.checkbox("No entra Neutral")
    with cm3: m_especial = st.checkbox("Maniobra Especial")
    
    sotano_check = st.checkbox("🔦 ¿Es Sótano?")
    pisos_input = st.number_input("Niveles:", min_value=0, step=1) if sotano_check else 0

# CÁLCULOS
BANDERAZO = 800.0
COSTO_MAN = (350.0 if m_volante else 0) + (350.0 if m_neutral else 0) + (350.0 if m_especial else 0) + (pisos_input * 350.0)
TOTAL_FINAL = BANDERAZO + (km_input * 25.0) + COSTO_MAN

with col_res:
    st.markdown("### 📋 DESGLOSE")
    st.markdown(f"<div class='price-tag'>🏁 Banderazo: $800.00</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🛣️ Recorrido: ${km_input*25:,.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🔧 Maniobras: ${COSTO_MAN:,.2f}</div>", unsafe_allow_html=True)
    st.divider()
    st.metric("TOTAL NETO", f"${TOTAL_FINAL:,.2f}")
    st.caption(f"Siguiente Folio: {inicializar_y_registrar()}")

# 5. REGISTRO Y ENVÍO
st.divider()
if len(whatsapp_input) >= 10:
    if st.button("🚀 REGISTRAR Y GENERAR COTIZACIÓN", use_container_width=True):
        fecha_h = datetime.now().strftime("%d/%m/%Y %H:%M")
        # Diccionario con los datos capturados para el Excel
        info = {
            "Folio": "", 
            "Fecha": fecha_h, 
            "Cliente": cliente_input if cliente_input else "General",
            "WhatsApp": whatsapp_input, 
            "Falla": falla_input, 
            "KM": km_input,
            "Maniobras": COSTO_MAN, 
            "Total": TOTAL_FINAL
        }
        
        folio_real = inicializar_y_registrar(info)
        
        # MENSAJE WHATSAPP (SIN CARACTERES RAROS)
        msg_wa = (f"*OKGRUAS RS - COTIZACIÓN*\n"
                  f"🆔 *Folio: {folio_real}*\n"
                  f"👤 Cliente: {info['Cliente']}\n"
                  f"🛠️ Falla: {falla_input}\n"
                  f"💰 *TOTAL: ${TOTAL_FINAL:,.2f}*\n"
                  f"--------------------------\n"
                  f"Reportar a: 528143029578")
        
        link_wa = f"https://wa.me/52{whatsapp_input[-10:]}?text={urllib.parse.quote(msg_wa)}"
        
        st.success(f"✅ ¡Folio {folio_real} guardado exitosamente!")
        st.link_button("📲 ENVIAR POR WHATSAPP", link_wa, type="primary", use_container_width=True)
else:
    st.warning("⚠️ Ingresa el WhatsApp del cliente.")

# 6. PANEL ADMIN
with st.expander("📊 PANEL ADMINISTRATIVO"):
    if st.text_input("Clave Admin", type="password") == "RS2014":
        try:
            df_hist = pd.read_csv(ARCHIVO_REGISTRO)
            st.dataframe(df_hist)
            u_neta = df_hist["Total"].sum() * 0.15
            st.metric("TU GANANCIA (15%)", f"${u_neta:,.2f}")
            st.download_button("📥 DESCARGAR EXCEL", data=df_hist.to_csv(index=False).encode('utf-8'), file_name="servicios_rs.csv", mime="text/csv")
        except:
            st.error("No hay datos todavía.")
