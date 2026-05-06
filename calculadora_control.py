import streamlit as st
import urllib.parse
from datetime import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="OKGRUAS RS - Auditoría", page_icon="🚛")

# --- LÓGICA DE FOLIO CONSECUTIVO ---
# Por ahora, usaremos un contador de sesión. 
# Para que sea permanente entre días, conectaremos Google Sheets en el siguiente paso.
if 'ultimo_folio' not in st.session_state:
    st.session_state['ultimo_folio'] = 1  # Aquí puedes cambiar el número inicial

def generar_folio():
    num = st.session_state['ultimo_folio']
    return f"RS2014-{num}"

# --- INTERFAZ ---
st.markdown("<h1 style='color: #00FF00;'>🚛 OKGRUAS RS CONTROL</h1>", unsafe_allow_html=True)
st.divider()

# ENTRADA DE DATOS
col1, col2 = st.columns(2)
with col1:
    cliente_nombre = st.text_input("Nombre del Cliente:")
    cliente_whatsapp = st.text_input("WhatsApp (10 dígitos):")
with col2:
    km = st.number_input("Kilómetros:", min_value=0.0)
    total_final = st.number_input("Total a Cobrar ($):", min_value=0.0)

# CÁLCULOS INTERNOS
utilidad_yaja = total_final * 0.15
pago_socio = total_final - utilidad_yaja
folio_actual = generar_folio()
fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")

# SECCIÓN DE ENVÍO Y REGISTRO
st.divider()
if st.button("📝 REGISTRAR SERVICIO Y GENERAR WHATSAPP"):
    # 1. Incrementamos el folio para el siguiente
    st.session_state['ultimo_folio'] += 1
    
    # 2. Preparamos el mensaje
    texto = (f"*OKGRUAS RS - COTIZACIÓN*\n"
             f"🆔 *Folio: {folio_actual}*\n"
             f"📅 Fecha: {fecha_hoy}\n"
             f"👤 Cliente: {cliente_nombre}\n"
             f"💰 TOTAL: ${total_final:,.2f}\n"
             f"--------------------------\n"
             f"Reportar a: 528143029578")
    
    # 3. Generamos el link
    clean_phone = "".join(filter(str.isdigit, cliente_whatsapp))
    num_dest = "52" + clean_phone if len(clean_phone) == 10 else clean_phone
    link_ws = f"https://wa.me/{num_dest}?text={urllib.parse.quote(texto)}"
    
    st.success(f"✅ Servicio {folio_actual} registrado en el sistema local.")
    st.markdown(f'<a href="{link_ws}" target="_blank"><button style="width:100%; background-color:#25d366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">📲 ABRIR WHATSAPP DEL CLIENTE</button></a>', unsafe_allow_html=True)
    
    # NOTA PARA YAJAIRA: Aquí es donde se dispara la orden al Excel
    st.info("💡 Tip: Para que se guarde en tu Excel de Google Sheets automáticamente, necesitamos conectar tu 'Streamlit Secret'. ¿Quieres que te enseñe cómo hacerlo?")

st.markdown(f"<p style='text-align:center; color:gray;'>Folio actual: {folio_actual}</p>", unsafe_allow_html=True)
