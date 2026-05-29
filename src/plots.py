import plotly.express as px
import pandas as pd
import streamlit as st

def plot_temporal(df: pd.DataFrame):
    if df.empty or 'Periodo' not in df.columns:
        return st.warning("⚠️ No hay datos válidos de periodo.")
    counts = df.groupby('Periodo', observed=True).size().reset_index(name='Registros')
    if counts.empty: return st.info("Sin registros en el rango seleccionado.")
    fig = px.line(counts, x='Periodo', y='Registros', markers=True, title="📈 Tendencia de Registros por Periodo")
    fig.update_layout(xaxis_tickangle=-45, title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def plot_top_species(df: pd.DataFrame, n=10):
    if df.empty: return st.warning("Sin datos para top especies.")
    counts = df['Nombre científico'].value_counts().reset_index()
    counts.columns = ['Especie', 'Registros']
    fig = px.bar(counts.head(n), x='Especie', y='Registros', title=f"🦜 Top {n} Especies", color='Registros')
    fig.update_layout(xaxis_tickangle=-45, title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def plot_class_dist(df: pd.DataFrame):
    if df.empty: return st.warning("Sin datos para distribución por Clase.")
    counts = df['Clase'].value_counts().reset_index()
    counts.columns = ['Clase', 'Registros']
    fig = px.pie(counts, values='Registros', names='Clase', title="🦎 Distribución por Clase", hole=0.4)
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def plot_spatial(df: pd.DataFrame):
    valid = df[['X-UTM', 'Y-UTM', 'Nombre científico', 'Clase', 'UM_id']].dropna()
    if valid.empty: return st.warning("Sin coordenadas válidas.")
    fig = px.scatter(valid, x='X-UTM', y='Y-UTM', color='Clase', hover_data=['Nombre científico', 'UM_id'], title="🗺️ Distribución Espacial (UTM)")
    st.caption("⚠️ Coordenadas UTM relativas.")
    st.plotly_chart(fig, use_container_width=True)

def plot_hierarchical_distribution(df: pd.DataFrame):
    st.subheader("🌳 Distribución: Ecozona → Departamento → Familia")
    if df.empty: return st.warning("Sin datos para visualización jerárquica.")
    
    metric = st.radio("Métrica de concentración:", ["Registros (conteo)", "Especies Únicas"], horizontal=True, key="hier_metric")
    st.caption("💡 Haz clic en cualquier segmento para profundizar. El número central indica la cantidad exacta.")
    
    if metric == "Registros (conteo)":
        df_plot = df.copy()
        df_plot['Valor'] = 1
    else:
        df_plot = df.groupby(['Ecozona', 'Departamento', 'Familia'])['Nombre científico'].nunique().reset_index(name='Valor')
        
    fig = px.treemap(
        df_plot, path=['Ecozona', 'Departamento', 'Familia'], values='Valor',
        title=f"Concentración por {metric}", color='Ecozona',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(texttemplate='%{label}<br>%{value:.0f}', textposition='middle center', textfont=dict(size=14, color='white'))
    fig.update_layout(margin=dict(t=40, l=20, r=20, b=20), title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
