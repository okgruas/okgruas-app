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
    
    /* Inputs y Checkboxes */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea { 
        background-color: #1A1A1A !important; color: #00FF00 !important; border: 1px solid #00FF00 !important; 
    }
    label { color: #00FF00 !important; font-weight: bold !important; }
    
    /* Estilo para los Checkboxes */
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
    clave = st.text_input("Clave", type="password")
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
    # Sección 1: Datos Generales
    col_a, col_b = st.columns(2)
    with col_a:
        nombre = st.text_input("Nombre del Cliente")
        vehiculo = st.text_input("Tipo de Vehículo (Marca y Modelo)")
        color = st.text_input("Color")
    with col_b:
        placas = st.text_input("Placas")
        año = st.text_input("Año")
        tipo_servicio = st.selectbox("Tipo de Servicio", ["Local (Mty)", "Foráneo"])

    st.divider()
    
    # Sección 2: Ubicación
    col_c, col_d = st.columns(2)
    with col_c:
        origen = st.text_input("📍 Punto de Recolección")
    with col_d:
        destino = st.text_input("🏁 Punto de Entrega")

    # Sección 3: Preguntas de Control (Checkboxes y Selects)
    st.markdown("#### 🛠️ Estado del Vehículo")
    c_check1, c_check2 = st.columns(2)
    with c_check1:
        neutral = st.checkbox("¿Se puede poner en neutral?")
        giro = st.checkbox("¿Ruedas y volante giran?")
    with c_check2:
        problema = st.selectbox("Problema principal", ["Falla Mecánica", "Choque", "Llanta", "Batería", "Bloqueado"])

    notas = st.text_area("Notas adicionales (ej. ¿Cuántos km extras son si es foráneo?)")
    
    st.markdown("""
    <div style="background-color: #111; padding: 10px; border-left: 5px solid #00FF00; margin-bottom: 15px;">
        <small style="color: #00FF00;"><b>NOTA:</b> El costo base es de $800. Servicios fuera del área metropolitana generan cargo de $25 por km.</small>
    </div>
    """, unsafe_allow_html=True)

    btn_enviar = st.form_submit_button("🚀 SOLICITAR COTIZACIÓN AHORA")

# 5. LÓGICA DE WHATSAPP
if btn_enviar:
    if nombre and vehiculo and origen and destino:
        # Convertir booleanos a texto amigable
        neutral_txt = "SÍ" if neutral else "NO"
        giro_txt = "SÍ" if giro else "NO"
        
        texto = (
            f"*NUEVA SOLICITUD - OKGRUAS RS*\n"
            f"--------------------------------\n"
            f"👤 *Cliente:* {nombre}\n"
            f"🚗 *Auto:* {vehiculo} ({año}) | *Color:* {color}\n"
            f"🆔 *Placas:* {placas}\n"
            f"📍 *Origen:* {origen}\n"
            f"🏁 *Destino:* {destino}\n"
            f"--------------------------------\n"
            f"⚙️ *¿Neutral?:* {neutral_txt}\n"
            f"🔄 *¿Giran ruedas/volante?:* {giro_txt}\n"
            f"🚨 *Falla:* {problema}\n"
            f"📝 *Notas:* {notas}\n"
            f"--------------------------------\n"
            f"💰 *Banderazo:* $800.00\n"
            f"🛣️ *Km Extra:* $25.00\n\n"
            f"*Favor de confirmar precio final y tiempo de llegada.*"
        )
        
        mensaje_url = urllib.parse.quote(texto)
        whatsapp_link = f"https://wa.me/528143029578?text={mensaje_url}"
        
        st.markdown(f'''
            <a href="{whatsapp_link}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #00FF00; color: black; padding: 18px; border-radius: 12px; width: 100%; text-align: center; font-weight: bold; font-size: 18px;">
                    ✅ CLICK PARA ENVIAR POR WHATSAPP
                </div>
            </a>
        ''', unsafe_allow_html=True)
    else:
        st.error("⚠️ Falta llenar datos obligatorios para la grúa.")

st.markdown("<br><p style='text-align: center; color: #333; font-size: 10px;'>OKGRUAS RS © 2026 | Logística Blindada</p>", unsafe_allow_html=True)
