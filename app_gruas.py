import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="OKGRUAS RS", layout="wide")
st.title("🏗️ OKGRUAS RS - Catálogo de Servicios")

# --- CARGA DE DATOS ---
def cargar_datos():
    archivo = "autos.csv" 
    if not os.path.exists(archivo):
        return None
    try:
        # Cargamos el archivo y limpiamos nombres de columnas
        df = pd.read_csv(archivo)
        df.columns = df.columns.str.strip().lower()
        return df
    except:
        return None

df_datos = cargar_datos()

# --- BARRA LATERAL ---
st.sidebar.header("Área Administrativa")
clave = st.sidebar.text_input("Clave Admin:", type="password")
es_admin = (clave == "RS1020") # Tu clave secreta

# --- DISEÑO DE CUADROS ---
if df_datos is not None:
    st.info("✅ **Garantía RS:** Si surge algún detalle, nosotros respondemos.")
    
    # Creamos las 3 columnas que te gustan
    cols = st.columns(3)
    
    for i, (index, row) in enumerate(df_datos.iterrows()):
        with cols[i % 3]:
            # Imagen
            ruta = str(row.get('img', '')).strip()
            if os.path.exists(ruta):
                st.image(ruta, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300/172b4d/ffffff?text=OKGRUAS+RS", use_container_width=True)
            
            st.subheader(row.get('nombre', 'Servicio RS'))
            
            # Precio
            precio = row.get('precio', 0)
            st.metric("Precio", f"${precio:,.0f}")
            
            with st.expander("Ver más"):
                st.write(row.get('detalles', 'Disponible 24/7'))
                st.link_button("WhatsApp 💬", f"https://wa.me/521234567890?text=Servicio:{row['nombre']}")
            
            # Si eres admin, ves al socio y tu 10%
            if es_admin:
                st.divider()
                st.write(f"👤 **Socio:** {row.get('socio', 'Pendiente')}")
                st.write(f"💰 **Comisión (10%):** ${float(precio)*0.10:,.2f}")
else:
    st.error("⚠️ No encuentro el archivo 'autos.csv' en tu carpeta de Proyectos_Python.")
