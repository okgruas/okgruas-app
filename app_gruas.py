import streamlit as st
import pandas as pd
import os

# 1. Configuración (Igual que tu diseño favorito)
st.set_page_config(page_title="OKGRUAS RS", layout="wide")

st.title("🏗️ OKGRUAS RS - Catálogo de Servicios")

# --- CARGA DE DATOS ---
def cargar_datos():
    # Usamos el nombre del archivo que acordamos ayer
    archivo = "autos.csv" 
    if not os.path.exists(archivo):
        return None
    try:
        df = pd.read_csv(archivo)
        # Limpieza de nombres de columnas
        df.columns = df.columns.str.strip().lower()
        # Forzar que precio sea número
        df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
        return df.dropna(subset=['nombre']) # Que al menos tenga nombre
    except:
        return None

df_datos = cargar_datos()

# --- BARRA LATERAL (Filtros + La Llave Maestra) ---
st.sidebar.header("Configuración")
precio_max = st.sidebar.slider("Presupuesto Máximo", 0, 1500000, 1000000)
buscar = st.sidebar.text_input("Buscar servicio:")

st.sidebar.markdown("---")
st.sidebar.subheader("🔒 Área Administrativa")
clave = st.sidebar.text_input("Introduce clave Admin:", type="password")
es_admin = (clave == "RS1020")

if clave != "" and not es_admin:
    st.sidebar.error("Clave incorrecta")

# --- CUERPO DEL PROGRAMA ---
if df_datos is not None and not df_datos.empty:
    
    # La leyenda de garantía que me pediste
    st.info("✅ **Garantía RS:** Si surge algún detalle con el servicio, la empresa responde. Tu tranquilidad es primero.")

    # Filtros
    df_filtrado = df_datos[
        (df_datos['precio'] <= precio_max) & 
        (df_datos['nombre'].str.contains(buscar, case=False, na=False))
    ]

    # Diseño de 3 columnas
    cols = st.columns(3)

    for i, (index, row) in enumerate(df_filtrado.iterrows()):
        with cols[i % 3]:
            # Fotos
            ruta_foto = str(row['img']).strip()
            if os.path.exists(ruta_foto):
                st.image(ruta_foto, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300/172b4d/ffffff?text=OKGRUAS+RS", use_container_width=True)
            
            st.subheader(row["nombre"])
            
            # Solo mostrar precio si existe
            valor_precio = row['precio'] if pd.notnull(row['precio']) else 0
            st.metric("Precio", f"${valor_precio:,.0f}")
            
            # Detalles Públicos
            with st.expander("Ver especificaciones"):
                st.write(row.get("detalles", "Servicio disponible en Monterrey."))
                st.link_button("Solicitar Grúa 💬", f"https://wa.me/521234567890?text=Servicio:{row['nombre']}")
            
            # --- INFO DE SOCIOS (Solo si la clave es correcta) ---
            if es_admin:
                st.markdown("---")
                socio_nombre = row.get('socio', 'Sin asignar')
                st.warning(f"👤 **Socio:** {socio_nombre}")
                comision = valor_precio * 0.10
                st.success(f"💰 **Comisión (10%):** ${comision:,.2f}")

else:
    st.error("⚠️ No se pudo leer el archivo 'autos.csv'.")
    st.info("Crea un archivo llamado autos.csv en VS Code y pega esto:\n\nnombre,precio,img,detalles,socio\nGrúa Plataforma,1500,fotos/grua1.jpg,Servicio local,Juan Perez")

st.markdown("---")
st.caption("OKGRUAS RS - Monterrey, N.L.")
