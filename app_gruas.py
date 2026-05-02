import streamlit as st
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="OKGRUAS RS", page_icon="🚛", layout="centered")

# 2. Estilo Visual (Rosa y Oscuro)
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .stButton>button { 
        background-color: #FF69B4; 
        color: white; 
        border-radius: 10px; 
        width: 100%;
        font-weight: bold;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { background-color: #262626; color: white; border: 1px solid #FF69B4; }
    label { color: #FF69B4 !important; font-weight: bold; }
    .stSuccess { background-color: #1e1e1e; color: #25D366; border: 1px solid #25D366; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logo
try:
    st.image("logo.png", width=250)
except:
    st.markdown("<h1 style='color: #FF69B4;'>OKGRUAS RS</h1>", unsafe_allow_html=True)

# 4. Menú Lateral
menu = st.sidebar.radio("Menú", ["📱 Cotizador", "📊 Admin"])

if menu == "📱 Cotizador":
    st.title("Cotizador y Calculadora")
    
    with st.form("cotizador"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Tu Nombre")
            modelo = st.text_input("Modelo del Auto")
        with col2:
            origen = st.text_input("¿Dónde está el auto?")
            destino = st.text_input("¿A dónde va?")
        
        detalle_falla = st.text_area("Detalle del coche (¿Qué le pasó? ¿Está bloqueado?)")
        
        st.write("---")
        st.write("### 💰 Calculadora de Costo Estimado")
        distancia = st.number_input("Kilómetros aproximados (solo números)", min_value=0, value=0)
        
        # Lógica de precios (Puedes ajustar estos valores)
        banderazo = 600
        costo_km = 30
        total_estimado = banderazo + (distancia * costo_km) if distancia > 0 else 0
        
        if total_estimado > 0:
            st.info(f"Costo aproximado: ${total_estimado} MXN")
        
        btn_enviar = st.form_submit_button("📩 ENVIAR SOLICITUD POR WHATSAPP")

    if btn_enviar:
        if nombre and modelo and destino:
            # Construcción del mensaje
            texto = (
                f"Hola, soy {nombre}. Solicito servicio para un {modelo}.\n"
                f"📍 Recoger en: {origen}\n"
                f"🏁 Entrega en: {destino}\n"
                f"🛠️ Detalle: {detalle_falla}\n"
                f"🛣️ Distancia: {distancia} km\n"
                f"💰 Estimado: ${total_estimado} MXN"
            )
            mensaje_url = urllib.parse.quote(texto)
            
            # --- PON TU NÚMERO AQUÍ ---
            mi_numero = "528143029578" 
            whatsapp_link = f"https://wa.me/{mi_numero}?text={mensaje_url}"
            
            st.success("¡Cotización lista! Haz clic abajo para enviarla.")
            st.markdown(f'''
                <a href="{whatsapp_link}" target="_blank">
                    <button style="background-color: #25D366; color: white; padding: 15px; border: none; border-radius: 10px; width: 100%; cursor: pointer; font-weight: bold;">
                        ✅ CONFIRMAR Y ENVIAR WHATSAPP
                    </button>
                </a>
            ''', unsafe_allow_html=True)
        else:
            st.error("Por favor llena Nombre, Modelo y Destino.")

elif menu == "📊 Admin":
    st.title("Panel Interno")
    password = st.text_input("Contraseña", type="password")
    if password == "RS2026":
        st.success("Acceso Total")
        st.write("Aquí podrás ver reportes en el futuro.")
