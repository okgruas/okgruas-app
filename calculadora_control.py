import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime
import os

# 1. ESTILO Y CONFIGURACIÓN RS
st.set_page_config(page_title="OKGRUAS RS - Excel Nativo", page_icon="🚛", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; background-color: #121212; color: #FFFFFF; }
    .stMetric { background-color: #1e1e1e; border: 1px solid #00FF00; padding: 15px; border-radius: 10px; }
    .price-tag { background-color: #262626; padding: 10px; border-radius: 5px; border-left: 3px solid #00FF00; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE EXCEL NATIVO (.xlsx)
ARCHIVO_EXCEL = "servicios_rs_oficial.xlsx"
COLUMNAS = ["Folio", "Fecha", "Cliente", "WhatsApp", "Falla", "KM", "Maniobras", "Total"]

def guardar_en_excel_nativo(datos=None):
    if not os.path.exists(ARCHIVO_EXCEL):
        df_base = pd.DataFrame(columns=COLUMNAS)
        df_base.to_excel(ARCHIVO_EXCEL, index=False)
    
    df = pd.read_excel(ARCHIVO_EXCEL)
    
    if datos:
        folio_nuevo = f"RS2014-{len(df) + 1}"
        datos["Folio"] = folio_nuevo
        # Concatenar nuevo servicio
        nuevo_df = pd.DataFrame([datos])[COLUMNAS]
        df_actualizado = pd.concat([df, nuevo_df], ignore_index=True)
        df_actualizado.to_excel(ARCHIVO_EXCEL, index=False)
        return folio_nuevo
    
    return f"RS2014-{len(df) + 1}"

# 3. ACCESO
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    st.markdown("<h1 style='color: #00FF00; text-align: center;'>🔐 ACCESO RS</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.text_input("Clave de Aplicación", type="password") == "RS2026":
            if st.button("ENTRAR"):
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# 4. CAPTURA DE DATOS
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
    m1, m2, m3 = st.columns(3)
    v_trab = m1.checkbox("Volante/Llantas")
    n_neut = m2.checkbox("No Neutral")
    m_espec = m3.checkbox("Especial")
    
    sotano_ch = st.checkbox("🔦 ¿Sótano?")
    niveles_n = st.number_input("Niveles:", min_value=0, step=1) if sotano_ch else 0

# CÁLCULOS
COSTO_EXTRAS = (350.0 * sum([v_trab, n_neut, m_espec])) + (niveles_n * 350.0)
TOTAL_TOTAL = 800.0 + (km_n * 25.0) + COSTO_EXTRAS

with col_res:
    st.markdown("### 📋 DESGLOSE")
    st.markdown(f"<div class='price-tag'>🏁 Banderazo: $800.00</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🛣️ KM: ${km_n*25:,.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🔧 Extras: ${COSTO_EXTRAS:,.2f}</div>", unsafe_allow_html=True)
    st.divider()
    st.metric("TOTAL NETO", f"${TOTAL_TOTAL:,.2f}")
    st.caption(f"Siguiente Folio: {guardar_en_excel_nativo()}")

# 5. REGISTRO Y WHATSAPP
st.divider()
if len(whatsapp_n) >= 10:
    if st.button("🚀 REGISTRAR Y GENERAR COTIZACIÓN", use_container_width=True):
        datos = {
            "Folio": "", "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Cliente": cliente_n if cliente_n else "General",
            "WhatsApp": whatsapp_n, "Falla": falla_n, "KM": km_n,
            "Maniobras": COSTO_EXTRAS, "Total": TOTAL_TOTAL
        }
        folio_asig = guardar_en_excel_nativo(datos)
        
        msg = (f"*OKGRUAS RS*\n🆔 *Folio: {folio_asig}*\n👤 Cliente: {datos['Cliente']}\n💰 *TOTAL: ${TOTAL_TOTAL:,.2f}*\n------------------\n_Monterrey, N.L._")
        link = f"https://wa.me/52{whatsapp_n[-10:]}?text={urllib.parse.quote(msg)}"
        
        st.success(f"✅ ¡Folio {folio_asig} guardado en Excel nativo!")
        st.link_button("📲 ENVIAR WHATSAPP", link, type="primary", use_container_width=True)
else:
    st.warning("⚠️ Falta número de cliente.")

# 6. PANEL ADMIN (COMISIÓN 10%)
with st.expander("📊 RENDIMIENTO PRIVADO"):
    if st.text_input("Clave Admin", type="password") == "RS2014":
        if os.path.exists(ARCHIVO_EXCEL):
            df_admin = pd.read_excel(ARCHIVO_EXCEL)
            st.dataframe(df_admin, use_container_width=True)
            
            ganancia = df_admin["Total"].sum() * 0.10
            st.metric("TU GANANCIA (10%)", f"${ganancia:,.2f}")
