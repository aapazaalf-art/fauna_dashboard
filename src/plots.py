import plotly.express as px
import pandas as pd
import streamlit as st

def _safe_fig(func):
    """Decorator interno para manejar gráficos vacíos de forma segura."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return None
    return wrapper

@_safe_fig
def plot_temporal(df):
    if df.empty or 'Periodo' not in df.columns: return None
    counts = df.groupby('Periodo', observed=True).size().reset_index(name='Registros')
    if counts.empty: return None
    return px.line(counts, x='Periodo', y='Registros', markers=True, title="📈 Tendencia Temporal")

@_safe_fig
def plot_top_species(df, n=10):
    if df.empty: return None
    counts = df['Nombre científico'].value_counts().head(n).reset_index()
    counts.columns = ['Especie', 'Registros']
    return px.bar(counts, x='Especie', y='Registros', title=f"🦜 Top {n} Especies")

@_safe_fig
def plot_class_dist(df):
    if df.empty: return None
    counts = df['Clase'].value_counts().reset_index()
    counts.columns = ['Clase', 'Registros']
    return px.pie(counts, values='Registros', names='Clase', title="🦎 Por Clase")

@_safe_fig
def plot_spatial_richness(df):
    if df.empty or 'Ecozona' not in df.columns: return None
    richness = df.groupby('Ecozona')['Nombre científico'].nunique().reset_index(name='Riqueza')
    return px.bar(richness, x='Ecozona', y='Riqueza', title="🗺️ Riqueza por Ecozona")

@_safe_fig
def plot_hierarchical_distribution(df, key_suffix=""):
    if df.empty: return None
    # Widget con key único para evitar duplicados
    metric = st.radio("Métrica:", ["Registros", "Especies Únicas"], horizontal=True, key=f"hier_{key_suffix}")
    if metric == "Registros":
        df_plot = df.copy(); df_plot['Valor'] = 1
    else:
        df_plot = df.groupby(['Ecozona','Departamento','Familia'])['Nombre científico'].nunique().reset_index(name='Valor')
    return px.treemap(df_plot, path=['Ecozona','Departamento','Familia'], values='Valor', title="🌳 Composición")

@_safe_fig
def plot_family_richness_by_dept(df):
    if df.empty: return None
    agg = df.groupby(['Departamento','Familia'])['Nombre científico'].nunique().reset_index(name='Riqueza')
    top = agg.groupby('Familia')['Riqueza'].sum().nlargest(10).index
    return px.bar(agg[agg['Familia'].isin(top)], x='Riqueza', y='Familia', color='Departamento', title="🌿 Familias por Departamento")

@_safe_fig
def plot_cooccurrence_matrix(df):
    if df.empty: return None
    top_sp = df['Nombre científico'].value_counts().head(15).index
    pivot = pd.crosstab(df[df['Nombre científico'].isin(top_sp)]['UM_id'], df['Nombre científico'])
    pivot = (pivot > 0).astype(int)
    return px.imshow(pivot, color_continuous_scale=['#eee','#D32F2F'], title="🔗 Co-ocurrencia")

@_safe_fig
def plot_cua_species_visual(df):
    """Treemap visual CUA → Especies destacadas"""
    if df.empty or 'CUA' not in df.columns: return None
    agg = df.groupby(['CUA','Nombre científico']).size().reset_index(name='Registros')
    top = agg.sort_values('Registros', ascending=False).groupby('CUA').head(3)
    return px.treemap(top, path=['CUA','Nombre científico'], values='Registros', title="📊 Especies por CUA")
