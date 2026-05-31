import streamlit as st
import pandas as pd
from src.data_loader import load_raw_data
from src.preprocessing import preprocess_fauna
from src.filters import setup_independent_filters
from src.metrics import compute_kpis
import src.plots as plots

# 🎨 CSS DE ACCESIBILIDAD VISUAL (Texto oscuro, alto contraste)
st.markdown("""
<style>
    /* Tipografía global oscura y legible */
    .stMarkdown, .stDataFrame, .stMetric, .stSelectbox label, .stMultiSelect label, 
    .stSlider label, .stCheckbox label, .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.1rem !important;
        color: #000000 !important;
        font-family: Arial, sans-serif;
        font-weight: 500;
    }
    /* Títulos de sección */
    h1, h2, h3, h4 { color: #000000 !important; }
    /* Bordes definidos para contenedores de gráficos */
    .st-emotion-cache-1y4p8pa { 
        border: 2px solid #2C3E50 !important; 
        border-radius: 8px; 
        padding: 12px; 
        margin: 8px 0; 
        background-color: #FAFAFA;
    }
    /* Tablas legibles */
    .stDataFrame thead th, .stDataFrame tbody td { 
        font-size: 1rem !important; 
        color: #000000 !important; 
    }
    /* Botones destacados */
    .stDownloadButton > button { 
        font-size: 1.1rem !important; 
        font-weight: bold; 
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Dashboard Fauna Silvestre", layout="wide", page_icon="🌿")
st.title("🌿 Explorador de Registros de Fauna Silvestre")
st.caption("Inventario Nacional Forestal | Visualización mejorada y análisis de biodiversidad")

# 1️⃣ Carga y Preprocesamiento
DATA_PATH = "data/fauna_data.xlsx"
raw_df = load_raw_data(DATA_PATH)
df_full = preprocess_fauna(raw_df)

if df_full.empty:
    st.error("❌ No se pudo cargar la base de datos.")
    st.stop()

# 2️⃣ Filtros Independientes
st.divider()
df_filtered = setup_independent_filters(df_full)

if df_filtered.empty:
    st.warning("⚠️ Sin datos para los filtros seleccionados.")
    st.stop()

# 3️⃣ KPIs Dinámicos
st.info(f"📊 **{len(df_filtered):,}** registros activos")
kpis = compute_kpis(df_filtered)
cols = st.columns(4)
for col, (k,v) in zip(cols, kpis.items()):
    col.metric(k, f"{v:,}")

# 4️⃣ Visualizaciones Interactivas
st.subheader("📊 Gráficos Interactivos")
tabs = st.tabs(["📅 Temporal", "🦎 Taxonómica", "🗺️ Espacial", "🌳 Composición", "📊 CUA", "🔬 Avanzadas"])

# Pestaña 1: Temporal
with tabs[0]:
    with st.container(border=True):
        fig = plots.plot_temporal(df_filtered)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⏳ Sin datos temporales")

# Pestaña 2: Taxonómica (Top 10 con colores distintos por barra)
with tabs[1]:
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        fig = plots.plot_class_dist(df_filtered)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⏳ Sin datos de Clase")
    with c2, st.container(border=True):
        fig = plots.plot_top_species(df_filtered, n=10)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⏳ Sin datos de Especies")

# Pestaña 3: Espacial (Riqueza con colores por Ecozona)
with tabs[2]:
    with st.container(border=True):
        fig = plots.plot_spatial_richness(df_filtered)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⏳ Sin datos de Ecozona")

# Pestaña 4: Composición (✅ REEMPLAZADO: Treemap → Barras agrupadas)
with tabs[3]:
    with st.container(border=True):
        fig = plots.plot_composition_bars(df_filtered, key_suffix="_main")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⏳ Sin datos de composición")

# Pestaña 5: CUA (Colores distintos por categoría)
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

# Pestaña 6: Métricas Avanzadas (✅ ELIMINADO: "Espacio adicional")
with tabs[5]:
    st.markdown("### 🔬 Métricas Biológicas Avanzadas")
    c1, c2 = st.columns(2)  # ✅ Solo 2 columnas, eliminada la tercera innecesaria
    with c1, st.container(border=True):
        fig = plots.plot_family_richness_by_dept(df_filtered)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⏳ Sin datos por Departamento")
    with c2, st.container(border=True):
        fig = plots.plot_cooccurrence_matrix(df_filtered)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⏳ Sin datos de co-ocurrencia")
    # ✅ "Espacio adicional" eliminado según solicitud

# 5️⃣ Tabla y Exportación
st.divider()
st.subheader("📋 Tabla de Detalle y Exportación")
st.dataframe(df_filtered, use_container_width=True, hide_index=True)

csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Descargar CSV con registros filtrados",
    data=csv,
    file_name=f"fauna_export_{len(df_filtered)}_registros.csv",
    mime="text/csv",
    use_container_width=True,
    key="btn_download"
)
st.caption("✅ Se exportan TODAS las filas que cumplen con los filtros activos.")
