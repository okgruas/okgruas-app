import streamlit as st
import urllib.parse
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="OKGRUAS RS - Solicitud", page_icon="🚛", layout="centered")

# 2. ESTILO VISUAL (Verde Neón y Tipografía Montserrat)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        background-color: #121212;
        color: white;
    }
    .stButton>button { 
        background-color: #00FF00; 
        color: black; 
        border-radius: 10px; 
        width: 100%;
        font-weight: bold;
        height: 3em;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea { 
        background-color: #262626 !important; color: white !important; border: 1px solid #00FF00 !important; 
    }
    label { color: #00FF00 !important; font-weight: bold; }
    h1, h2, h3 { color: #00FF00 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. CABECERA (LOGO PEQUEÑO + NOMBRE OKGRUAS RS)
col_head1, col_head2 = st.columns([1, 4])

with col_head1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=100)
    else:
        st.markdown("<h1 style='margin:0;'>🚛</h1>", unsafe_allow_html=True)

with col_head2:
    st.markdown("<h1 style='margin-bottom: 0px; padding-top: 10px;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; margin-top: 0px;'>Solicitud de Servicio de Grúa</p>", unsafe_allow_html=True)

st.divider()

# 4. FORMULARIO DE SOLICITUD
st.markdown("### 📱 Completa los datos para tu cotización")

with st.form("solicitud_servicio"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Tu Nombre")
        modelo = st.text_input("Modelo del Auto")
    with col2:
        origen = st.text_input("📍 Punto de Recolección")
        destino = st.text_input("🏁 Punto de Entrega")
    
    tipo_falla = st.selectbox("¿Qué problema presenta el vehículo?", [
        "Falla Mecánica", 
        "Choque / Siniestro", 
        "Llanta Ponchada", 
        "Sin Batería", 
        "Auto Bloqueado",
        "Otro (Especificar en notas)"
    ])
    
    notas = st.text_area("Notas adicionales (ej. si está en un sótano, no tiene llaves, etc.)")
    
    st.info("💡 Al enviar la solicitud, un asesor se pondrá en contacto contigo vía WhatsApp para darte el costo exacto y tiempo de llegada.")
    
    btn_enviar = st.form_submit_button("📩 SOLICITAR COTIZACIÓN POR WHATSAPP")

# 5. LÓGICA DE ENVÍO
if btn_enviar:
    if nombre and modelo and origen and destino:
        # Texto del mensaje sin precio, pidiendo cotización
        texto = (
            f"*NUEVA SOLICITUD DE SERVICIO - OKGRUAS RS*\n\n"
            f"👤 *Cliente:* {nombre}\n"
            f"🚗 *Vehículo:* {modelo}\n"
            f"🛠️ *Problema:* {tipo_falla}\n"
            f"📍 *Origen:* {origen}\n"
            f"🏁 *Destino:* {destino}\n"
            f"📝 *Notas:* {notas}\n\n"
            f"🧐 *Solicito cotización y tiempo de llegada.*"
        )
        mensaje_url = urllib.parse.quote(texto)
        mi_numero = "528143029578" # Tu número actualizado
        whatsapp_link = f"https://wa.me/{mi_numero}?text={mensaje_url}"
        
        st.markdown(f'''
            <a href="{whatsapp_link}" target="_blank">
                <button style="background-color: #25D366; color: white; padding: 15px; border: none; border-radius: 10px; width: 100%; cursor: pointer; font-weight: bold; font-size: 16px;">
                    ✅ CLICK AQUÍ PARA CONFIRMAR EN WHATSAPP
                </button>
            </a>
        ''', unsafe_allow_html=True)
    else:
        st.error("⚠️ Por favor, llena los campos obligatorios (Nombre, Vehículo, Origen y Destino).")

st.markdown("<br><p style='text-align: center; color: #444; font-size: 10px;'>OKGRUAS RS © 2026</p>", unsafe_allow_html=True)
