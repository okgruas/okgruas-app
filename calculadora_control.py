import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime
import os

# 1. CONFIGURACIÓN VISUAL
st.set_page_config(page_title="OKGRUAS RS - Control Excel", page_icon="🚛", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; background-color: #121212; color: #FFFFFF; }
    .stMetric { background-color: #1e1e1e; border: 1px solid #00FF00; padding: 15px; border-radius: 10px; }
    .price-tag { background-color: #262626; padding: 10px; border-radius: 5px; border-left: 3px solid #00FF00; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE EXCEL (ORDENADO POR COLUMNAS)
ARCHIVO_EXCEL = "registro_asistencias_rs.csv"
COLUMNAS = ["Folio", "Fecha", "Cliente", "WhatsApp", "Falla", "KM", "Maniobras", "Total"]

def inicializar_y_guardar(datos=None):
    # Si no existe, crea el archivo con el separador correcto para Excel
    if not os.path.exists(ARCHIVO_EXCEL):
        pd.DataFrame(columns=COLUMNAS).to_csv(ARCHIVO_EXCEL, index=False, sep=';')
    
    try:
        df = pd.read_csv(ARCHIVO_EXCEL, sep=';')
    except:
        # En caso de error, reinicia el archivo limpio
        pd.DataFrame(columns=COLUMNAS).to_csv(ARCHIVO_EXCEL, index=False, sep=';')
        df = pd.read_csv(ARCHIVO_EXCEL, sep=';')
    
    if datos:
        siguiente_folio = f"RS2014-{len(df) + 1}"
        datos["Folio"] = siguiente_folio
        nuevo_registro = pd.DataFrame([datos])[COLUMNAS]
        # Guardar con sep=';' para que Excel lo abra con columnas separadas
        nuevo_registro.to_csv(ARCHIVO_EXCEL, mode='a', header=False, index=False, sep=';')
        return siguiente_folio
    
    return f"RS2014-{len(df) + 1}"

# 3. SEGURIDAD DE ACCESO
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    st.markdown("<h1 style='color: #00FF00; text-align: center;'>🔐 ACCESO RS</h1>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1,2,1])
    with col_l2:
        if st.text_input("Ingresa Clave de App", type="password") == "RS2026":
            if st.button("ENTRAR"):
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# 4. INTERFAZ DE REGISTRO
st.markdown("<h1 style='color: #00FF00;'>OKGRUAS RS 🚛</h1>", unsafe_allow_html=True)
st.divider()

col_datos, col_calculos = st.columns([3, 2])

with col_datos:
    st.markdown("### 📍 DATOS DEL SERVICIO")
    c1, c2 = st.columns(2)
    with c1: cliente_nom = st.text_input("Nombre del Cliente:")
    with c2: cliente_tel = st.text_input("WhatsApp (10 dígitos):")
    
    ck1, ck2 = st.columns(2)
    with ck1: km_totales = st.number_input("Kilómetros Recorridos:", min_value=0.0, step=1.0)
    with ck2: tipo_falla = st.selectbox("Falla:", ["Falla Mecánica", "Choque", "Llanta", "Batería", "Sótano"])
    
    st.markdown("**🔧 Maniobras Extras ($350 c/u)**")
    m1, m2, m3 = st.columns(3)
    v_trabado = m1.checkbox("Volante/Llantas")
    n_neutral = m2.checkbox("No Neutral")
    especial = m3.checkbox("Extra Especial")
    
    sotano_en = st.checkbox("🔦 ¿Entrada a Sótano?")
    niveles_n = st.number_input("¿Cuántos niveles?", min_value=0, step=1) if sotano_en else 0

# CÁLCULOS
COSTO_MANIOBRAS = (350.0 * sum([v_trabado, n_neutral, especial])) + (niveles_n * 350.0)
TOTAL_A_COBRAR = 800.0 + (km_totales * 25.0) + COSTO_MANIOBRAS

with col_calculos:
    st.markdown("### 📋 DESGLOSE")
    st.markdown(f"<div class='price-tag'>🏁 Salida: $800.00</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🛣️ Ruta ({km_totales}km): ${km_totales*25:,.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🔧 Extras: ${COSTO_MANIOBRAS:,.2f}</div>", unsafe_allow_html=True)
    st.divider()
    st.metric("TOTAL NETO", f"${TOTAL_A_COBRAR:,.2f}")
    st.caption(f"Siguiente Folio a Generar: {inicializar_y_guardar()}")

# 5. REGISTRO Y WHATSAPP
st.divider()
if len(cliente_tel) >= 10:
    if st.button("🚀 REGISTRAR Y GENERAR WHATSAPP", use_container_width=True):
        datos_registro = {
            "Folio": "", 
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Cliente": cliente_nom if cliente_nom else "General",
            "WhatsApp": cliente_tel, 
            "Falla": tipo_falla, 
            "KM": km_totales,
            "Maniobras": COSTO_MANIOBRAS, 
            "Total": TOTAL_A_COBRAR
        }
        
        folio_real = inicializar_y_guardar(datos_registro)
        
        # MENSAJE LIMPIO
        mensaje = (f"*OKGRUAS RS*\n🆔 *Folio: {folio_real}*\n👤 Cliente: {datos_registro['Cliente']}\n🛠️ Falla: {tipo_falla}\n💰 *TOTAL: ${TOTAL_A_COBRAR:,.2f}*\n------------------\n_Servicio Monterrey_")
        url_wa = f"https://wa.me/52{cliente_tel[-10:]}?text={urllib.parse.quote(mensaje)}"
        
        st.success(f"✅ ¡Servicio {folio_real} guardado en el Excel!")
        st.link_button("📲 ENVIAR POR WHATSAPP", url_wa, type="primary", use_container_width=True)
else:
    st.info("💡 Ingresa el número del cliente para registrar.")

# 6. PANEL DE AUDITORÍA (GANANCIA 10%)
with st.expander("📊 PANEL ADMINISTRADOR"):
    if st.text_input("Clave Admin", type="password") == "RS2014":
        if os.path.exists(ARCHIVO_EXCEL):
            df_final = pd.read_csv(ARCHIVO_EXCEL, sep=';')
            st.dataframe(df_final, use_container_width=True)
            
            # COMISIÓN AL 10%
            mi_comision = df_final["Total"].sum() * 0.10
            st.metric("TU GANANCIA (10%)", f"${mi_comision:,.2f}")
            
            st.download_button("📥 DESCARGAR EXCEL COMPLETO", 
                             data=df_final.to_csv(index=False, sep=';').encode('utf-8'), 
                             file_name="reporte_servicios_rs.csv", mime="text/csv")
