import streamlit as st
import pandas as pd
import os

# 1. Configuración de la página
st.set_page_config(page_title="OKGRUAS RS - Gestión", layout="wide", page_icon="🏗️")

# --- FUNCIÓN DE CARGA DE DATOS ---
def cargar_datos():
    archivo = "servicios_gruas.csv"
    if not os.path.exists(archivo):
        # Creamos un archivo de ejemplo si no existe
        df = pd.DataFrame(columns=['fecha', 'cliente', 'servicio', 'monto', 'socio'])
        df.to_csv(archivo, index=False)
        return df
    return pd.read_csv(archivo)

df_servicios = cargar_datos()

# --- BARRA LATERAL (Acceso Secreto) ---
st.sidebar.title("Configuración")
modo_admin = st.sidebar.checkbox("Acceso Administrador")

# --- VISTA PÚBLICA (Lo que todos ven) ---
st.title("🏗️ OKGRUAS RS - Servicios de Asistencia")

st.info("✨ **Compromiso RS:** Tu seguridad es nuestra prioridad. En OKGRUAS RS respaldamos cada servicio para tu total tranquilidad. Si surge cualquier inconveniente, nosotros respondemos.")

# Buscador para clientes
buscar = st.text_input("🔍 Buscar mi servicio (por nombre de cliente):")

if not df_servicios.empty:
    # Mostramos solo información pública
    vista_publica = df_servicios[['fecha', 'servicio', 'cliente']]
    if buscar:
        vista_publica = vista_publica[vista_publica['cliente'].str.contains(buscar, case=False)]
    
    st.subheader("Servicios en Curso / Finalizados")
    st.dataframe(vista_publica, use_container_width=True)
else:
    st.write("No hay servicios registrados por el momento.")

# --- VISTA ADMINISTRADOR (Solo con la 'llave') ---
if modo_admin:
    st.sidebar.markdown("---")
    password = st.sidebar.text_input("Introduce tu clave:", type="password")
    
    if password == "RS1020": # <--- ESTA ES TU CLAVE SECRETA
        st.markdown("---")
        st.header("📊 Panel de Control de Socios (Privado)")
        
        if not df_servicios.empty:
            # Cálculos automáticos
            df_servicios['monto'] = pd.to_numeric(df_servicios['monto'], errors='coerce')
            df_servicios['comision'] = df_servicios['monto'] * 0.10
            
            # Métricas rápidas
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Venta Total", f"${df_servicios['monto'].sum():,.2f}")
            with c2:
                st.metric("Comisiones por Cobrar (10%)", f"${df_servicios['comision'].sum():,.2f}", delta_color="normal")
            with c3:
                st.metric("Total Servicios", len(df_servicios))
            
            st.write("### Desglose por Socio")
            # Mostramos la tabla completa con el nombre del socio y la comisión
            st.dataframe(df_servicios[['fecha', 'cliente', 'socio', 'monto', 'comision']], use_container_width=True)
            
            # Botón para descargar reporte
            csv = df_servicios.to_csv(index=False).encode('utf-8')
            st.download_button("Descargar Reporte de Comisiones", csv, "reporte_rs.csv", "text/csv")
        else:
            st.warning("Aún no hay datos financieros para mostrar.")
    elif password != "":
        st.sidebar.error("Clave incorrecta")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("© 2026 OKGRUAS RS - Monterrey, N.L. | Sistema de gestión de flota y socios.")
