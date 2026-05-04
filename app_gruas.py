import streamlit as st
import urllib.parse
import os
import pandas as pd # Agregamos pandas para la parte de administración

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="OKGRUAS RS - Solicitud", page_icon="🚛", layout="centered")

# 2. TU ESTILO VISUAL "BLINDADO" (Se mantiene intacto)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    .stApp { background-color: #000000 !important; }
    header, footer, .stAppDeployButton, #MainMenu { display: none !important; visibility: hidden !important; }
    .block-container { padding-top: 0rem !important; }
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Montserrat', sans-serif;
        color: #FFFFFF !important;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea { 
        background-color: #1A1A1A !important; 
        color: #00FF00 !important; 
        border: 1px solid #00FF00 !important; 
    }
    label { color: #00FF00 !important; font-weight: bold !important; font-size: 1.1rem !important; }
    h1, h2, h3 { color: #00FF00 !important; text-shadow: 0 0 10px rgba(0, 255, 0, 0.3); }
    .stButton>button { 
        background-color: #00FF00 !important; 
        color: #000000 !important; 
        border-radius: 10px; font-weight: bold; border: none; height: 3em; width: 100%;
    }
    .stButton>button:hover { box-shadow: 0 0 20px #00FF00; color: #000000 !important; }
    hr { border-top: 1px solid #00FF00 !important; }
    
    /* Estilo para la barra lateral de Admin */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #00FF00 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NUEVA SECCIÓN: LÓGICA DE ADMINISTRACIÓN (OCULTA) ---
# Esto solo aparece si tú decides abrir la barra lateral
with st.sidebar:
    st.markdown("### 🔐 Panel Admin")
    clave = st.text_input("Clave de acceso", type="password")
    
    if clave == "RS1020": # Tu clave secreta
        st.success("Acceso Autorizado")
        st.markdown("---")
        st.subheader("💰 Calculadora de Comisión")
        monto_servicio = st.number_input("Monto del servicio ($)", min_value=0, value=1500)
        socio_nombre = st.text_input("Nombre del Socio", "Ej. Juan Perez")
        
        comision = monto_servicio * 0.10
        st.metric("Tu Ganancia (10%)", f"${comision:,.2f}")
        
        if st.button("REGISTRAR COMISIÓN"):
            st.toast(f"Registrado: {socio_nombre} - ${comision}")
    elif clave != "":
        st.error("Clave incorrecta")

# 3. CABECERA (Tu diseño original)
col_head1, col_head2 = st.columns([1, 4])
with col_head1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=100)
    else:
        st.markdown("<h1 style='margin:0;'>🚛</h1>", unsafe_allow_html=True)

with col_head2:
    st.markdown("<h1 style='margin-bottom: 0px; padding-top: 10px;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; margin-top: 0px;'>Servicio Profesional de Grúas</p>", unsafe_allow_html=True)

st.divider()

# --- NUEVA LEYENDA DE GARANTÍA (Lo que acordamos) ---
st.markdown("""
    <div style="border: 1px dashed #00FF00; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px;">
        <span style="color: #00FF00; font-weight: bold;">🛡️ GARANTÍA RS:</span> 
        Si surge cualquier inconveniente con el servicio, la empresa responde de inmediato.
    </div>
    """, unsafe_allow_html=True)

# 4. FORMULARIO DE SOLICITUD (Tu diseño original)
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
        "Falla Mecánica", "Choque / Siniestro", "Llanta Ponchada", "Sin Batería", "Auto Bloqueado", "Otro"
    ])
    
    notas = st.text_area("Notas adicionales (ej. sótano, sin llaves, etc.)")
    btn_enviar = st.form_submit_button("📩 SOLICITAR COTIZACIÓN POR WHATSAPP")

# 5. LÓGICA DE ENVÍO
if btn_enviar:
    if nombre and modelo and origen and destino:
        texto = (
            f"*NUEVA SOLICITUD - OKGRUAS RS*\n\n"
            f"👤 *Cliente:* {nombre}\n"
            f"🚗 *Vehículo:* {modelo}\n"
            f"🛠️ *Problema:* {tipo_falla}\n"
            f"📍 *Origen:* {origen}\n"
            f"🏁 *Destino:* {destino}\n"
            f"📝 *Notas:* {notas}\n\n"
            f"🧐 *Solicito cotización y tiempo de llegada.*"
        )
        mensaje_url = urllib.parse.quote(texto)
        mi_numero = "528143029578" # Tu número de Monterrey
        whatsapp_link = f"https://wa.me/{mi_numero}?text={mensaje_url}"
        
        st.markdown(f'''
            <a href="{whatsapp_link}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #00FF00; color: black; padding: 15px; border-radius: 10px; width: 100%; text-align: center; font-weight: bold; font-size: 16px; cursor: pointer;">
                    ✅ CLICK AQUÍ PARA CONFIRMAR EN WHATSAPP
                </div>
            </a>
        ''', unsafe_allow_html=True)
    else:
        st.error("⚠️ Por favor, llena los campos obligatorios.")

st.markdown("<br><p style='text-align: center; color: #444; font-size: 10px;'>OKGRUAS RS © 2026 | Monterrey, N.L.</p>", unsafe_allow_html=True)
