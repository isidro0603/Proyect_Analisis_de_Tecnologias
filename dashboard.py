import streamlit as st
import pandas as pd
import os
import glob

st.set_page_config(page_title="Sistema Anti-Sueño - Reportes", layout="wide")
st.title("📊 Panel de Control - Historial de Ejecuciones")

DATA_DIR = "data"

archivos_csv = glob.glob(os.path.join(DATA_DIR, "incidentes_*.csv"))

if archivos_csv:
    archivos_csv.sort(reverse=True)
    nombres_limpios = [os.path.basename(f) for f in archivos_csv]

    archivo_seleccionado_nombre = st.selectbox("📂 Selecciona la sesión de simulación/ejecución:", nombres_limpios)
    archivo_completo_path = os.path.join(DATA_DIR, archivo_seleccionado_nombre)

    df = pd.read_csv(archivo_completo_path)

    if len(df) > 0:
        col1, col2 = st.columns(2)
        col1.metric("🚨 Alertas en esta sesión", f"{len(df)} eventos")
        col2.metric("⏱️ Duración Promedio", f"{df['duracion_segundos'].mean():.2f} s")

        st.markdown("---")

        # Gráfica interactiva de la sesión
        st.subheader("📈 Comportamiento de Fatiga en el Tiempo")
        st.bar_chart(data=df, x="fecha_hora", y="duracion_segundos")

        # Tabla de datos de la sesión
        st.subheader("📋 Datos de esta ejecución")
        st.dataframe(df, use_container_width=True)
    else:
        st.info(
            "Esta sesión acaba de iniciar y aún no tiene alertas registradas. ¡Prueba cerrando los ojos frente a la cámara!")
else:
    st.warning(
        "⚠️ No se han encontrado archivos de datos. Inicia el servidor primero para generar el archivo de ejecución.")