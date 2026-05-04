import streamlit as st
import pandas as pd
import os

# Configuración de página
st.set_page_config(page_title="OKGRUAS RS", layout="wide")
st.title("🏗️ OKGRUAS RS - Catálogo de Servicios")

# --- FUNCIÓN DE EMERGENCIA ---
def cargar_datos():
    # Intentamos con el nombre estándar
    archivo = "autos.csv"
    
    if not os.path.exists(archivo):
        # SI NO EXISTE, CREAMOS UNO DE PRUEBA PARA QUE NO SALGA ERROR
        datos_prueba = {
            'nombre': ['Servicio de Prueba 1', 'Servicio de Prueba 2'],
            'precio': [1500, 2000],
            'img': ['fotos/grua1.jpg', 'fotos/grua2.jpg'],
            'detalles': ['Descripción de prueba', 'Descripción de prueba'],
            'socio': ['Socio A', 'Socio B']
        }
        df_temp = pd.DataFrame(datos_prueba)
        df_temp.to_csv(archivo, index=False)
        return df_temp
    
    try:
        df = pd.read_csv(archivo)
        df.columns = df.columns.str.strip().lower()
        return df
    except:
        return None

df_datos = cargar_datos()

# --- BARRA LATERAL ---
st.sidebar.header("Administración")
clave = st.sidebar.text_input("Clave Admin:", type="password")
es_admin = (clave == "RS1020")

# --- DISEÑO ---
if df_datos is not None:
    st.info("✅ **Garantía RS:** Tu seguridad es nuestra prioridad. Nosotros respondemos.")
    
    cols = st.columns(3)
    for i, (index, row) in enumerate(df_datos.iterrows()):
        with cols[i % 3]:
            # Imagen con "paracaídas"
            ruta = str(row.get('img', '')).strip()
            if os.path.exists(ruta):
                st.image(ruta, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300/172b4d/ffffff?text=OKGRUAS+RS", use_container_width=True)
            
            st.subheader(row.get('nombre', 'Servicio'))
            precio = row.get('precio', 0)
            st.metric("Precio", f"${precio:,.0f}")
            
            with st.expander("Ver más"):
                st.write(row.get('detalles', 'Disponible 24/7'))
                st.link_button("WhatsApp 💬", f"https://wa.me/521234567890?text=Servicio")

            if es_admin:
                st.divider()
                st.write(f"👤 **Socio:** {row.get('socio', 'Pendiente')}")
                st.success(f"💰 **Comisión (10%):** ${float(precio)*0.10:,.2f}")
