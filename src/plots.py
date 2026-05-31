import plotly.express as px
import pandas as pd
import streamlit as st

def apply_accessibility(fig, title_size=18, font_size=13):
    """Aplica estilos de alto contraste y tipografía legible."""
    fig.update_layout(
        title_font=dict(size=title_size, family="Arial, sans-serif", color="#000000"),
        font=dict(size=font_size, family="Arial, sans-serif", color="#000000"),
        legend=dict(font=dict(size=font_size, color="#000000"), bgcolor="rgba(255,255,255,0.95)", bordercolor="#000000", borderwidth=1),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=60, r=40, t=70, b=60)
    )
    try:
        fig.update_xaxes(tickfont=dict(size=12, color="#000000"), title_font=dict(size=14, color="#000000"), gridcolor="#D3D3D3")
        fig.update_yaxes(tickfont=dict(size=12, color="#000000"), title_font=dict(size=14, color="#000000"), gridcolor="#D3D3D3")
    except Exception:
        pass
    try:
        fig.update_coloraxes(tickfont=dict(color="#000000"), titlefont=dict(color="#000000"))
    except Exception:
        pass
    return fig

def plot_temporal(df: pd.DataFrame):
    """Gráfico de tendencia temporal."""
    if df.empty or 'Periodo' not in df.columns:
        return None
    counts = df.groupby('Periodo', observed=True).size().reset_index(name='Registros')
    if counts.empty:
        return None
    fig = px.line(counts, x='Periodo', y='Registros', markers=True,
                  title="📈 Tendencia de Registros por Periodo",
                  color_discrete_sequence=['#1A73E8'])
    return apply_accessibility(fig)

def plot_top_species(df: pd.DataFrame, n=10):
    """Top N especies más frecuentes."""
    if df.empty:
        return None
    counts = df['Nombre científico'].value_counts().head(n).reset_index()
    counts.columns = ['Especie', 'Registros']
    fig = px.bar(counts, x='Especie', y='Registros', 
                 title=f"🦜 Top {n} Especies más Frecuentes",
                 color='Registros', color_continuous_scale='Viridis')
    fig.update_layout(xaxis_tickangle=-45)
    return apply_accessibility(fig)

def plot_class_dist(df: pd.DataFrame):
    """Distribución por Clase Taxonómica."""
    if df.empty:
        return None
    counts = df['Clase'].value_counts().reset_index()
    counts.columns = ['Clase', 'Registros']
    if len(counts) == 0:
        return None
    fig = px.pie(counts, values='Registros', names='Clase', 
                 title="🦎 Distribución por Clase Taxonómica", hole=0.4)
    fig.update_traces(textfont=dict(color="#000000", size=12), pull=[0.02]*len(counts))
    fig.update_layout(title_font=dict(color="#000000"), legend=dict(font=dict(color="#000000")))
    return fig

def plot_spatial_richness(df: pd.DataFrame):
    """Riqueza de especies por Ecozona."""
    if df.empty or 'Ecozona' not in df.columns:
        return None
    richness = df.groupby('Ecozona')['Nombre científico'].nunique().reset_index(name='Riqueza de Especies')
    richness = richness.sort_values('Riqueza de Especies', ascending=False)
    fig = px.bar(richness, x='Ecozona', y='Riqueza de Especies', 
                 title="🗺️ Riqueza de Especies por Ecozona",
                 color='Riqueza de Especies', color_continuous_scale='Tealgrn', text_auto=True)
    return apply_accessibility(fig)

