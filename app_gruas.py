import streamlit as st
import pandas as pd
import os

# 1. Configuración idéntica a tu diseño favorito
st.set_page_config(page_title="OKGRUAS RS", layout="wide")

st.title("🏗️ OKGRUAS RS - Catálogo de Servicios")

# --- CARGA DE DATOS SEGURA ---
def cargar_datos():
    archivo = "autos.csv"  # Asegúrate que este archivo tenga la columna 'socio'
    if not os.path.exists(archivo):
        return None
    try:
        df = pd.read_csv(archivo)
        df.columns = df.columns.str.strip().lower()
        df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
        return df.dropna(subset=['nombre', 'precio'])
    except:
        return None

df_datos = cargar_datos()

# --- BARRA LATERAL (Filtros + Acceso Admin) ---
st.sidebar.header("Filtros de Búsqueda")
precio_max = st.sidebar.slider("Presupuesto Máximo", 0, 1500000, 500000)
buscar = st.sidebar.text_input("Buscar servicio:")

st.sidebar.markdown("---")
# La "Puerta Secreta"
es_admin = st.sidebar.checkbox("🔒 Modo Administrador")

# --- RENDERIZADO DEL CATÁLOGO (Lo que ve el cliente) ---
if df_datos is not None and not df_datos.empty:
    
    # Leyenda de garantía simple (Lo que me pediste)
    st.info("✅ **Garantía RS:** Si surge algún detalle con el servicio, la empresa responde. Tu tranquilidad es primero.")

    # Filtramos
    df_filtrado = df_datos[
        (df_datos['precio'] <= precio_max) & 
        (df_datos['nombre'].str.contains(buscar, case=False, na=False))
    ]

    # Diseño de 3 columnas (Exactamente como antes)
    cols = st.columns(3)

    for i, (index, row) in enumerate(df_filtrado.iterrows()):
        with cols[i % 3]:
            # Imagen local
            ruta_foto = str(row['img']).strip()
            if os.path.exists(ruta_foto):
                st.image(ruta_foto, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300/172b4d/ffffff?text=OKGRUAS+RS", use_container_width=True)
            
            st.subheader(row["nombre"])
            st.metric("Precio", f"${row['precio']:,.0f}")
            
            # Parte pública: Detalles y WhatsApp
            with st.expander("Ver detalles del servicio"):
                st.write(row.get("detalles", "Servicio disponible en Monterrey y área metropolitana."))
                url_wa = f"https://wa.me/521234567890?text=Hola, me interesa el servicio: {row['nombre']}"
                st.link_button("Solicitar Grúa 💬", url_wa)
            
            # --- PARTE PRIVADA (Solo aparece si marcas el checkbox y pones la clave) ---
            if es_admin:
                clave = st.sidebar.text_input("Introduce clave Admin:", type="password", key="admin_key")
                if clave == "RS1020":
                    st.markdown("---")
                    st.warning(f"🕵️ **Info Socio:** {row.get('socio', 'No asignado')}")
                    comision = row['precio'] * 0.10
                    st.success(f"💰 **Tu Comisión (10%):** ${comision:,.2f}")
                elif clave != "":
                    st.sidebar.error("Clave incorrecta")

else:
    st.warning("⚠️ No encontré el archivo 'autos.csv'. Revisa que esté en la carpeta.")

# Pie de página simple
st.markdown("---")
st.caption("OKGRUAS RS - Líderes en logística y rescate.")
