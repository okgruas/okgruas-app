import streamlit as st
import urllib.parse
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="OKGRUAS RS - Cotizador", page_icon="🚛", layout="centered")

# 2. ESTILO VISUAL (Cambiado de Rosa a Verde Neón para unificar)
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
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input { 
        background-color: #262626 !important; color: white !important; border: 1px solid #00FF00 !important; 
    }
    label { color: #00FF00 !important; font-weight: bold; }
    h1, h2, h3 { color: #00FF00 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. CABECERA (LOGO PEQUEÑO + NOMBRE)
col_head1, col_head2 = st.columns([1, 4])

with col_head1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=100)
    else:
        st.markdown("<h1 style='margin:0;'>🚛</h1>", unsafe_allow_html=True)

with col_head2:
    # AQUÍ ESTÁ EL NOMBRE QUE FALTABA
    st.markdown("<h1 style='margin-bottom: 0px; padding-top: 10px;'>OKGRUAS RS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; margin-top: 0px;'>Cotizador de Servicios</p>", unsafe_allow_html=True)

st.divider()

# 4. MENÚ LATERAL
menu = st.sidebar.radio("Menú", ["📱 Cotizador", "📊 Admin"])

if menu == "📱 Cotizador":
    st.title("Solicitud de Servicio")
    
    with st.form("cotizador"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Tu Nombre")
            modelo = st.text_input("Modelo del Auto")
        with col2:
            origen = st.text_input("¿Dónde está el auto?")
            destino = st.text_input("¿A dónde va?")
        
        tipo_falla = st.selectbox("¿Qué problema tiene el auto?", [
            "Falla Mecánica", 
            "Choque / Siniestro", 
            "Llanta Ponchada", 
            "Sin Batería", 
            "Auto Bloqueado",
            "Otro (Especificar en notas)"
        ])
        
        notas = st.text_area("Notas adicionales o detalles")
        
        st.write("---")
        st.write("### 💰 Calculadora de Costo Estimado")
        distancia = st.number_input("Kilómetros según Google Maps", min_value=0, value=0)
        
        # Lógica de precios
        banderazo = 800 # Ajustado a tu precio base
        costo_km = 25   # Ajustado a tu precio por KM
        total = banderazo + (distancia * costo_km)
        
        st.info(f"Costo base (Banderazo): ${banderazo} MXN")
        st.write(f"➕ Costo por kilómetro: **${costo_km} MXN**")
        
        if distancia > 0:
            st.success(f"Total Estimado: **${total} MXN**")
        
        btn_enviar = st.form_submit_button("📩 SOLICITAR GRÚA POR WHATSAPP")

    if btn_enviar:
        if nombre and modelo and destino:
            texto = (
                f"*SOLICITUD DE GRÚA - OKGRUAS RS*\n\n"
                f"👤 *Cliente:* {nombre}\n"
                f"🚗 *Vehículo:* {modelo}\n"
                f"🛠️ *Problema:* {tipo_falla}\n"
                f"📍 *Origen:* {origen}\n"
                f"🏁 *Destino:* {destino}\n"
                f"🛣️ *Distancia:* {distancia} km\n"
                f"💰 *Precio estimado:* ${total} MXN\n\n"
                f"📝 *Notas:* {notas}"
            )
            mensaje_url = urllib.parse.quote(texto)
            mi_numero = "528143029578" # TU NÚMERO ACTUALIZADO
            whatsapp_link = f"https://wa.me/{mi_numero}?text={mensaje_url}"
            
            st.markdown(f'''
                <a href="{whatsapp_link}" target="_blank">
                    <button style="background-color: #25D366; color: white; padding: 15px; border: none; border-radius: 10px; width: 100%; cursor: pointer; font-weight: bold;">
                        ✅ CONFIRMAR Y ENVIAR A WHATSAPP
                    </button>
                </a>
            ''', unsafe_allow_html=True)
        else:
            st.error("Por favor llena Nombre, Modelo y Destino.")

elif menu == "📊 Admin":
    st.title("Panel de Control")
    password = st.text_input("Contraseña", type="password")
    if password == "RS2026":
        st.success("Acceso autorizado")
        st.write("Bienvenida, Yajaira. Aquí puedes ver el registro de solicitudes (Próximamente).")
