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
    html, body, [class*="css"], .stMarkdown { font-family: 'Montserrat', sans-serif; color: #FFFFFF !important; }
    
    /* Botón de Pánico Rojo */
    .panic-button {
        display: block;
        background-color: #FF0000;
        color: white !important;
        border: 3px solid #FFFFFF;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        font-size: 1.4rem;
        margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.6);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CABECERA
st.markdown("<h1 style='text-align: center; color: #00FF00;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Logística Integral Monterrey</p>", unsafe_allow_html=True)

# --- BOTÓN DE PÁNICO (GPS) ---
st.markdown("""
    <a href="https://www.google.com/maps/search/?api=1&query=mi+ubicacion" class="panic-button">
        🆘 ENVIAR MI UBICACIÓN GPS
    </a>
    <p style='text-align: center; font-size: 0.8rem; color: #FF0000;'>Presiona si no sabes dónde estás; te abrirá el mapa para compartirlo.</p>
""", unsafe_allow_html=True)

# --- BOTÓN DE LLAMADA ---
st.markdown('<a href="tel:8143029578" style="display:block; background-color:#1A1A1A; color:#00FF00; border:2px solid #00FF00; border-radius:10px; padding:10px; text-align:center; text-decoration:none; font-weight:bold; margin-bottom:20px;">📞 LLAMADA DE EMERGENCIA</a>', unsafe_allow_html=True)

st.divider()

# 4. FORMULARIO RESUMIDO
with st.form("solicitud_rapida"):
    nombre = st.text_input("Tu Nombre")
    vehiculo = st.text_input("Vehículo (Marca/Modelo/Color)")
    falla = st.selectbox("¿Qué sucede?", ["Falla Mecánica", "Choque", "Llanta Ponchada", "Sin Batería", "Otro"])
    
    st.markdown("#### 📍 Destino")
    destino = st.text_input("¿A dónde llevamos el auto?")
    
    submit = st.form_submit_button("🚀 SOLICITAR GRÚA AHORA")

if submit:
    if nombre:
        msg = f"*EMERGENCIA OKGRUAS RS*\n👤 *Cliente:* {nombre}\n🚗 *Auto:* {vehiculo}\n🚨 *Problema:* {falla}\n🏁 *Destino:* {destino}\n📍 *Ubicación:* Enviada por GPS"
        link_ws = f"https://wa.me/528143029578?text={urllib.parse.quote(msg)}"
        st.markdown(f'<a href="{link_ws}" target="_blank"><div style="background-color:#00FF00; color:black; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">✅ CONFIRMAR POR WHATSAPP</div></a>', unsafe_allow_html=True)
