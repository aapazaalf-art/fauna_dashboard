import plotly.express as px
import pandas as pd

def _apply_style(fig):
    """Aplica estilos básicos de accesibilidad."""
    try:
        fig.update_layout(
            font=dict(size=12, color="#000000"),
            title_font=dict(size=16, color="#000000"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
    except Exception:
        pass
    return fig

def plot_temporal(df):
    if df is None or df.empty or 'Periodo' not in df.columns:
        return None
    counts = df.groupby('Periodo', observed=True).size().reset_index(name='Registros')
    if counts.empty:
        return None
    fig = px.line(counts, x='Periodo', y='Registros', markers=True, title="📈 Tendencia Temporal")
    return _apply_style(fig)

def plot_top_species(df, n=10):
    if df is None or df.empty:
        return None
    counts = df['Nombre científico'].value_counts().head(n).reset_index()
    counts.columns = ['Especie', 'Registros']
    fig = px.bar(counts, x='Especie', y='Registros', title=f"🦜 Top {n} Especies")
    return _apply_style(fig)

def plot_class_dist(df):
    if df is None or df.empty:
        return None
    counts = df['Clase'].value_counts().reset_index()
    counts.columns = ['Clase', 'Registros']
    if len(counts) == 0:
        return None
    fig = px.pie(counts, values='Registros', names='Clase', title="🦎 Por Clase")
    return fig

def plot_spatial_richness(df):
    if df is None or df.empty or 'Ecozona' not in df.columns:
        return None
    richness = df.groupby('Ecozona')['Nombre científico'].nunique().reset_index(name='Riqueza')
    fig = px.bar(richness, x='Ecozona', y='Riqueza', title="🗺️ Riqueza por Ecozona")
    return _apply_style(fig)

def plot_hierarchical_distribution(df, key_suffix=""):
    if df is None or df.empty:
        return None
    import streamlit as st
    st.subheader("🌳 Composición")
    metric = st.radio("Métrica:", ["Registros", "Especies"], horizontal=True, key=f"hier_{key_suffix}")
    if metric == "Registros":
        df_plot = df.copy()
        df_plot['Valor'] = 1
    else:
        df_plot = df.groupby(['Ecozona','Departamento','Familia'])['Nombre científico'].nunique().reset_index(name='Valor')
    fig = px.treemap(df_plot, path=['Ecozona','Departamento','Familia'], values='Valor', title="Concentración")
    return fig

def plot_family_richness_by_dept(df):
    if df is None or df.empty:
        return None
    agg = df.groupby(['Departamento','Familia'])['Nombre científico'].nunique().reset_index(name='Riqueza')
    top = agg.groupby('Familia')['Riqueza'].sum().nlargest(10).index
    fig = px.bar(agg[agg['Familia'].isin(top)], x='Riqueza', y='Familia', color='Departamento', title="🌿 Familias por Departamento")
    return _apply_style(fig)

def plot_cooccurrence_matrix(df):
    if df is None or df.empty:
        return None
    top_sp = df['Nombre científico'].value_counts().head(15).index
    if len(top_sp) == 0:
        return None
    df_sub = df[df['Nombre científico'].isin(top_sp)]
    if df_sub.empty:
        return None
    pivot = pd.crosstab(df_sub['UM_id'], df_sub['Nombre científico'])
    pivot = (pivot > 0).astype(int)
    fig = px.imshow(pivot, color_continuous_scale=['#eee','#D32F2F'], title="🔗 Co-ocurrencia")
    return _apply_style(fig)

# ✅ FUNCIÓN NUEVA: CUA vs Cantidad de Especies (Barras simples)
def plot_cua_species_count(df):
    """CUA vs Cantidad de Especies Registradas - Gráfico de barras simples."""
    if df is None or df.empty or 'CUA' not in df.columns:
        return None
    species_per_cua = df.groupby('CUA')['Nombre científico'].nunique().reset_index(name='Especies')
    species_per_cua = species_per_cua.sort_values('Especies', ascending=False)
    fig = px.bar(species_per_cua, x='CUA', y='Especies', title="📊 Especies por CUA", color='Especies')
    return _apply_style(fig)

# ✅ FUNCIÓN NUEVA: Composición de cada CUA por Clase (Barras apiladas %)
def plot_cua_by_class_composition(df):
    """Composición por Clase dentro de cada CUA - Barras apiladas normalizadas."""
    if df is None or df.empty or 'CUA' not in df.columns:
        return None
    agg = df.groupby(['CUA', 'Clase']).size().reset_index(name='Registros')
    total = agg.groupby('CUA')['Registros'].transform('sum')
    agg['Pct'] = (agg['Registros'] / total * 100).round(1)
    fig = px.bar(agg, x='CUA', y='Pct', color='Clase', title="🌍 Composición por Clase en cada CUA (%)", barmode='stack')
    return _apply_style(fig)
