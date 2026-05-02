import streamlit as st
import urllib.parse
from datetime import datetime

# 1. Configuración
st.set_page_config(page_title="OKGRUAS RS - PRIVADO", page_icon="🔐", layout="centered")

# 2. Estilo
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .stButton>button { background-color: #FF69B4; color: white; border-radius: 10px; width: 100%; font-weight: bold; }
    label { color: #FF69B4 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN DE SEGURIDAD ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    st.image("logo.png", width=200)
    st.title("🔒 Acceso Restringido")
    clave = st.text_input("Introduce la clave de acceso", type="password")
    if st.button("Entrar"):
        if clave == "RS2026": # <--- TU CLAVE MAESTRA
            st.session_state['autenticado'] = True
            st.rerun()
        else:
            st.error("Clave incorrecta")
    st.stop() # Detiene todo lo de abajo si no hay clave

# --- SI ESTÁ AUTENTICADO, MUESTRA EL RESTO ---

menu = st.sidebar.radio("Menú", ["📱 Cotizador", "📊 Admin"])

if menu == "📱 Cotizador":
    st.title("Calculadora Oficial OKGRUAS RS")
    
    with st.form("cotizador"):
        nombre_cliente = st.text_input("Nombre del Cliente")
        modelo = st.text_input("Modelo del Auto")
        tipo_falla = st.selectbox("Problema", ["Falla Mecánica", "Choque", "Llanta", "Batería", "Bloqueado"])
        distancia = st.number_input("Kilómetros totales", min_value=0, value=0)
        
        btn_enviar = st.form_submit_button("📩 GENERAR COTIZACIÓN")

    if btn_enviar:
        banderazo = 800
        costo_km = 25
        total = banderazo + (distancia * costo_km)
        
        # Aquí es donde tú llevas el control:
        # El mensaje que te llegue dirá la hora exacta de la consulta
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        texto = (
            f"*OKGRUAS RS - REGISTRO DE SERVICIO*\n"
            f"📅 *Fecha:* {ahora}\n"
            f"👤 *Cliente:* {nombre_cliente}\n"
            f"🛣️ *Distancia:* {distancia} km\n"
            f"💰 *Total:* ${total} MXN\n"
            f"--------------------------"
        )
        
        mensaje_url = urllib.parse.quote(texto)
        mi_numero = "528143029578"
        whatsapp_link = f"https://wa.me/{mi_numero}?text={mensaje_url}"
        
        st.success(f"Cotización de ${total} generada correctamente.")
        st.markdown(f'<a href="{whatsapp_link}" target="_blank"><button>✅ ENVIAR REPORTE A MATRIZ</button></a>', unsafe_allow_html=True)

elif menu == "📊 Admin":
    st.title("Control de Mandos")
    st.write("Bienvenida, Yajaira. Aquí puedes ver que el sistema está protegido.")
    if st.button("Cerrar Sesión"):
        st.session_state['autenticado'] = False
        st.rerun()
