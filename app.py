import streamlit as st
import pandas as pd
from src.data_loader import load_raw_data
from src.preprocessing import preprocess_fauna
from src.filters import setup_independent_filters
from src.metrics import compute_kpis
from src import plots

st.set_page_config(page_title="Dashboard Fauna Silvestre", layout="wide", page_icon="🌿")
st.title("🌿 Explorador de Registros de Fauna Silvestre")
st.caption("Inventario Nacional Forestal | Filtros independientes y análisis de composición")

# 1. Carga y Preprocesamiento
DATA_PATH = "data/fauna_data.xlsx"
raw_df = load_raw_data(DATA_PATH)
df_full = preprocess_fauna(raw_df)

if df_full.empty:
    st.error("No se pudo cargar o procesar la base de datos.")
    st.stop()

# 2. Filtros
st.divider()
df_filtered = setup_independent_filters(df_full)

if df_filtered.empty:
    st.warning("⚠️ No hay registros para la combinación de filtros seleccionada.")
    st.stop()

# 3. KPIs
st.info(f"📊 Mostrando **{len(df_filtered):,}** registros tras aplicar intersección de filtros.")
kpis = compute_kpis(df_filtered)
cols_kpi = st.columns(4)
metrics_map = {"Total Registros": "📄", "Especies Únicas": "🔬", "Familias Únicas": "🌿", "Registros con Foto": "📸"}
for col, (k, v) in zip(cols_kpi, kpis.items()):
    with col: st.metric(label=f"{metrics_map[k]} {k}", value=f"{v:,}")

# 4. Visualizaciones (con manejo seguro de errores)
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
    st.code("Verifica en logs de Streamlit Cloud el traceback completo para depurar columnas faltantes.")

# 5. Tabla y Descarga Selectiva
st.subheader("📋 Tabla de Detalle y Exportación")
with st.expander("🔧 Configuración de Descarga Selectiva", expanded=False):
    st.markdown("- La descarga incluye **todas las filas filtradas**, no solo las visibles en pantalla.")
    all_cols = [c for c in ['UM_id', 'Ecozona', 'Departamento', 'Periodo', 'Nombre científico', 'Nombre común', 
                            'Familia', 'Clase', 'Tipo de registro', 'CUA', 'Zona UTM', 'Altitud (m)', 'Distancia (m)', 'Número de foto'] if c in df_filtered.columns]
    sel_cols = st.multiselect("Columnas a exportar:", options=all_cols, default=all_cols[:8])
    if sel_cols:
        export_df = df_filtered[sel_cols]
        st.download_button(
            label=f"⬇️ Descargar {len(export_df):,} registros (CSV)",
            data=export_df.to_csv(index=False).encode('utf-8'),
            file_name="fauna_export.csv", mime="text/csv", use_container_width=True
        )
    else:
        st.warning("Selecciona al menos una columna para descargar.")

st.dataframe(df_filtered[sel_cols if sel_cols else all_cols], use_container_width=True, hide_index=True)
