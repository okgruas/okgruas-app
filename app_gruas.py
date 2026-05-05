import streamlit as st
import urllib.parse

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
    
    /* BOTÓN DE PÁNICO (LLAMADA) */
    .panic-button {
        display: block;
        background-color: #FF0000;
        color: white !important;
        border: 2px solid #FFFFFF;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 10px;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
    }
    
    /* CONTACTO DIRECTO */
    .call-button {
        display: block;
        background-color: #1A1A1A;
        color: #00FF00 !important;
        border: 2px solid #00FF00;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

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

# --- OPCIÓN 1: LLAMADA DIRECTA (ARRIBA) ---
st.markdown('<a href="tel:8143029578" class="panic-button">🚨 BOTÓN DE PÁNICO: LLAMAR AHORA</a>', unsafe_allow_html=True)
st.markdown('<a href="tel:8143029578" class="call-button">📞 CONTACTO DIRECTO A GRUEROS</a>', unsafe_allow_html=True)

st.divider()

# 4. FORMULARIO DE DATOS
st.markdown("### 📋 Datos del Vehículo")
with st.form("form_rs_full"):
    nombre = st.text_input("Nombre del Cliente")
    
    col1, col2 = st.columns(2)
    with col1:
        vehiculo = st.text_input("Marca y Modelo")
        año_auto = st.text_input("Año")
    with col2:
        color = st.text_input("Color")
        placas = st.text_input("Placas")

    st.divider()
    
    punto_recoleccion = st.text_input("📍 Punto de Recolección")
    punto_destino = st.text_input("🏁 Punto Destino")
    
    falla = st.selectbox("Problema", ["Falla Mecánica", "Choque", "Llanta", "Batería", "Bloqueado"])
    notas = st.text_area("Notas adicionales")
    
    submit_rs = st.form_submit_button("🚀 GENERAR REPORTE")

# 5. OPCIÓN 2: WHATSAPP CON UBICACIÓN EN TIEMPO REAL (ABAJO)
if submit_rs:
    if nombre:
        # Link de ubicación GPS para WhatsApp
        gps_link = "http://maps.google.com/maps?q=loc:0,0" # Enlace base para que el chat detecte ubicación
        
        msg = (
            f"*🚨 SOLICITUD DE AUXILIO - OKGRUAS RS*\n"
            f"--------------------------------\n"
            f"👤 *Cliente:* {nombre}\n"
            f"🚗 *Auto:* {vehiculo} {año_auto} ({color})\n"
            f"🔢 *Placas:* {placas}\n"
            f"--------------------------------\n"
            f"📍 *Origen:* {punto_recoleccion if punto_recoleccion else 'Ver GPS en mensaje'}\n"
            f"🏁 *Destino:* {punto_destino}\n"
            f"🚨 *Falla:* {falla}\n"
            f"📝 *Notas:* {notas}\n"
            f"--------------------------------\n"
            f"📍 *ENVÍO UBICACIÓN EN TIEMPO REAL ABAJO:* \n"
        )
        
        link_ws = f"https://wa.me/528143029578?text={urllib.parse.quote(msg)}"
        
        st.markdown(f'''
            <a href="{link_ws}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #00FF00; color: black; padding: 25px; border-radius: 15px; text-align: center; font-weight: bold; font-size: 1.3rem; box-shadow: 0 0 20px rgba(0,255,0,0.6);">
                    ✅ ENVIAR DATOS Y UBICACIÓN GPS
                </div>
            </a>
            <p style='text-align: center; color: #00FF00; font-size: 0.8rem; margin-top: 10px;'>Al hacer clic, se abrirá WhatsApp con tu reporte listo para enviar.</p>
        ''', unsafe_allow_html=True)
