import streamlit as st
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="OKGRUAS RS", page_icon="🚛", layout="centered")

# 2. Estilo Visual
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
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input { 
        background-color: #262626 !important; color: white !important; border: 1px solid #FF69B4 !important; 
    }
    label { color: #FF69B4 !important; font-weight: bold; }
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
        st.caption("Introduce los KM (Sujeto a verificación por el operador)")
        distancia = st.number_input("Kilómetros según Maps", min_value=0, value=0)
        
        # Lógica de precios
        banderazo = 600
        costo_km = 30
        total = banderazo + (distancia * costo_km) if distancia > 0 else banderazo
        
        # --- AQUÍ ESTÁ EL CAMBIO ---
        st.info(f"Costo base (Banderazo): ${banderazo} MXN")
        st.write(f"➕ Costo por kilómetro: **${costo_km} MXN**") # <-- Esta es la línea nueva
        
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
            mi_numero = "528132454641" 
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
        st.write("Bienvenida, Yajaira.")