def plot_hierarchical_distribution(df: pd.DataFrame, key_suffix: str = ""):
    """Treemap jerárquico: Ecozona → Departamento → Familia."""
    if df.empty:
        return None
    st.subheader("🌳 Composición: Ecozona → Departamento → Familia")
    metric = st.radio("Métrica:", ["Registros", "Especies Únicas"], 
                      horizontal=True, key=f"hier_metric{key_suffix}")
    if metric == "Registros":
        df_plot = df.copy()
        df_plot['Valor'] = 1
    else:
        df_plot = df.groupby(['Ecozona','Departamento','Familia'])['Nombre científico'].nunique().reset_index(name='Valor')
    fig = px.treemap(df_plot, path=['Ecozona','Departamento','Familia'], values='Valor', 
                     title=f"Concentración por {metric}", color='Ecozona',
                     color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_traces(texttemplate='%{label}<br>%{value:.0f}', textposition='middle center', 
                      textfont=dict(size=15, color='#111111'))
    fig.update_layout(margin=dict(t=40, l=20, r=20, b=20))
    return fig

def plot_family_richness_by_dept(df: pd.DataFrame):
    """Riqueza de Familias por Departamento."""
    if df.empty:
        return None
    agg = df.groupby(['Departamento','Familia'])['Nombre científico'].nunique().reset_index(name='Riqueza')
    top_families = agg.groupby('Familia')['Riqueza'].sum().nlargest(10).index
    fig = px.bar(agg[agg['Familia'].isin(top_families)], x='Riqueza', y='Familia', 
                 color='Departamento', title="🌿 Familias por Departamento (Top 10)",
                 color_discrete_sequence=px.colors.qualitative.Bold, barmode='stack')
    fig.update_layout(yaxis={'categoryorder': 'array', 'categoryarray': top_families[::-1]})
    return apply_accessibility(fig)

def plot_cooccurrence_matrix(df: pd.DataFrame):
    """Matriz de co-ocurrencia: Top especies × UM_id."""
    if df.empty:
        return None
    top_sp = df['Nombre científico'].value_counts().head(15).index
    if len(top_sp) == 0:
        return None
    df_sub = df[df['Nombre científico'].isin(top_sp)]
    if df_sub.empty:
        return None
    pivot = pd.crosstab(df_sub['UM_id'], df_sub['Nombre científico'])
    pivot = (pivot > 0).astype(int)
    fig = px.imshow(pivot, color_continuous_scale=['#F0F0F0', '#D32F2F'], 
                     title="🔗 Co-ocurrencia: Top 15 Especies × UM_id",
                     labels=dict(x="Especie", y="UM_id", color="Presencia"))
    fig.update_layout(xaxis_tickangle=-60, plot_bgcolor='white')
    return apply_accessibility(fig)

def plot_cua_species_count(df: pd.DataFrame):
    """CUA vs Cantidad de Especies Registradas (Barras simples)."""
    if df.empty or 'CUA' not in df.columns:
        return None
    # Conteo de especies únicas por CUA
    species_per_cua = df.groupby('CUA')['Nombre científico'].nunique().reset_index(name='Especies Únicas')
    species_per_cua = species_per_cua.sort_values('Especies Únicas', ascending=False)
    
    fig = px.bar(species_per_cua, x='CUA', y='Especies Únicas', 
                 title="📊 Especies Registradas por CUA",
                 color='Especies Únicas', color_continuous_scale='Blues', text_auto=True)
    fig.update_layout(xaxis_title="Categoría CUA", yaxis_title="Número de Especies Únicas", xaxis_tickangle=-30)
    return apply_accessibility(fig)

def plot_cua_by_class_composition(df: pd.DataFrame):
    """Composición de cada CUA por Clase de especies (barras apiladas normalizadas)."""
    if df.empty or 'CUA' not in df.columns:
        return None
    # Agregación: conteo de registros por CUA × Clase
    agg = df.groupby(['CUA', 'Clase']).size().reset_index(name='Registros')
    
    # Calcular porcentajes por CUA
    total_per_cua = agg.groupby('CUA')['Registros'].transform('sum')
    agg['Porcentaje'] = (agg['Registros'] / total_per_cua * 100).round(1)
    
    fig = px.bar(agg, x='CUA', y='Porcentaje', color='Clase',
                 title="🌍 Composición por Clase dentro de cada CUA (%)",
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 text_auto='.1f', barmode='stack')
    fig.update_layout(yaxis_title="Porcentaje de Registros (%)", yaxis_range=[0, 105], xaxis_tickangle=-30)
    return apply_accessibility(fig)
