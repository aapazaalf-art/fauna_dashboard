import streamlit as st
import pandas as pd
from src.data_loader import load_raw_data
from src.preprocessing import preprocess_fauna
from src.filters import setup_sidebar
from src.metrics import compute_kpis
from src import plots

# Configuración inicial
st.set_page_config(page_title="Dashboard Fauna Silvestre", layout="wide", page_icon="🌿")

st.title("🌿 Explorador de Registros de Fauna Silvestre")
st.caption("Inventario Nacional Forestal | Análisis por Unidad Muestral y Atributos Biológicos/Espaciales")

# 1. Carga y Preprocesamiento
DATA_PATH = "data/fauna_data.xlsx"
raw_df = load_raw_data(DATA_PATH)
df = preprocess_fauna(raw_df)

if df.empty:
    st.error("No se pudo cargar o procesar la base de datos.")
    st.stop()

# 2. Filtros
st.divider()
df_filtered = setup_sidebar(df)

# Verificación post-filtro
if df_filtered.empty:
    st.warning("⚠️ No hay datos para la combinación de filtros seleccionada. Ajuste los criterios.")
    st.stop()

# 3. Estado y KPIs
st.info(f"📊 Mostrando **{len(df_filtered):,}** registros filtrados.")
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

# 4. Visualizaciones
st.subheader("📊 Visualizaciones Interactivas")
tab1, tab2, tab3 = st.tabs(["Temporal", "Taxonómica", "Espacial"])
with tab1: plots.plot_temporal(df_filtered)
with tab2:
    c1, c2 = st.columns(2)
    with c1: plots.plot_class_dist(df_filtered)
    with c2: plots.plot_top_species(df_filtered, n=10)
with tab3: plots.plot_spatial(df_filtered)

# 5. Tabla de Detalle y Descarga
st.subheader("📋 Tabla de Detalle de Registros")
cols_table = [
    'UM_id', 'Departamento', 'Periodo', 'Nombre científico', 'Nombre común', 
    'Familia', 'Clase', 'Tipo de registro', 'CUA', 'Zona UTM', 
    'Altitud (m)', 'Distancia (m)', 'Número de foto'
]
display_cols = [c for c in cols_table if c in df_filtered.columns]
st.dataframe(df_filtered[display_cols], use_container_width=True, hide_index=True)

# Descarga CSV
csv = df_filtered[display_cols].to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Descargar resultados filtrados (CSV)",
    data=csv,
    file_name="fauna_filtrada.csv",
    mime="text/csv",
)