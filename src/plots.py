import plotly.express as px
import pandas as pd
import streamlit as st

def plot_temporal(df: pd.DataFrame):
    if df.empty or 'Periodo' not in df.columns:
        return st.warning("⚠️ No hay datos válidos de periodo.")
    counts = df.groupby('Periodo', observed=True).size().reset_index(name='Registros')
    if counts.empty: return st.info("Sin registros en el rango seleccionado.")
    fig = px.line(counts, x='Periodo', y='Registros', markers=True, title="📈 Tendencia de Registros por Periodo (Mes/Año)")
    fig.update_layout(xaxis_tickangle=-45, title_x=0.5, yaxis_title="Número de Registros")
    st.plotly_chart(fig, use_container_width=True)

def plot_top_species(df: pd.DataFrame, n=10):
    if df.empty: return st.warning("Sin datos para top especies.")
    counts = df['Nombre científico'].value_counts().reset_index()
    counts.columns = ['Especie', 'Registros']
    fig = px.bar(counts.head(n), x='Especie', y='Registros', title=f"🦜 Top {n} Especies más Frecuentes", 
                 color='Registros', color_continuous_scale='Viridis')
    fig.update_layout(xaxis_tickangle=-45, title_x=0.5, yaxis_title="Frecuencia de Avistamientos")
    st.plotly_chart(fig, use_container_width=True)

def plot_class_dist(df: pd.DataFrame):
    if df.empty: return st.warning("Sin datos para distribución por Clase.")
    counts = df['Clase'].value_counts().reset_index()
    counts.columns = ['Clase', 'Registros']
    fig = px.pie(counts, values='Registros', names='Clase', title="🦎 Distribución por Clase Taxonómica", hole=0.4)
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def plot_spatial_richness(df: pd.DataFrame):
    """X = Ecozonas, Y = Riqueza de Especies (Especies Únicas)"""
    if df.empty or 'Ecozona' not in df.columns:
        return st.warning("⚠️ No hay datos de Ecozona disponibles.")
    richness = df.groupby('Ecozona')['Nombre científico'].nunique().reset_index(name='Riqueza de Especies')
    richness = richness.sort_values('Riqueza de Especies', ascending=False)
    
    fig = px.bar(richness, x='Ecozona', y='Riqueza de Especies', 
                 title="🗺️ Riqueza de Especies por Ecozona",
                 color='Riqueza de Especies', color_continuous_scale='Tealgrn', text_auto=True)
    fig.update_layout(xaxis_title="Ecozona", yaxis_title="Cantidad de Especies Únicas (Riqueza)", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("📌 Representa la diversidad observada por ecozona. Para mapas georreferenciados se requiere datum específico.")

def plot_hierarchical_distribution(df: pd.DataFrame):
    st.subheader("🌳 Composición: Ecozona → Departamento → Familia")
    if df.empty: return st.warning("Sin datos para visualización jerárquica.")
    
    metric = st.radio("Métrica de concentración:", ["Registros (conteo)", "Especies Únicas"], horizontal=True, key="hier_metric")
    
    if metric == "Registros (conteo)":
        df_plot = df.copy()
        df_plot['Valor'] = 1
    else:
        df_plot = df.groupby(['Ecozona', 'Departamento', 'Familia'])['Nombre científico'].nunique().reset_index(name='Valor')
        
    fig = px.treemap(
        df_plot, path=['Ecozona', 'Departamento', 'Familia'], values='Valor',
        title=f"Concentración por {metric}", color='Ecozona',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_traces(
        texttemplate='%{label}<br>%{value:.0f}', 
        textposition='middle center',
        textfont=dict(size=15, color='#111111', family='Inter, Arial, sans-serif')
    )
    fig.update_layout(margin=dict(t=40, l=20, r=20, b=20), title_x=0.5, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

def plot_cua_species(df: pd.DataFrame):
    st.subheader("📊 CUA y Distribución de Especies")
    if df.empty or 'CUA' not in df.columns:
        return st.warning("Sin datos para CUA.")
    
    cua_agg = df.groupby('CUA')['Nombre científico'].nunique().reset_index(name='Especies Únicas')
    cua_agg = cua_agg.sort_values('Especies Únicas', ascending=False)
    
    fig = px.bar(cua_agg, x='CUA', y='Especies Únicas', title="Especies Registradas por Clasificación de Uso Actual (CUA)",
                 color='CUA', color_discrete_sequence=px.colors.qualitative.Alphabet, text_auto=True)
    fig.update_layout(xaxis_title="Categoría CUA", yaxis_title="Número de Especies Únicas", title_x=0.5, xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("📌 Muestra la riqueza taxonómica asociada a cada categoría de uso actual del suelo/vegetación.")
