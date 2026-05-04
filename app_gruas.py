import streamlit as st
import urllib.parse

# 1. CONFIGURACIÓN
st.set_page_config(page_title="OKGRUAS RS - Cotización", page_icon="🚛", layout="centered")

# 2. ESTILO VISUAL "NEÓN RS" + PARCHE DE IMPRESIÓN
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
    hr { border-top: 1px solid #00FF00 !important; }

    /* Estilo para el botón de llamada */
    .call-button {
        display: block;
        background-color: #1A1A1A;
        color: #00FF00 !important;
        border: 2px solid #00FF00;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 20px;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.2);
    }

    @media print {
        body, .stApp { background-color: #000000 !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
        h1, h2, h3, label, p, span, b { color: #00FF00 !important; -webkit-print-color-adjust: exact !important; }
        .stTextInput>div>div>input, .stSelectbox>div>div>div { background-color: #1A1A1A !important; border: 1px solid #00FF00 !important; color: #00FF00 !important; }
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

# --- BOTÓN DE LLAMADA DIRECTA (NUEVO) ---
st.markdown('<a href="tel:8143029578" class="call-button">📞 LLAMAR AHORA: 81 4302 9578</a>', unsafe_allow_html=True)

st.divider()

# --- TARIFAS ---
st.markdown("### 💰 Tarifas Base")
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
        color_auto = st.text_input("Color del Auto")
    with col_v2:
        vehiculo = st.text_input("Marca y Modelo")
        placas_auto = st.text_input("Placas")
        zona_serv = st.selectbox("Zona Sugerida", ["Local (Mty)", "Foráneo"])

    st.divider()
    
    punto_recoleccion = st.text_input("📍 Punto de Recolección")
    st.markdown("<p style='color: #888; font-size: 0.8rem; margin-top: -15px;'>(Si desconoce la ubicación, un asesor le contactará para apoyarle)</p>", unsafe_allow_html=True)
    
    punto_destino = st.text_input("🏁 Punto Destino")
    
    st.divider()
    st.markdown("#### 🛠️ Estado del Vehículo")
    cf1, cf2 = st.columns(2)
    with cf1:
        is_neutral = st.checkbox("¿Se puede poner en neutral?")
        is_giro = st.checkbox("¿Ruedas y volante giran?")
    with cf2:
        falla_tipo = st.selectbox("Problema", ["Falla Mecánica", "Choque", "Llanta", "Batería", "Bloqueado"])

    notas_serv = st.text_area("Notas adicionales")
    st.markdown("<p style='color: #00FF00; font-weight: bold; text-align: center;'>⚠️ Un asesor confirmará el costo total del servicio.</p>", unsafe_allow_html=True)
    
    submit_rs = st.form_submit_button("🚀 ENVIAR SOLICITUD")

# 5. LÓGICA WHATSAPP
if submit_rs:
    if nombre:
        n_txt = "SÍ" if is_neutral else "NO"
        g_txt = "SÍ" if is_giro else "NO"
        msg = (
            f"*NUEVA SOLICITUD OKGRUAS RS*\n"
            f"Buen día compañeros solicitando su apoyo\n"
            f"--------------------------------\n"
            f"👤 *Cliente:* {nombre}\n"
            f"🚗 *Auto:* {vehiculo} ({año_auto})\n"
            f"🎨 *Color:* {color_auto} | *Placas:* {placas_auto}\n"
            f"--------------------------------\n"
            f"📍 *Origen:* {punto_recoleccion if punto_recoleccion else 'Por confirmar por asesor'}\n"
            f"🏁 *Punto Destino:* {punto_destino}\n"
            f"--------------------------------\n"
            f"⚙️ *Neutral:* {n_txt} | *Gira:* {g_txt}\n"
            f"🚨 *Falla:* {falla_tipo}\n"
            f"📝 *Notas:* {notas_serv}\n"
            f"--------------------------------\n"
            f"🧐 *Pendiente cotización final.*"
        )
        link_ws = f"https://wa.me/528143029578?text={urllib.parse.quote(msg)}"
        st.markdown(f'<a href="{link_ws}" target="_blank"><div style="background-color: #00FF00; color: black; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold;">✅ ENVIAR POR WHATSAPP</div></a>', unsafe_allow_html=True)
    else:
        st.error("⚠️ El nombre es necesario para continuar.")

# 6. PANEL ADMIN
st.write("<br><br>", unsafe_allow_html=True)
with st.expander("🔐 Acceso Administrativo"):
    clave_admin = st.text_input("Introduce Clave", type="password")
    if clave_admin == "RS1020":
        st.success("Acceso Confirmado")
        monto_serv = st.number_input("Costo pactado ($)", value=800)
        st.metric("Comisión OKGRUAS (10%)", f"${monto_serv * 0.10:,.2f}")

st.markdown("<br><p style='text-align: center; color: #444; font-size: 10px;'>OKGRUAS RS © 2026 | Logística Integral Monterrey</p>", unsafe_allow_html=True)
