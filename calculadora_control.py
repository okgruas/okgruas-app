import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime
import os

# 1. ESTILO RS
st.set_page_config(page_title="OKGRUAS RS - Sistema Monterrey", page_icon="🚛", layout="wide")

# 2. SISTEMA DE EXCEL (FORMATO NATIVO .XLSX)
ARCHIVO_REGISTRO = "servicios_okgruas_rs.xlsx"
COLUMNAS = ["Folio", "Fecha", "Cliente", "WhatsApp", "Falla", "KM", "Maniobras", "Total"]

def gestionar_datos_excel(datos_nuevos=None):
    if not os.path.exists(ARCHIVO_REGISTRO):
        pd.DataFrame(columns=COLUMNAS).to_excel(ARCHIVO_REGISTRO, index=False)
    
    df_actual = pd.read_excel(ARCHIVO_REGISTRO)
    
    if datos_nuevos:
        id_folio = f"RS2014-{len(df_actual) + 1}"
        datos_nuevos["Folio"] = id_folio
        nuevo_registro = pd.DataFrame([datos_nuevos])[COLUMNAS]
        df_final = pd.concat([df_actual, nuevo_registro], ignore_index=True)
        df_final.to_excel(ARCHIVO_REGISTRO, index=False)
        return id_folio
    
    return f"RS2014-{len(df_actual) + 1}"

# 3. INTERFAZ PRINCIPAL
st.markdown("<h1 style='color: #00FF00;'>OKGRUAS RS 🚛</h1>", unsafe_allow_html=True)
st.divider()

col_form, col_resumen = st.columns([3, 2])

with col_form:
    st.markdown("### 📍 REGISTRO DE SERVICIO")
    c1, c2 = st.columns(2)
    with c1: nom_cliente = st.text_input("Nombre del Cliente:")
    with c2: tel_cliente = st.text_input("WhatsApp (10 dígitos):")
    
    ck1, ck2 = st.columns(2)
    with ck1: dist_km = st.number_input("Kilómetros Recorridos:", min_value=0.0, step=1.0)
    with ck2: tipo_incidente = st.selectbox("Falla:", ["Mecánica", "Choque", "Llanta", "Batería", "Sótano"])
    
    st.markdown("**🔧 Maniobras Extras ($350 c/u)**")
    m1, m2, m3 = st.columns(3)
    llantas_t = m1.checkbox("Llantas trabadas")
    no_neutral = m2.checkbox("No entra Neutral")
    m_especial = m3.checkbox("Especial")
    
    en_sotano = st.checkbox("🔦 ¿Es Sótano?")
    num_pisos = st.number_input("Pisos:", min_value=0, step=1) if en_sotano else 0

# CÁLCULOS (Aquí corregimos el error de TOTAL_TOTAL que te salía)
EXTRAS_CALC = (350.0 * sum([llantas_t, no_neutral, m_especial])) + (num_pisos * 350.0)
TOTAL_FINAL = 800.0 + (dist_km * 25.0) + EXTRAS_CALC

with col_resumen:
    st.markdown("### 📋 RESUMEN")
    st.metric("TOTAL A COBRAR", f"${TOTAL_FINAL:,.2f}")
    st.caption(f"Siguiente Folio: {gestionar_datos_excel()}")

# 4. BOTÓN DE GUARDADO
st.divider()
if len(tel_cliente) >= 10:
    if st.button("🚀 GUARDAR Y ENVIAR WHATSAPP", use_container_width=True):
        nuevo_servicio = {
            "Folio": "", "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Cliente": nom_cliente if nom_cliente else "Gral",
            "WhatsApp": tel_cliente, "Falla": tipo_incidente, "KM": dist_km,
            "Maniobras": EXTRAS_CALC, "Total": TOTAL_FINAL
        }
        folio_gen = gestionar_datos_excel(nuevo_servicio)
        
        mensaje_wa = (f"*OKGRUAS RS*\n🆔 Folio: {folio_gen}\n💰 *TOTAL: ${TOTAL_FINAL:,.2f}*")
        url_final = f"https://wa.me/52{tel_cliente[-10:]}?text={urllib.parse.quote(mensaje_wa)}"
        
        st.success(f"✅ ¡Folio {folio_gen} guardado!")
        st.link_button("📲 ENVIAR POR WHATSAPP", url_final, type="primary", use_container_width=True)
else:
    st.info("💡 Ingresa el WhatsApp del cliente.")

# 5. ADMINISTRACIÓN (10% COMISIÓN)
with st.expander("📊 PANEL PRIVADO"):
    if st.text_input("Clave Admin", type="password") == "RS2014":
        if os.path.exists(ARCHIVO_REGISTRO):
            df_adm = pd.read_excel(ARCHIVO_REGISTRO)
            st.dataframe(df_adm)
            ganancia = df_adm["Total"].sum() * 0.10
            st.metric("TU GANANCIA (10%)", f"${ganancia:,.2f}")
