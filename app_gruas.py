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
    .block-container { padding-top: 0rem !important; }
    html, body, [class*="css"], .stMarkdown { font-family: 'Montserrat', sans-serif; color: #FFFFFF !important; }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea { 
        background-color: #1A1A1A !important; color: #00FF00 !important; border: 1px solid #00FF00 !important; 
    }
    label { color: #00FF00 !important; font-weight: bold !important; }
    .stCheckbox>label>div>div { border: 1px solid #00FF00 !important; }
    
    h1, h2, h3 { color: #00FF00 !important; text-shadow: 0 0 10px rgba(0, 255, 0, 0.3); }
    .stButton>button { 
        background-color: #00FF00 !important; color: #000000 !important; 
        border-radius: 10px; font-weight: bold; width: 100%; height: 3.5em;
    }
    hr { border-top: 1px solid #00FF00 !important; }
    
    [data-testid="stSidebar"] { background-color: #111111 !important; border-right: 1px solid #00FF00 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL ADMIN (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 🔐 Admin OKGRUAS")
    clave = st.text_input("Clate", type="password")
    if clave == "RS1020":
        st.success("Modo Admin")
        monto_final = st.number_input("Costo Total Final ($)", value=800)
        st.metric("Tu Comisión (10%)", f"${monto_final * 0.10:,.2f}")

# 3. CABECERA
col_head1, col_head2 = st.columns([1, 4])
with col_head1:
    st.markdown("<h1 style='margin:0;'>🚛</h1>", unsafe_allow_html=True)
with col_head2:
    st.markdown("<h1 style='margin-bottom: 0px; padding-top: 10px;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888;'>Área Metropolitana y Foráneos</p>", unsafe_allow_html=True)

st.divider()

# --- INFORMACIÓN DE TARIFAS ---
c1, c2 = st.columns(2)
with c1:
    st.markdown("📍 **Banderazo:** $800.00")
with c2:
    st.markdown("🛣️ **Km Extra:** $25.00")

# 4. FORMULARIO DINÁMICO
st.markdown("### 📋 Datos del Servicio")

with st.form("solicitud_detallada"):
    col_a, col_b = st.columns(2)
    with col_a:
        nombre = st.text_input("Nombre del Cliente")
        vehiculo = st.text_input("Tipo de Vehículo (Marca y Modelo)")
        color = st.text_input("
