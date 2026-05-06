import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime
import os

# 1. CONFIGURACIÓN VISUAL RS
st.set_page_config(page_title="OKGRUAS RS - Oficial", page_icon="🚛", layout="wide")

# 2. SISTEMA DE EXCEL REAL (SIN LEYENDAS AMARILLAS)
ARCHIVO_OFICIAL = "servicios_monterrey_rs.xlsx"
COLUMNAS = ["Folio", "Fecha", "Cliente", "WhatsApp", "Falla", "KM", "Maniobras", "Total"]

def gestionar_excel(datos=None):
    # Si el archivo no existe, lo creamos como .xlsx real
    if not os.path.exists(ARCHIVO_OFICIAL):
        pd.DataFrame(columns=COLUMNAS).to_excel(ARCHIVO_OFICIAL, index=False)
    
    df = pd.read_excel(ARCHIVO_OFICIAL)
    
    if datos:
        folio = f"RS2014-{len(df) + 1}"
        datos["Folio"] = folio
        # Guardamos el nuevo servicio
        nuevo_registro = pd.DataFrame([datos])[COLUMNAS]
        df_final = pd.concat([df, nuevo_registro], ignore_index=True)
        df_final.to_excel(ARCHIVO_OFICIAL, index=False)
        return folio
    
    return f"RS2014-{len(df) + 1}"

# 3. INTERFAZ DE USUARIO
st.markdown("<h1 style='color: #00FF00;'>OKGRUAS RS 🚛</h1>", unsafe_allow_html=True)
st.divider()

col_datos, col_total = st.columns([3, 2])

with col_datos:
    st.markdown("### 📍 REGISTRO DE SERVICIO")
    c1, c2 = st.columns(2)
    with c1: cliente = st.text_input("Nombre del Cliente:")
    with c2: tel = st.text_input("WhatsApp (10 dígitos):")
    
    ck1, ck2 = st.columns(2)
    with ck1: km = st.number_input("KM Recorridos:", min_value=0.0, step=1.0)
    with ck2: falla = st.selectbox("Falla:", ["Mecánica", "Choque", "Llanta", "Batería", "Sótano"])
    
    st.markdown("**🔧 Maniobras Extras ($350 c/u)**")
    m1, m2, m3 = st.columns(3)
    v_traba = m1.checkbox("Llantas trabadas")
    n_neutro = m2.checkbox("No entra Neutral")
    m_especial = m3.checkbox("Especial")
    
    es_sotano = st.checkbox("🔦 ¿Es Sótano?")
    niveles = st.number_input("Pisos:", min_value=0, step=1) if es_sotano else 0

# CÁLCULOS
COSTO_EXTRAS = (350.0 * sum([v_traba, n_neutro, m_especial])) + (niveles * 350.0)
TOTAL_NETO = 800.0 + (km * 25.0) + COSTO_EXTRAS

with col_total:
    st.markdown("### 📋 RESUMEN")
    st.metric("TOTAL A COBRAR", f"${TOTAL_TOTAL:,.2f}")
    st.caption(f"Siguiente Folio: {gestionar_excel()}")

# 4. BOTÓN DE REGISTRO
st.divider()
if len(tel) >= 10:
    if st.button("🚀 GUARDAR Y ENVIAR WHATSAPP", use_container_width=True):
        info_servicio = {
            "Folio": "", "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Cliente": cliente if cliente else "Gral",
            "WhatsApp": tel, "Falla": falla, "KM": km,
            "Maniobras": COSTO_EXTRAS, "Total": TOTAL_NETO
        }
        f_real = gestionar_excel(info_servicio)
        
        # WhatsApp sin símbolos raros
        msj = (f"*OKGRUAS RS*\n🆔 Folio: {f_real}\n👤 Cliente: {info_servicio['Cliente']}\n💰 *TOTAL: ${TOTAL_NETO:,.2f}*")
        link_wa = f"https://wa.me/52{tel[-10:]}?text={urllib.parse.quote(msj)}"
        
        st.success(f"✅ ¡Folio {f_real} guardado!")
        st.link_button("📲 ENVIAR POR WHATSAPP", link_wa, type="primary", use_container_width=True)
else:
    st.warning("⚠️ Pon el WhatsApp del cliente para guardar.")

# 5. PANEL DE AUDITORÍA (GANANCIA 10%)
with st.expander("📊 RENDIMIENTO PRIVADO"):
    if st.text_input("Clave Admin", type="password") == "RS2014":
        if os.path.exists(ARCHIVO_OFICIAL):
            df_historial = pd.read_excel(ARCHIVO_OFICIAL)
            st.dataframe(df_historial)
            
            # COMISIÓN AL 10%
            ganancia_rs = df_historial["Total"].sum() * 0.10
            st.metric("TU GANANCIA (10%)", f"${ganancia_rs:,.2f}")
