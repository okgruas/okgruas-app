import streamlit as st
import urllib.parse
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="OKGRUAS RS - Cotización", page_icon="🚛", layout="centered")

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
        border-radius: 10px; font-weight: bold; width: 100%; height: 3.5em;
    }

    /* ESTILO PARA EL LOGO TRASLÚCIDO */
    .logo-container {
        opacity: 0.5; /* Ajusta la transparencia aquí (0.1 es muy invisible, 1.0 es sólido) */
        transition: opacity 0.3s;
    }
    .logo-container:hover {
        opacity: 1.0; /* Se aclara cuando pasas el mouse */
    }

    .call-footer {
        display: block;
        background-color: #1A1A1A;
        color: #FF0000 !important;
        border: 2px solid #FF0000;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        font-size: 1rem;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CABECERA CON LOGO TRASLÚCIDO
col_logo1, col_logo2 = st.columns([1, 2])

with col_logo1:
    # Intentamos cargar el logo desde tu carpeta de GitHub
    if os.path.exists("logo.png"):
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.image("logo.png", width=120)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Si no encuentra el archivo, pone el emoji traslúcido
        st.markdown("<h1 style='margin:0; opacity: 0.5;'>🚛</h1>", unsafe_allow_html=True)

with col_logo2:
    st.markdown("<h1 style='margin-bottom: 0px; padding-top: 10px;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888;'>Servicio en Monterrey Área Metropolitana</p>", unsafe_allow_html=True)

st.divider()

# --- RECOMENDACIONES DE SEGURIDAD ---
with st.expander("🛡️ RECOMENDACIONES DE SEGURIDAD"):
    st.markdown("""
    * **Mantén la calma:** Ya estamos en camino.
    * **Encienda luces intermitentes:** Hazte visible.
    * **Resguárdate:** Si es posible, espera fuera del vehículo en zona segura.
    """)

# 4. FORMULARIO
st.markdown("### 📋 Datos del Servicio")
with st.form("form_rs_v5"):
    nombre = st.text_input("Nombre del Cliente")
    
    col1, col2 = st.columns(2)
    with col1:
        vehiculo = st.text_input("Marca y Modelo")
        año_auto = st.text_input("Año")
    with col2:
        color_auto = st.text_input("Color")
        placas = st.text_input("Placas")

    st.divider()
    
    punto_recoleccion = st.text_input("📍 Punto de Recolección (Manual)")
    punto_destino = st.text_input("🏁 Punto Destino")
    
    falla = st.selectbox("Problema", ["Falla Mecánica", "Choque", "Llanta", "Batería", "Falta de Gasolina", "Bloqueado"])
    
    submit_rs = st.form_submit_button("🚀 ENVIAR REPORTE POR WHATSAPP")

# 5. LÓGICA WHATSAPP
if submit_rs:
    if nombre:
        msg = (
            f"*🚨 SOLICITUD OKGRUAS RS*\n"
            f"--------------------------------\n"
            f"👤 *Cliente:* {nombre}\n"
            f"🚗 *Auto:* {vehiculo} ({año_auto})\n"
            f"🔢 *Placas:* {placas}\n"
            f"🚨 *Falla:* {falla}\n"
            f"📍 *Origen:* {punto_recoleccion}\n"
            f"🏁 *Destino:* {punto_destino}\n"
            f"--------------------------------"
        )
        link_ws = f"https://wa.me/528143029578?text={urllib.parse.quote(msg)}"
        st.markdown(f'<a href="{link_ws}" target="_blank"><div style="background-color: #00FF00; color: black; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold;">✅ CONFIRMAR EN WHATSAPP</div></a>', unsafe_allow_html=True)
    else:
        st.error("⚠️ El nombre es necesario.")

# --- 6. LLAMADA AL FINAL ---
st.markdown('<a href="tel:8143029578" class="call-footer">📞 EMERGENCIAS: 81 4302 9578</a>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #444; font-size: 10px;'>OKGRUAS RS © 2026 | Monterrey, N.L.</p>", unsafe_allow_html=True)
