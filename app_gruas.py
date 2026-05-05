import streamlit as st
import urllib.parse
from streamlit_js_eval import streamlit_js_eval

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
    hr { border-top: 1px solid #00FF00 !important; }

    /* Botón de llamada al final */
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

    @media print {
        body, .stApp { background-color: #000000 !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
        h1, h2, h3, label, p, span, b { color: #00FF00 !important; -webkit-print-color-adjust: exact !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- OBTENCIÓN DE UBICACIÓN GPS ---
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
    st.markdown("<p style='color: #888;'>Servicio en Monterrey Área Metropolitana y Otros Municipios</p>", unsafe_allow_html=True)

st.divider()

# --- RECOMENDACIONES DE SEGURIDAD ---
with st.expander("🛡️ RECOMENDACIONES DE SEGURIDAD (Leer importante)"):
    st.markdown("""
    * **Mantén la calma:** Ya estamos en camino.
    * **Encienda luces intermitentes:** Hazte visible para otros conductores.
    * **Baje del vehículo:** Si es seguro, resguárdate fuera del arroyo vehicular.
    * **No acepte ayuda de extraños:** Espere a la unidad oficial identificada.
    """)

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
    
    punto_recoleccion = st.text_input("📍 Punto de Recolección (Manual)")
    st.markdown("<p style='color: #888; font-size: 0.8rem; margin-top: -15px;'>(Si desconoce la ubicación, se le brindara apoyo)</p>", unsafe_allow_html=True)
    
    punto_destino = st.text_input("🏁 Punto Destino")
    
    st.divider()
    st.markdown("#### 🛠️ Estado del Vehículo")
    cf1, cf2 = st.columns(2)
    with cf1:
        is_neutral = st.checkbox("¿Se puede poner en neutral?")
        is_giro = st.checkbox("¿Ruedas y volante giran?")
    with cf2:
        falla_tipo = st.selectbox("Problema", ["Falla Mecánica", "Choque", "Llanta", "Batería", "Falta de Gasolina", "Bloqueado"])

    notas_serv = st.text_area("Notas adicionales")
    st.markdown("<p style='color: #00FF00; font-weight: bold; text-align: center;'>⚠️ Al confirmar, se abrirá WhatsApp con tus datos y un asesor le enviara costo total del servicio.</p>", unsafe_allow_html=True)
    
    submit_rs = st.form_submit_button("🚀 ENVIAR SOLICITUD PARA COTIZACION")

# 5. LÓGICA WHATSAPP
if submit_rs:
    if nombre:
        gps_final = lat_long_str if lat_long_str else "GPS no activado por el usuario"
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
            f"📍 *Origen:* {punto_recoleccion if punto_recoleccion else 'Ver GPS abajo'}\n"
            f"🏁 *Punto Destino:* {punto_destino}\n"
            f"--------------------------------\n"
            f"⚙️ *Neutral:* {n_txt} | *Gira:* {g_txt}\n"
            f"🚨 *Falla:* {falla_tipo}\n"
            f"📍 *GPS:* {gps_final}\n"
            f"📝 *Notas:* {notas_serv}\n"
            f"--------------------------------\n"
            f"🧐 *Pendiente cotización final.*"
        )
        link_ws = f"https://wa.me/528143029578?text={urllib.parse.quote(msg)}"
        st.markdown(f'<a href="{link_ws}" target="_blank"><div style="background-color: #00FF00; color: black; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 1.2rem;">✅ ENVIAR POR WHATSAPP</div></a>', unsafe_allow_html=True)
    else:
        st.error("⚠️ El nombre es necesario para continuar.")

# --- 6. BOTÓN DE LLAMADA AL FINAL (TUS PETICIÓN) ---
st.markdown('<a href="tel:8143029578" class="call-footer">📞 LLAMADA DE EMERGENCIA: 81 4302 9578</a>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #444; font-size: 10px;'>OKGRUAS RS © 2026 | Logística Integral Monterrey</p>", unsafe_allow_html=True)
