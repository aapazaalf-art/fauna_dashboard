import streamlit as st
import pandas as pd
from src.data_loader import load_raw_data
from src.preprocessing import preprocess_fauna
from src.filters import setup_independent_filters
from src.metrics import compute_kpis
import src.plots as plots

# 🔧 Configuración de página
st.set_page_config(page_title="Dashboard Fauna Silvestre", layout="wide", page_icon="🌿")
st.title("🌿 Explorador de Registros de Fauna Silvestre")
st.caption("Inventario Nacional Forestal | Análisis multidimensional y exportación completa")

# 1️⃣ Carga y Preprocesamiento
DATA_PATH = "data/fauna_data.xlsx"
raw_df = load_raw_data(DATA_PATH)
df_full = preprocess_fauna(raw_df)

if df_full.empty:
    st.error("❌ No se pudo cargar o procesar la base de datos. Verifique la ruta del archivo.")
    st.stop()

# 2️⃣ Filtros Independientes
st.divider()
df_filtered = setup_independent_filters(df_full)

if df_filtered.empty:
    st.warning("⚠️ No hay registros para la combinación de filtros seleccionada. Ajuste los criterios en el sidebar.")
    st.stop()

# 3️⃣ KPIs Dinámicos
st.info(f"📊 Mostrando **{len(df_filtered):,}** registros tras aplicar intersección de filtros.")
kpis = compute_kpis(df_filtered)
cols_kpi = st.columns(4)
metrics_map = {"Total Registros": "📄", "Especies Únicas": "🔬", "Familias Únicas": "🌿", "Registros con Foto": "📸"}
for col, (k, v) in zip(cols_kpi, kpis.items()):
    with col: st.metric(label=f"{metrics_map[k]} {k}", value=f"{v:,}")

# 4️⃣ Visualizaciones Interactivas
st.subheader("📊 Visualizaciones Interactivas")
try:
    tabs = st.tabs(["📅 Temporal", "🦎 Taxonómica", "🗺️ Espacial (Riqueza)", "🌳 Composición", "📊 CUA"])
    with tabs[0]: plots.plot_temporal(df_filtered)
    with tabs[1]:
        c1, c2 = st.columns(2)
        with c1: plots.plot_class_dist(df_filtered)
        with c2: plots.plot_top_species(df_filtered, n=10)
    with tabs[2]: plots.plot_spatial_richness(df_filtered)
    with tabs[3]: plots.plot_hierarchical_distribution(df_filtered)
    with tabs[4]: plots.plot_cua_species(df_filtered)
except Exception as e:
    st.error(f"❌ Error al renderizar gráficos: {e}")
    st.caption("Revise los logs de Streamlit para depurar columnas faltantes.")

# 5️⃣ Tabla de Detalle y Exportación (CORREGIDO)
st.divider()
st.subheader("📋 Tabla de Detalle y Exportación Completa")
st.info(f"📥 **{len(df_filtered):,} registros** coinciden con los filtros activos del sidebar.")

# La tabla muestra SOLO lo filtrado. Sin paginación que afecte la descarga.
st.dataframe(df_filtered, use_container_width=True, hide_index=True)

# Botón de descarga DIRECTA del DataFrame filtrado completo
csv_data = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Descargar TABLA COMPLETA FILTRADA (CSV compatible con Excel)",
    data=csv_data,
    file_name=f"fauna_export_{len(df_filtered)}_registros.csv",
    mime="text/csv",
    use_container_width=True
)
st.caption("✅ Se descargan TODAS las filas y columnas que cumplen con los filtros seleccionados, sin recortes ni limitaciones visuales.")
