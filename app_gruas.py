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
    .block-container { padding-top: 2rem !important; }
    html, body, [class*="css"], .stMarkdown { font-family: 'Montserrat', sans-serif; color: #FFFFFF !important; }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea { 
        background-color: #1A1A1A !important; color: #00FF00 !important; border: 1px solid #00FF00 !important; 
    }
    label { color: #00FF00 !important; font-weight: bold !important; }
    h1, h2, h3 { color: #00FF00 !important; text-shadow: 0 0 10px rgba(0, 255, 0, 0.3); }
    
    .stButton>button { 
        background-color: #00FF00 !important; color: #000000 !important; 
        border-radius: 12px; font-weight: bold; width: 100%; height: 3.5em;
    }
    
    /* BOTÓN DE LLAMADA AL FINAL (DISCRETO) */
    .call-footer {
        display: block;
        background-color: #1A1A1A;
        color: #FF0000 !important;
        border: 1px solid #FF0000;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.9rem;
        margin-top: 30px;
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

st.divider()

# 4. FORMULARIO DE DATOS
st.markdown("### 📋 Reporte de Asistencia")
with st.form("form_rs_v3"):
    nombre = st.text_input("Nombre del Cliente")
    
    col1, col2 = st.columns(2)
    with col1:
        vehiculo = st.text_input("Marca y Modelo")
        año_auto = st.text_input("Año")
    with col2:
        color = st.text_input("Color")
        placas = st.text_input("Placas")

    st.divider()
    
    punto_recoleccion = st.text_input("📍 Punto de Recolección (Calle/Cruce/Colonia)")
    st.markdown("<p style='color: #888; font-size: 0.8rem; margin-top: -15px;'>(Si no conoce la dirección exacta, el GPS se enviará al confirmar abajo)</p>", unsafe_allow_html=True)
    
    punto_destino = st.text_input("🏁 Punto Destino")
    
    # OPCIÓN DE GAS AGREGADA
    falla = st.selectbox("Problema o Falla", ["Falla Mecánica", "Choque", "Llanta Ponchada", "Batería / Paso de Corriente", "Falta de Gasolina", "Bloqueado / Llaves dentro"])
    
    notas = st.text_area("Notas adicionales")
    
    st.markdown("<p style='color: #00FF00; font-weight: bold; text-align: center;'>Al dar click se abrirá WhatsApp con su ubicación GPS</p>", unsafe_allow_html=True)
    submit_rs = st.form_submit_button("🚀 ENVIAR DATOS Y UBICACIÓN GPS")

# 5. LÓGICA DE WHATSAPP
if submit_rs:
    if nombre:
        gps_link = "https://www.google.com/maps/search/?api=1&query=mi+ubicacion"
        
        msg = (
            f"*🚨 SOLICITUD DE ASISTENCIA - OKGRUAS RS*\n"
            f"--------------------------------\n"
            f"👤 *Cliente:* {nombre}\n"
            f"🚗 *Auto:* {vehiculo} {año_auto} ({color})\n"
            f"🔢 *Placas:* {placas}\n"
            f"--------------------------------\n"
            f"📍 *Origen:* {punto_recoleccion if punto_recoleccion else 'Confirmar con GPS'}\n"
            f"🏁 *Destino:* {punto_destino}\n"
            f"🚨 *Situación:* {falla}\n"
            f"📝 *Notas:* {notas}\n"
            f"--------------------------------\n"
            f"📍 *UBICACIÓN GPS:* {gps_link}\n"
            f"--------------------------------\n"
            f"🧐 *Asesor: Proceder con cotización inmediata.*"
        )
        
        link_ws = f"https://wa.me/528143029578?text={urllib.parse.quote(msg)}"
        
        st.markdown(f'''
            <a href="{link_ws}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #00FF00; color: black; padding: 20px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 1.2rem; box-shadow: 0 0 15px rgba(0,255,0,0.5);">
                    ✅ CONFIRMAR ENVÍO POR WHATSAPP
                </div>
            </a>
        ''', unsafe_allow_html=True)
    else:
        st.error("⚠️ Por favor, ingresa tu nombre.")

# --- 6. BOTÓN DE LLAMADA AL FINAL (TU PETICIÓN) ---
st.markdown('<a href="tel:8143029578" class="call-footer">📞 ¿No puedes escribir? Llamar a Central de Grúas</a>', unsafe_allow_html=True)

# 7. PANEL ADMIN
st.write("<br><br>", unsafe_allow_html=True)
with st.expander("🔐 Panel Administrativo"):
    clave = st.text_input("Clave", type="password")
    if clave == "RS1020":
        monto = st.number_input("Costo del servicio ($)", value=800)
        st.metric("Comisión (10%)", f"${monto * 0.10:,.2f}")

st.markdown("<br><p style='text-align: center; color: #444; font-size: 10px;'>OKGRUAS RS © 2026 | Logística Integral Monterrey</p>", unsafe_allow_html=True)
