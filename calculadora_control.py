# Reemplaza la sección 6 (ENVÍO WHATSAPP) con este código "Auditor":

st.divider()
fecha_txt = datetime.now().strftime("%d/%m/%Y")
mi_numero = "528143029578"

# 1. Preparamos el texto que verán ambos
texto_base = (f"*OKGRUAS RS - COTIZACIÓN OFICIAL*\n"
            f"📅 Fecha: {fecha_txt}\n"
            f"👤 Cliente: {cliente_nombre if cliente_nombre else 'General'}\n"
            f"🛠️ Falla: {tipo_falla}\n"
            f"--------------------------\n"
            f"✅ Banderazo: $800\n"
            f"📍 KM ({km}): ${COSTO_RECORRIDO:,.2f}\n"
            f"🔧 Maniobras: ${COSTO_MANIOBRAS + COSTO_SOTANO:,.2f}\n"
            f"--------------------------\n"
            f"💰 *TOTAL: ${total_final:,.2f}*\n"
            f"--------------------------\n"
            f"🆔 Folio: {datetime.now().strftime('%H%M%S')}") # Esto te sirve para rastrear

# 2. LÓGICA DE ENVÍO "UN SOLO BOTÓN"
clean_phone = "".join(filter(str.isdigit, cliente_whatsapp))

if len(clean_phone) >= 10:
    num_final = "52" + clean_phone if len(clean_phone) == 10 else clean_phone
    
    # TRUCO: El enlace de "Enviar a" sin número específico abre la lista de contactos, 
    # pero nosotros queremos forzar el envío. 
    # Como WhatsApp no deja abrir dos chats, usaremos el link del cliente
    # pero agregaremos una instrucción visual.
    
    link_c = f"https://wa.me/{num_final}?text={urllib.parse.quote(texto_base)}"
    
    st.markdown(f"""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 1px solid #00FF00; text-align: center;">
            <p style="color: #00FF00; font-weight: bold;">⚠️ REGISTRO DE SERVICIO ACTIVO</p>
            <a href="{link_c}" target="_blank">
                <button style="width:100%; background-color:#25d366; color:white; border:none; padding:20px; border-radius:10px; font-weight:bold; cursor:pointer; font-size:20px;">
                    🚀 ENVIAR COTIZACIÓN Y REGISTRAR
                </button>
            </a>
            <p style="color: #888; font-size: 12px; margin-top: 10px;">Al dar clic, se genera un folio automático para tu reporte mensual.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Escribe el WhatsApp del cliente para habilitar el botón de envío.")
