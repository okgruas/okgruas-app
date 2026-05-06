import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime
import os

# 1. ESTILO PROFESIONAL RS
st.set_page_config(page_title="OKGRUAS RS - Control Total", page_icon="🚛", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; background-color: #121212; color: #FFFFFF; }
    .stMetric { background-color: #1e1e1e; border: 1px solid #00FF00; padding: 15px; border-radius: 10px; }
    .price-tag { background-color: #262626; padding: 10px; border-radius: 5px; border-left: 3px solid #00FF00; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE ARCHIVO (CREA COLUMNAS LIMPIAS)
ARCHIVO_REGISTRO = "registro_asistencias.csv"

def inicializar_y_registrar(datos=None):
    columnas = ["Folio", "Fecha", "Cliente", "WhatsApp", "Falla", "KM", "Maniobras", "Total"]
    if not os.path.exists(ARCHIVO_REGISTRO):
        df_base = pd.DataFrame(columns=columnas)
        df_base.to_csv(ARCHIVO_REGISTRO, index=False)
    
    df = pd.read_csv(ARCHIVO_REGISTRO)
    
    if datos:
        siguiente_num = len(df) + 1
        folio_nuevo = f"RS2014-{siguiente_num}"
        datos["Folio"] = folio_nuevo
        # Reordenar datos para que coincidan con las columnas
        nuevo_df = pd.DataFrame([datos])[columnas]
        nuevo_df.to_csv(ARCHIVO_REGISTRO, mode='a', header=False, index=False)
        return folio_nuevo
    
    return f"RS2014-{len(df) + 1}"

# 3. ACCESO
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    st.markdown("<h1 style='color: #00FF00; text-align: center;'>🔐 ACCESO RS</h1>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1,2,1])
    with col_l2:
        clave_input = st.text_input("Clave de Aplicación", type="password")
        if st.button("ENTRAR"):
            if clave_input == "RS2026":
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# 4. INTERFAZ DE CAPTURA
st.markdown("<h1 style='color: #00FF00;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
st.divider()

col_in, col_res = st.columns([3, 2])

with col_in:
    st.markdown("### 📍 DATOS DEL SERVICIO")
    c1, c2 = st.columns(2)
    with c1: cliente_n = st.text_input("Nombre del Cliente:")
    with c2: whatsapp_n = st.text_input("WhatsApp (10 dígitos):")
    
    ck1, ck2 = st.columns(2)
    with ck1: km_n = st.number_input("Kilómetros:", min_value=0.0, step=1.0)
    with ck2: falla_n = st.selectbox("Falla:", ["Mecánica", "Choque", "Llanta", "Batería", "Sótano"])
    
    st.markdown("**🔧 Maniobras Extras ($350 c/u)**")
    cm1, cm2 = st.columns(2)
    with cm1: m_volante = st.checkbox("Volante/Llantas trabadas")
    with cm2: m_neutral = st.checkbox("No entra Neutral")
    
    sotano_n = st.checkbox("🔦 ¿Es Sótano?")
    pisos_n = st.number_input("Niveles sótano:", min_value=0, step=1) if sotano_n else 0

# CÁLCULOS
COSTO_MANIOBRAS = (350.0 if m_volante else 0) + (350.0 if m_neutral else 0) + (pisos_n * 350.0)
TOTAL_CALCULADO = 800.0 + (km_n * 25.0) + COSTO_MANIOBRAS

with col_res:
    st.markdown("### 📋 DESGLOSE")
    st.markdown(f"<div class='price-tag'>🏁 Banderazo: $800.00</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🛣️ Recorrido: ${km_n*25:,.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🔧 Maniobras: ${COSTO_MANIOBRAS:,.2f}</div>", unsafe_allow_html=True)
    st.divider()
    st.metric("TOTAL NETO", f"${TOTAL_CALCULADO:,.2f}")
    st.caption(f"Próximo Folio: {inicializar_y_registrar()}")

# 5. BOTÓN DE REGISTRO AUTOMÁTICO
st.divider()
if len(whatsapp_n) >= 10:
    if st.button("🚀 REGISTRAR Y GENERAR COTIZACIÓN", use_container_width=True):
        fecha_asistencia = datetime.now().strftime("%d/%m/%Y %H:%M")
        datos_finales = {
            "Folio": "",
            "Fecha": fecha_asistencia,
            "Cliente": cliente_n if cliente_n else "General",
            "WhatsApp": whatsapp_n,
            "Falla": falla_n,
            "KM": km_n,
            "Maniobras": COSTO_MANIOBRAS,
            "Total": TOTAL_CALCULADO
        }
        
        folio_asig = inicializar_y_registrar(datos_finales)
        
        # MENSAJE DE WHATSAPP LIMPIO
        msg = (f"*OKGRUAS RS - COTIZACIÓN*\n"
               f"🆔 *Folio: {folio_asig}*\n"
               f"📅 Fecha: {fecha_asistencia}\n"
               f"👤 Cliente: {datos_finales['Cliente']}\n"
               f"💰 *TOTAL: ${TOTAL_CALCULADO:,.2f}*\n"
               f"--------------------------\n"
               f"Reportar a: 528143029578")
        
        link_wa = f"https://wa.me/52{whatsapp_n[-10:]}?text={urllib.parse.quote(msg)}"
        
        st.success(f"✅ ¡Folio {folio_asig} guardado en el Excel!")
        st.link_button("📲 ENVIAR POR WHATSAPP", link_wa, type="primary", use_container_width=True)
else:
    st.warning("⚠️ Ingresa el WhatsApp para habilitar el registro.")

# 6. PANEL ADMIN (CORREGIDO)
with st.expander("📊 PANEL ADMINISTRATIVO"):
    pass_admin = st.text_input("Clave Admin", type="password")
    if pass_admin == "RS2014":
        if os.path.exists(ARCHIVO_REGISTRO):
            df_final = pd.read_csv(ARCHIVO_REGISTRO)
            st.dataframe(df_final)
            
            ganancia = df_final["Total"].sum() * 0.15
            st.metric("TU GANANCIA (15%)", f"${ganancia:,.2f}")
            
            # Botón para descargar
            csv_data = df_final.to_csv(index=False).encode('utf-8')
            st.download_button("📥 DESCARGAR EXCEL", data=csv_data, file_name="servicios_rs.csv", mime="text/csv")
