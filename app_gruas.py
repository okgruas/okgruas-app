import streamlit as st
import urllib.parse
from streamlit_js_eval import streamlit_js_eval # Necesitarás instalar: pip install streamlit-js-eval

# 1. CONFIGURACIÓN
st.set_page_config(page_title="OKGRUAS RS - Auxilio Vial", page_icon="🚨", layout="centered")

# 2. ESTILO VISUAL "NEÓN RS"
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    .stApp { background-color: #000000 !important; }
    header, footer, .stAppDeployButton, #MainMenu { display: none !important; visibility: hidden !important; }
    .block-container { padding-top: 2rem !important; }
    html, body, [class*="css"], .stMarkdown { font-family: 'Montserrat', sans-serif; color: #FFFFFF !important; }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea { 
        background-color: #1A1A1A !important; color: #00FF00 !important; border: 1px solid #00FF00 !important; 
    }
    label { color: #00FF00 !important; font-weight: bold !important; }
    h1, h2, h3 { color: #00FF00 !important; text-shadow: 0 0 10px rgba(0, 255, 0, 0.3); }
    
    .stButton>button { 
        background-color: #00FF00 !important; color: #000000 !important; 
        border-radius: 12px; font-weight: bold; width: 100%; height: 3.5em;
    }
    
    .call-footer {
        display: block;
        background-color: #1A1A1A;
        color: #FF0000 !important;
        border: 1px solid #FF0000;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.9rem;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- OBTENCIÓN DE UBICACIÓN REAL (GPS) ---
# Esto detecta las coordenadas del celular del cliente
location = streamlit_js_eval(data_key='pos', func_name='getCurrentPosition', want_output=True)
lat_long_str = ""
if location:
    lat = location['coords']['latitude']
    lon = location['coords']['longitude']
    lat_long_str = f"https://www.google.com/maps?q={lat},{lon}"

# 3. CABECERA
col_logo1, col_logo2 = st.columns([1, 2])
with col_logo1:
    try:
        st.image("logo.png", width=120) 
    except:
        st.markdown("<h1 style='margin:0;'>🚛</h1>", unsafe_allow_html=True)

with col_logo2:
    st.markdown("<h1 style='margin-bottom: 0px; padding-top: 10px;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888;'>Servicio en Monterrey y Área Metropolitana</p>", unsafe_allow_html=True)

st.divider()

# 4. FORMULARIO
st.markdown("### 📋 Reporte de Asistencia")
with st.form("form_rs_v4"):
    nombre = st.text_input("Nombre del Cliente")
    
    col1, col2 = st.columns(2)
    with col1:
        vehiculo = st.text_input("Marca y Modelo")
        año_auto = st.text_input("Año")
    with col2:
        color = st.text_input("Color")
        placas = st.text_input("Placas")

    st.divider()
    
    punto_recoleccion = st.text_input("📍 Punto de Recolección (Manual)")
    punto_destino = st.text_input("🏁 Punto Destino")
    
    falla = st.selectbox("Problema o Falla", ["Falla Mecánica", "Choque", "Llanta Ponchada", "Batería / Paso de Corriente", "Falta de Gasolina", "Bloqueado / Llaves dentro"])
    
    notas = st.text_area("Notas adicionales")
    
    st.info("💡 Al confirmar, se incluirán tus coordenadas GPS reales en el mensaje.")
    submit_rs = st.form_submit_button("🚀 GENERAR REPORTE CON GPS")

# 5. LÓGICA DE WHATSAPP
if submit_rs:
    if nombre:
        # Si detectó el GPS usamos las coordenadas reales, si no, el link genérico
        final_gps = lat_long_str if lat_long_str else "El cliente no activó su GPS manual"
        
        msg = (
            f"*🚨 SOLICITUD DE ASISTENCIA - OKGRUAS RS*\n"
            f"--------------------------------\n"
            f"👤 *Cliente:* {nombre}\n"
            f"🚗 *Auto:* {vehiculo} {año_auto} ({color})\n"
            f"🔢 *Placas:* {placas}\n"
            f"--------------------------------\n"
            f"📍 *Origen Manual:* {punto_recoleccion}\n"
            f"🏁 *Destino:* {punto_destino}\n"
            f"🚨 *Situación:* {falla}\n"
            f"📝 *Notas:* {notas}\n"
            f"--------------------------------\n"
            f"📍 *UBICACIÓN GPS REAL:* \n{final_gps}\n"
            f"--------------------------------\n"
        )
        
        link_ws = f"https://wa.me/528143029578?text={urllib.parse.quote(msg)}"
        
        st.markdown(f'''
            <a href="{link_ws}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #00FF00; color: black; padding: 20px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 1.2rem; box-shadow: 0 0 15px rgba(0,255,0,0.5);">
                    ✅ ENVIAR POR WHATSAPP AHORA
                </div>
            </a>
        ''', unsafe_allow_html=True)
    else:
        st.error("⚠️ Ingresa tu nombre para continuar.")

# 6. LLAMADA AL FINAL
st.markdown('<a href="tel:8143029578" class="call-footer">📞 ¿No puedes escribir? Llamar a Central</a>', unsafe_allow_html=True)

# 7. PANEL ADMIN
with st.expander("🔐"):
    clave = st.text_input("Clave", type="password")
    if clave == "RS1020":
        st.write("Acceso Admin OK")
