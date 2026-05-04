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
    .block-container { padding-top: 1rem !important; }
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

# --- PANEL ADMIN ---
with st.sidebar:
    st.markdown("### 🔐 Admin OKGRUAS")
    clave_admin = st.text_input("Clave", type="password", key="admin_key")
    if clave_admin == "RS1020":
        st.success("Acceso Admin")
        monto_serv = st.number_input("Costo del servicio ($)", value=800)
        st.metric("Tu Ganancia (10%)", f"${monto_serv * 0.10:,.2f}")

# 3. CABECERA CON LOGO
# Reemplaza 'URL_DE_TU_LOGO' con el enlace de tu imagen (ej. de GitHub Raw)
col_logo1, col_logo2 = st.columns([1, 3])
with col_logo1:
    # Si tienes el archivo en el mismo nivel que el script en GitHub, pon el nombre aquí:
    # st.image("logo.png", width=100) 
    st.markdown("<h1 style='margin:0;'>🚛</h1>", unsafe_allow_html=True) # Icono provisional
with col_logo2:
    st.markdown("<h1 style='margin-bottom: 0px; padding-top: 5px;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888;'>Servicio en Monterrey y Área Metropolitana</p>", unsafe_allow_html=True)

st.divider()

# --- TARIFAS VISIBLES ---
c_tar1, c_tar2 = st.columns(2)
with c_tar1:
    st.markdown("📍 **Banderazo:** $800.00")
with c_tar2:
    st.markdown("🛣️ **Km Extra:** $25.00")

# 4. FORMULARIO
st.markdown("### 📋 Datos del Servicio")

with st.form("form_rs_final"):
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        nombre = st.text_input("Nombre del Cliente")
        año_auto = st.text_input("Año")
        color = st.text_input("Color del Auto")
    with col_v2:
        vehiculo = st.text_input("Marca y Modelo")
        placas_auto = st.text_input("Placas")
        zona_serv = st.selectbox("Zona Sugerida", ["Local (Mty)", "Foráneo"])

    st.divider()
    
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        punto_recoleccion = st.text_input("📍 Punto de Recolección")
    with col_u2:
        punto_destino = st.text_input("🏁 Punto Destino")
    
    tipo_lugar = st.radio("Tipo de destino", ["Casa Particular", "Taller Mecánico", "Corralón / Otro"], horizontal=True)

    st.divider()
    
    st.markdown("#### 🛠️ Estado del Vehículo")
    cf1, cf2 = st.columns(2)
    with cf1:
        is_neutral = st.checkbox("se puede poner en neutral")
        is_giro = st.checkbox("ruedas y volante giran")
    with cf2:
        falla_tipo = st.selectbox("Problema", ["Falla Mecánica", "Choque", "Llanta", "Batería", "Bloqueado"])

    notas_serv = st.text_area("Notas adicionales")
    
    st.markdown("<p style='color: #00FF00; font-size: 0.95rem; text-align: center; font-weight: bold;'>⚠️ Un asesor se pondrá en contacto con usted para confirmar el costo total del servicio.</p>", unsafe_allow_html=True)
    
    submit_rs = st.form_submit_button("🚀 SOLICITAR AHORA")

# 5. ENVÍO WHATSAPP
if submit_rs:
    if nombre:
        n_txt = "SÍ" if is_neutral else "NO"
        g_txt = "SÍ" if is_giro else "NO"
        
        msg = (
            f"*NUEVA SOLICITUD OKGRUAS RS*\n"
            f"Buen día compañeros solicitando su apoyo\n"
            f"--------------------------------\n"
            f"👤 *Cliente:* {nombre}\n"
            f"🚗 *Auto:* {vehiculo if vehiculo else 'N/A'} ({año_auto if año_auto else 'N/A'})\n"
            f"🎨 *Color:* {color} | *Placas:* {placas_auto}\n"
            f"--------------------------------\n"
            f"📍 *Origen:* {punto_recoleccion if punto_recoleccion else 'Por confirmar'}\n"
            f"🏁 *Punto Destino:* {punto_destino if punto_destino else 'Por confirmar'}\n"
            f"🏠 *Destino:* {tipo_lugar}\n"
            f"--------------------------------\n"
            f"⚙️ *¿Neutral?:* {n_txt}\n"
            f"🔄 *¿Giran ruedas?:* {g_txt}\n"
            f"🚨 *Falla:* {falla_tipo}\n"
            f"📝 *Notas:* {notas_serv}\n"
            f"--------------------------------\n"
            f"🧐 *Pendiente cotización final por asesor.*"
        )
        
        link_ws = f"https://wa.me/528143029578?text={urllib.parse.quote(msg)}"
        st.markdown(f'''
            <a href="{link_ws}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #00FF00; color: black; padding: 15px; border-radius: 10px; width: 100%; text-align: center; font-weight: bold; font-size: 18px;">
                    ✅ ENVIAR POR WHATSAPP
                </div>
            </a>
        ''', unsafe_allow_html=True)
    else:
        st.error("⚠️ El nombre es necesario para el reporte.")

st.markdown("<br><p style='text-align: center; color: #444; font-size: 10px;'>OKGRUAS RS © 2026 | Logística Integral Monterrey</p>", unsafe_allow_html=True)
