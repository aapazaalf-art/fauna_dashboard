import streamlit as st
import pandas as pd
from src.data_loader import load_raw_data
from src.preprocessing import preprocess_fauna
from src.filters import setup_independent_filters
from src.metrics import compute_kpis
from src import plots

# Configuración de página
st.set_page_config(page_title="Dashboard Fauna Silvestre", layout="wide", page_icon="🌿")
st.title("🌿 Explorador de Registros de Fauna Silvestre")
st.caption("Inventario Nacional Forestal | Filtros independientes y análisis de composición")

# 1. Carga y Preprocesamiento
DATA_PATH = "data/fauna_data.xlsx"
raw_df = load_raw_data(DATA_PATH)
df_full = preprocess_fauna(raw_df)

if df_full.empty:
    st.error("❌ No se pudo cargar o procesar la base de datos. Verifica la ruta y el formato del Excel.")
    st.stop()

# 2. Filtros independientes
st.divider()
df_filtered = setup_independent_filters(df_full)

if df_filtered.empty:
    st.warning("⚠️ No hay registros para la combinación de filtros seleccionada. Ajuste los criterios.")
    st.stop()

# 3. Estado y KPIs
st.info(f"📊 Mostrando **{len(df_filtered):,}** registros tras aplicar intersección de filtros.")
kpis = compute_kpis(df_filtered)
cols_kpi = st.columns(4)
metrics_map = {
    "Total Registros": "📄",
    "Especies Únicas": "🔬",
    "Familias Únicas": "🌿",
    "Registros con Foto": "📸"
}
for col, (k, v) in zip(cols_kpi, kpis.items()):
    with col:
        st.metric(label=f"{metrics_map[k]} {k}", value=f"{v:,}")

# 4. Visualizaciones Interactivas
st.subheader("📊 Visualizaciones Interactivas")
try:
    tab1, tab2, tab3, tab4 = st.tabs(["Temporal", "Taxonómica", "Espacial", "Composición por Ubicación"])
    with tab1: plots.plot_temporal(df_filtered)
    with tab2:
        c1, c2 = st.columns(2)
        with c1: plots.plot_class_dist(df_filtered)
        with c2: plots.plot_top_species(df_filtered, n=10)
    with tab3: plots.plot_spatial(df_filtered)
    with tab4: plots.plot_hierarchical_distribution(df_filtered)
except Exception as e:
    st.error(f"❌ Error al renderizar gráficos: {str(e)}")
    st.caption("Revisa los logs de Streamlit Cloud para detalles técnicos.")

# 5. Tabla de Detalle y Exportación Masiva
st.subheader("📋 Tabla de Detalle y Exportación")

with st.expander("🔧 Configuración de Columnas (opcional)", expanded=False):
    st.info("ℹ️ Por defecto se muestran **todas las columnas**. Puedes desmarcar las que no necesites.")
    all_cols = [c for c in [
        'UM_id', 'Ecozona', 'Departamento', 'Periodo', 'Nombre científico', 'Nombre común', 
        'Familia', 'Clase', 'Tipo de registro', 'CUA', 'Zona UTM', 
        'Altitud (m)', 'Distancia (m)', 'Número de foto'
    ] if c in df_filtered.columns]
    
    # Por defecto, todas las columnas están seleccionadas
    sel_cols = st.multiselect("Columnas a visualizar y descargar:", options=all_cols, default=all_cols)

# Preparar dataframe para tabla y exportación (siempre usa TODAS las filas filtradas)
export_df = df_filtered[sel_cols] if sel_cols else df_filtered

st.markdown(f"📥 **{len(export_df):,} registros completos** coinciden con los filtros activos.")
st.dataframe(export_df, use_container_width=True, hide_index=True)

# Botón de descarga masiva
csv_data = export_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label=f"⬇️ Descargar TODOS los registros filtrados ({len(export_df):,} filas)",
    data=csv_data,
    file_name="fauna_export_completa.csv",
    mime="text/csv",
    use_container_width=True
)
st.caption("✅ La descarga incluye únicamente las filas que cumplen con los filtros del sidebar, con la información completa de cada registro.")
