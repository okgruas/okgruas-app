import streamlit as st
import urllib.parse

# 1. CONFIGURACIÓN
st.set_page_config(page_title="OKGRUAS RS - Auxilio Vial", page_icon="🚨", layout="centered")

# 2. ESTILO VISUAL "NEÓN RS" + BOTONES ESPECIALES
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
    
    /* Botón de Pánico Rojo Vibrante */
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
    
    /* Botón de Llamada */
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

# --- SECCIÓN DE EMERGENCIA ---
st.markdown('<a href="tel:8143029578" class="panic-button">🚨 BOTÓN DE PÁNICO: LLAMAR AHORA</a>', unsafe_allow_html=True)
st.markdown('<a href="tel:8143029578" class="call-button">📞 CONTACTO DIRECTO A GRUEROS</a>', unsafe_allow_html=True)

st.divider()

# 4. FORMULARIO TÉCNICO
st.markdown("### 📋 Datos del Servicio")
with st.form("form_rs_final"):
    nombre = st.text_input("Nombre del Cliente")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        vehiculo = st.text_input("Marca y Modelo")
        año_auto = st.text_input("Año")
    with col_v2:
        color = st.text_input("Color")
        placas_auto = st.text_input("Placas")

    st.divider()
    
    punto_recoleccion = st.text_input("📍 Punto de Recolección (Calle/Colonia/Cruce)")
    st.markdown("<p style='color: #888; font-size: 0.8rem; margin-top: -15px;'>(Si desconoce la ubicación, se enviará su GPS automático al confirmar)</p>", unsafe_allow_html=True)
    
    punto_destino = st.text_input("🏁 Punto Destino")
    
    st.divider()
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        falla_tipo = st.selectbox("Problema", ["Falla Mecánica", "Choque", "Llanta", "Batería", "Bloqueado"])
    with col_f2:
        zona_serv = st.selectbox("Zona Sugerida", ["Local (Mty)", "Foráneo"])

    notas_serv = st.text_area("Notas adicionales")
    
    submit_rs = st.form_submit_button("🚀 SOLICITAR GRÚA Y ENVIAR UBICACIÓN")

# 5. LÓGICA DE WHATSAPP + UBICACIÓN GPS
if submit_rs:
    if nombre:
        # Link de ubicación GPS para que te llegue al hacer click
        gps_link = "https://www.google.com/maps/search/?api=1&query=Mi+Ubicacion"
        
        msg = (
            f"*🚨 SOLICITUD DE AUXILIO VIAL - OKGRUAS RS*\n"
            f"--------------------------------\n"
            f"👤 *Cliente:* {nombre}\n"
            f"🚗 *Auto:* {vehiculo} {año_auto} ({color})\n"
            f"🔢 *Placas:* {placas_auto}\n"
            f"--------------------------------\n"
            f"📍 *Origen:* {punto_recoleccion if punto_recoleccion else 'Ver GPS abajo'}\n"
            f"🏁 *Destino:* {punto_destino}\n"
            f"🚨 *Falla:* {falla_tipo}\n"
            f"📝 *Notas:* {notas_serv}\n"
            f"--------------------------------\n"
            f"📍 *UBICACIÓN GPS:* {gps_link}\n"
            f"--------------------------------\n"
            f"🧐 *Favor de contactar para confirmar costo.*"
        )
        
        link_ws = f"https://wa.me/528143029578?text={urllib.parse.quote(msg)}"
        st.markdown(f'''
            <a href="{link_ws}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #00FF00; color: black; padding: 20px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 1.2rem; box-shadow: 0 0 15px rgba(0,255,0,0.4);">
                    ✅ CONFIRMAR Y ENVIAR POR WHATSAPP
                </div>
            </a>
        ''', unsafe_allow_html=True)
    else:
        st.error("⚠️ El nombre es necesario para procesar tu auxilio.")

# 6. PANEL ADMIN
st.write("<br><br>", unsafe_allow_html=True)
with st.expander("🔐 Acceso Administrativo"):
    clave_admin = st.text_input("Introduce Clave", type="password")
    if clave_admin == "RS1020":
        st.success("Acceso Confirmado")
        monto_serv = st.number_input("Costo pactado ($)", value=800)
        st.metric("Comisión OKGRUAS (10%)", f"${monto_serv * 0.10:,.2f}")

st.markdown("<br><p style='text-align: center; color: #444; font-size: 10px;'>OKGRUAS RS © 2026 | Logística Integral Monterrey</p>", unsafe_allow_html=True)
