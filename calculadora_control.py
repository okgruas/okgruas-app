import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime
import os

# 1. CONFIGURACIÓN VISUAL RS
st.set_page_config(page_title="OKGRUAS RS - Auditoría", page_icon="🚛", layout="wide")

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
    # Si el archivo no existe o está dañado, lo creamos de cero
    try:
        if not os.path.exists(ARCHIVO_REGISTRO):
            pd.DataFrame(columns=COLUMNAS).to_csv(ARCHIVO_REGISTRO, index=False)
        df = pd.read_csv(ARCHIVO_REGISTRO)
    except Exception:
        # Si hay error de lectura (como el ParserError), borramos y reiniciamos
        pd.DataFrame(columns=COLUMNAS).to_csv(ARCHIVO_REGISTRO, index=False)
        df = pd.read_csv(ARCHIVO_REGISTRO)
    
    if datos:
        siguiente_num = len(df) + 1
        folio_nuevo = f"RS2014-{siguiente_num}"
        datos["Folio"] = folio_nuevo
        # Guardar asegurando que no se mezclen las columnas
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
        clave_app = st.text_input("Clave", type="password")
        if st.button("ENTRAR"):
            if clave_app == "RS2026":
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
    
    m_extra = st.checkbox("¿Maniobras Extras? ($350)")
    p_sotano = st.number_input("Niveles Sótano:", min_value=0, step=1) if falla_n == "Sótano" else 0

# CÁLCULOS
COSTO_MAN = (350.0 if m_extra else 0) + (p_sotano * 350.0)
TOTAL_FINAL = 800.0 + (km_n * 25.0) + COSTO_MAN

with col_res:
    st.markdown("### 📋 DESGLOSE")
    st.markdown(f"<div class='price-tag'>🏁 Banderazo: $800.00</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🛣️ KM: ${km_n*25:,.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-tag'>🔧 Maniobras: ${COSTO_MAN:,.2f}</div>", unsafe_allow_html=True)
    st.divider()
    st.metric("TOTAL NETO", f"${TOTAL_FINAL:,.2f}")
    st.caption(f"Siguiente Folio: {inicializar_y_registrar()}")

# 5. REGISTRO Y ENVÍO
st.divider()
if len(whatsapp_n) >= 10:
    if st.button("🚀 REGISTRAR Y GENERAR WHATSAPP", use_container_width=True):
        fecha_h = datetime.now().strftime("%d/%m/%Y %H:%M")
        info_servicio = {
            "Folio": "", "Fecha": fecha_h, "Cliente": cliente_n if cliente_n else "Gral",
            "WhatsApp": whatsapp_n, "Falla": falla_n, "KM": km_n,
            "Maniobras": COSTO_MAN, "Total": TOTAL_FINAL
        }
        f_real = inicializar_y_registrar(info_servicio)
        
        msg_wa = (f"*OKGRUAS RS*\n🆔 Folio: {f_real}\n👤 Cliente: {info_servicio['Cliente']}\n💰 *TOTAL: ${TOTAL_FINAL:,.2f}*\n------------------\nReportar: 528143029578")
        link_wa = f"https://wa.me/52{whatsapp_n[-10:]}?text={urllib.parse.quote(msg_wa)}"
        
        st.success(f"✅ ¡Folio {f_real} guardado!")
        st.link_button("📲 ENVIAR POR WHATSAPP", link_wa, type="primary", use_container_width=True)
else:
    st.warning("⚠️ Ingresa el número de 10 dígitos.")

# 6. PANEL ADMINISTRATIVO (CORREGIDO)
with st.expander("📊 PANEL DE AUDITORÍA"):
    clave_adm = st.text_input("Clave Admin", type="password")
    if clave_adm == "RS2014":
        try:
            df_hist = pd.read_csv(ARCHIVO_REGISTRO)
            st.write("### Historial de Servicios")
            st.dataframe(df_hist)
            
            ganancia_yaja = df_hist["Total"].sum() * 0.15
            st.metric("TU GANANCIA (15%)", f"${ganancia_yaja:,.2f}")
            
            csv_b = df_hist.to_csv(index=False).encode('utf-8')
            st.download_button("📥 DESCARGAR EXCEL", data=csv_b, file_name="servicios_rs.csv", mime="text/csv")
        except:
            st.error("El archivo está vacío o reiniciándose.")
