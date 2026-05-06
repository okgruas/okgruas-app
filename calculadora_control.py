import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime
import os

# 1. ESTILO Y CONFIGURACIÓN
st.set_page_config(page_title="OKGRUAS RS - Control Total", page_icon="🚛", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; background-color: #121212; color: #FFFFFF; }
    .stMetric { background-color: #1e1e1e; border: 1px solid #00FF00; padding: 15px; border-radius: 10px; }
    .price-tag { background-color: #262626; padding: 10px; border-radius: 5px; border-left: 3px solid #00FF00; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE REGISTRO (CREA EL EXCEL AUTOMÁTICO)
ARCHIVO = "registro_asistencias.csv"

def inicializar_y_registrar(datos=None):
    # Crea el archivo con encabezados si no existe
    if not os.path.exists(ARCHIVO):
        df_base = pd.DataFrame(columns=["Folio", "Fecha", "Cliente", "WhatsApp", "Total", "Falla"])
        df_base.to_csv(ARCHIVO, index=False)
    
    df = pd.read_csv(ARCHIVO)
    
    if datos:
        # Generar Folio Consecutivo RS2014-X
        nuevo_num = len(df) + 1
        folio_nuevo = f"RS2014-{nuevo_num}"
        datos["Folio"] = folio_nuevo
        
        # Guardar en el archivo inmediatamente
        nuevo_df = pd.DataFrame([datos])
        nuevo_df.to_csv(ARCHIVO, mode='a', header=False, index=False)
        return folio_nuevo
    
    return f"RS2014-{len(df) + 1}"

# 3. SEGURIDAD DE ACCESO
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

# 4. CAPTURA DE DATOS
st.markdown("<h1 style='color: #00FF00;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
col_in, col_res = st.columns([3, 2])

with col_in:
    st.markdown("### 📍 DATOS DEL SERVICIO")
    c1, c2 = st.columns(2)
    with c1: cliente = st.text_input("Nombre del Cliente:")
    with c2: tel = st.text_input("WhatsApp (10 dígitos):")
    
    km = st.number_input("Kilómetros:", min_value=0.0, step=1.0)
    falla = st.selectbox("Falla:", ["Falla Mecánica", "Choque", "Llanta", "Batería", "Sótano/Maniobra"])
    
    m_check = st.checkbox("¿Hubo maniobras extras?")
    costo_m = 350.0 if m_check else 0.0

# CÁLCULOS
total = 800.0 + (km * 25.0) + costo_m

with col_res:
    st.markdown("### 📋 DESGLOSE")
    st.markdown(f"<div class='price-tag'>🏁 Banderazo: $800.00</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🛣️ KM: ${km*25:,.2f}</div>", unsafe_allow_html=True)
    st.divider()
    st.metric("TOTAL NETO", f"${total:,.2f}")
    st.caption(f"Siguiente Folio: {inicializar_y_registrar()}")

# 5. EL BOTÓN "PERFECTO" DE REGISTRO
st.divider()
if len(tel) >= 10:
    if st.button("✅ REGISTRAR Y GENERAR COTIZACIÓN", use_container_width=True):
        # PRIMERO SE GUARDA EN EL EXCEL
        info = {
            "Folio": "",
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Cliente": cliente if cliente else "General",
            "WhatsApp": tel,
            "Total": total,
            "Falla": falla
        }
        folio_final = inicializar_y_registrar(info)
        
        # LUEGO SE PREPARA EL LINK
        msg = (f"*OKGRUAS RS - COTIZACIÓN*\n"
               f"🆔 *Folio: {folio_final}*\n"
               f"👤 Cliente: {info['Cliente']}\n"
               f"💰 TOTAL: ${total:,.2f}\n"
               f"--------------------------\n"
               f"Reportar a: 528143029578")
        
        link = f"https://wa.me/52{tel[-10:]}?text={urllib.parse.quote(msg)}"
        
        st.success(f"📦 Servicio {folio_final} guardado en el archivo correctamente.")
        st.link_button("📲 ENVIAR POR WHATSAPP", link, type="primary", use_container_width=True)
else:
    st.warning("Escribe el número del cliente para poder registrar.")

# 6. PANEL PARA DESCARGAR EL EXCEL
with st.expander("📊 PANEL ADMINISTRADOR"):
    if st.text_input("Clave Admin", type="password") == "RS2014":
        if os.path.exists(ARCHIVO):
            df_log = pd.read_csv(ARCHIVO)
            st.dataframe(df_log)
            st.download_button("📥 DESCARGAR REGISTRO COMPLETO", 
                             data=df_log.to_csv(index=False).encode('utf-8'),
                             file_name="servicios_rs.csv", mime="text/csv")
