import streamlit as st
import pandas as pd
from src.data_loader import load_raw_data
from src.preprocessing import preprocess_fauna
from src.filters import setup_independent_filters
from src.metrics import compute_kpis
import src.plots as plots

# CSS Accesibilidad
st.markdown("""
<style>
    .stMarkdown, .stDataFrame, .stMetric, label { font-size: 1.1rem !important; color: #000 !important; }
    .st-emotion-cache-1y4p8pa { border: 2px solid #2C3E50 !important; border-radius: 8px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Dashboard Fauna", layout="wide", page_icon="🌿")
st.title("🌿 Explorador de Fauna Silvestre")

# Carga
DATA_PATH = "data/fauna_data.xlsx"
raw_df = load_raw_data(DATA_PATH)
df_full = preprocess_fauna(raw_df)

if df_full.empty:
    st.error("❌ Error al cargar datos.")
    st.stop()

# Filtros
st.divider()
df_filtered = setup_independent_filters(df_full)

if df_filtered.empty:
    st.warning("⚠️ Sin datos para los filtros seleccionados.")
    st.stop()

# KPIs
st.info(f"📊 **{len(df_filtered):,}** registros activos")
kpis = compute_kpis(df_filtered)
cols = st.columns(4)
for col, (k,v) in zip(cols, kpis.items()):
    col.metric(k, f"{v:,}")

# Visualizaciones
st.subheader("📊 Gráficos")
tabs = st.tabs(["📅 Temporal","🦎 Taxonómica","🗺️ Espacial","🌳 Composición","📊 CUA","🔬 Avanzadas"])

with tabs[0]:
    with st.container(border=True):
        fig = plots.plot_temporal(df_filtered)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sin datos")

with tabs[1]:
    c1,c2 = st.columns(2)
    with c1, st.container(border=True):
        fig = plots.plot_class_dist(df_filtered)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sin datos")
    with c2, st.container(border=True):
        fig = plots.plot_top_species(df_filtered)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sin datos")

with tabs[2]:
    with st.container(border=True):
        fig = plots.plot_spatial_richness(df_filtered)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sin datos")

with tabs[3]:
    with st.container(border=True):
        fig = plots.plot_hierarchical_distribution(df_filtered, key_suffix="_main")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sin datos")

# ✅ PESTAÑA CUA CON LAS DOS FUNCIONES NUEVAS
with tabs[4]:
    st.markdown("### 📊 Clasificación de Uso Actual (CUA)")
    
    # Gráfico 1: CUA vs Cantidad de Especies
    with st.container(border=True):
        fig1 = plots.plot_cua_species_count(df_filtered)
        if fig1:
            st.plotly_chart(fig1, use_container_width=True, key="cua_count")
        else:
            st.info("⏳ Sin datos de CUA")
    
    # Gráfico 2: Composición por Clase dentro de cada CUA
    with st.container(border=True):
        fig2 = plots.plot_cua_by_class_composition(df_filtered)
        if fig2:
            st.plotly_chart(fig2, use_container_width=True, key="cua_class")
        else:
            st.info("⏳ Sin datos de composición")

with tabs[5]:
    c1,c2,c3 = st.columns(3)
    with c1, st.container(border=True):
        fig = plots.plot_family_richness_by_dept(df_filtered)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sin datos")
    with c2, st.container(border=True):
        fig = plots.plot_cooccurrence_matrix(df_filtered)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sin datos")
    with c3, st.container(border=True):
        st.info("Espacio adicional")

# Tabla y descarga
st.divider()
st.subheader("📋 Tabla y Exportación")
st.dataframe(df_filtered, use_container_width=True, hide_index=True)
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Descargar CSV", csv, "fauna_export.csv", "text/csv", key="btn_csv")
