import streamlit as st
import pandas as pd
from src.data_loader import load_raw_data
from src.preprocessing import preprocess_fauna
from src.filters import setup_independent_filters
from src.metrics import compute_kpis
import src.plots as plots

# 🎨 CSS DE ACCESIBILIDAD VISUAL
st.markdown("""
<style>
    .stMarkdown, .stDataFrame, .stMetric, .stSelectbox label, .stMultiSelect label, 
    .stSlider label, .stCheckbox label, .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.15rem !important; color: #000000 !important; font-family: Arial, sans-serif;
    }
    .st-emotion-cache-1y4p8pa { border: 2px solid #2C3E50 !important; border-radius: 10px; padding: 12px; margin: 8px 0; }
    .stDataFrame thead th, .stDataFrame tbody td { font-size: 1rem !important; color: #000000 !important; }
    .stDownloadButton > button { font-size: 1.1rem !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Dashboard Fauna Silvestre", layout="wide", page_icon="🌿")
st.title("🌿 Explorador de Registros de Fauna Silvestre")
st.caption("Inventario Nacional Forestal | Accesibilidad mejorada y métricas biológicas avanzadas")

# 1️⃣ Carga y Preprocesamiento
DATA_PATH = "data/fauna_data.xlsx"
raw_df = load_raw_data(DATA_PATH)
df_full = preprocess_fauna(raw_df)

if df_full.empty:
    st.error("❌ No se pudo cargar o procesar la base de datos.")
    st.stop()

# 2️⃣ Filtros Independientes
st.divider()
df_filtered = setup_independent_filters(df_full)

if df_filtered.empty:
    st.warning("⚠️ No hay registros para la combinación de filtros seleccionada.")
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
tabs = st.tabs(["📅 Temporal", "🦎 Taxonómica", "🗺️ Espacial", "🌳 Composición", "📊 CUA Visual", "🔬 Biológicas Avanzadas"])

with tabs[0]:
    with st.container(border=True):
        fig = plots.plot_temporal(df_filtered)
        if fig: st.plotly_chart(fig, use_container_width=True, key="plot_temporal_main")
        else: st.info("⏳ Sin datos temporales disponibles.")

with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            fig = plots.plot_class_dist(df_filtered)
            if fig: st.plotly_chart(fig, use_container_width=True, key="plot_class_dist")
            else: st.info("⏳ Sin datos de Clase.")
    with c2:
        with st.container(border=True):
            fig = plots.plot_top_species(df_filtered, n=10)
            if fig: st.plotly_chart(fig, use_container_width=True, key="plot_top_species")
            else: st.info("⏳ Sin datos de Especies.")

with tabs[2]:
    with st.container(border=True):
        fig = plots.plot_spatial_richness(df_filtered)
        if fig: st.plotly_chart(fig, use_container_width=True, key="plot_spatial_richness")
        else: st.info("⏳ Sin datos de Ecozona.")

with tabs[3]:
    with st.container(border=True):
        fig = plots.plot_hierarchical_distribution(df_filtered, key_suffix="_comp_tab")
        if fig: st.plotly_chart(fig, use_container_width=True, key="plot_hierarchical")
        else: st.info("⏳ Sin datos para jerarquía.")

with tabs[4]:  # ✅ NUEVA PESTAÑA CUA VISUAL
    with st.container(border=True):
        fig = plots.plot_cua_species_visual(df_filtered)
        if fig: st.plotly_chart(fig, use_container_width=True, key="plot_cua_visual")
        else: st.info("⏳ Sin datos de CUA.")

with tabs[5]:
    st.markdown("### 🔬 Métricas Biológicas Avanzadas")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            fig = plots.plot_family_richness_by_dept(df_filtered)
            if fig: st.plotly_chart(fig, use_container_width=True, key="plot_family_dept")
            else: st.info("⏳ Sin datos por Depto.")
    with c2:
        with st.container(border=True):
            fig = plots.plot_cooccurrence_matrix(df_filtered)
            if fig: st.plotly_chart(fig, use_container_width=True, key="plot_cooccurrence")
            else: st.info("⏳ Sin datos de co-ocurrencia.")
    with c3:
        with st.container(border=True):
            fig = plots.plot_cua_taxonomic_impact(df_filtered, key_suffix="_adv_tab") if hasattr(plots, 'plot_cua_taxonomic_impact') else None
            if fig: st.plotly_chart(fig, use_container_width=True, key="plot_cua_advanced")
            else: st.info("⏳ Sin datos CUA/Clase.")

# 5️⃣ Tabla de Detalle y Exportación
st.divider()
st.subheader("📋 Tabla de Detalle y Exportación Completa")
st.info(f"📥 **{len(df_filtered):,} registros** coinciden con los filtros activos del sidebar.")
st.dataframe(df_filtered, use_container_width=True, hide_index=True)

csv_data = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Descargar TABLA COMPLETA FILTRADA (CSV compatible con Excel)",
    data=csv_data,
    file_name=f"fauna_export_{len(df_filtered)}_registros.csv",
    mime="text/csv",
    use_container_width=True,
    key="btn_download_csv"
)
st.caption("✅ Se descargan TODAS las filas y columnas que cumplen con los filtros seleccionados.")
