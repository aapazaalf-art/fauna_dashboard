import plotly.express as px
import pandas as pd

# 🎨 PALETAS DE COLORES CATEGÓRICAS DE ALTO CONTRASTE
CAT_COLORS = px.colors.qualitative.Bold  # Colores vivos y distinguibles
SEQ_COLORS = px.colors.sequential.Tealgrn  # Para escalas continuas

def _apply_dark_style(fig, title_size=16, font_size=12):
    """Aplica tipografía oscura y alto contraste a cualquier gráfico Plotly."""
    fig.update_layout(
        title_font=dict(size=title_size, family="Arial, sans-serif", color="#000000"),
        font=dict(size=font_size, family="Arial, sans-serif", color="#000000"),
        legend=dict(font=dict(size=font_size, color="#000000"), bgcolor="rgba(255,255,255,0.95)", bordercolor="#000000", borderwidth=1),
        plot_bgcolor="rgba(250,250,250,1)",
        paper_bgcolor="rgba(255,255,255,1)",
        margin=dict(l=50, r=30, t=60, b=50)
    )
    try:
        fig.update_xaxes(tickfont=dict(size=11, color="#000000"), title_font=dict(size=13, color="#000000"), gridcolor="#CCCCCC")
        fig.update_yaxes(tickfont=dict(size=11, color="#000000"), title_font=dict(size=13, color="#000000"), gridcolor="#CCCCCC")
    except Exception:
        pass
    try:
        fig.update_coloraxes(tickfont=dict(color="#000000"), titlefont=dict(color="#000000"))
    except Exception:
        pass
    return fig

def plot_temporal(df):
    """Tendencia temporal con línea oscura."""
    if df is None or df.empty or 'Periodo' not in df.columns:
        return None
    counts = df.groupby('Periodo', observed=True).size().reset_index(name='Registros')
    if counts.empty:
        return None
    fig = px.line(counts, x='Periodo', y='Registros', markers=True, 
                  title="📈 Tendencia de Registros por Periodo",
                  line_shape='spline', color_discrete_sequence=['#1A5276'])
    return _apply_dark_style(fig)

def plot_top_species(df, n=10):
    """Top N especies con COLOR DIFERENTE POR BARRA (solicitud específica)."""
    if df is None or df.empty:
        return None
    counts = df['Nombre científico'].value_counts().head(n).reset_index()
    counts.columns = ['Especie', 'Registros']
    # ✅ Color categórico único por barra para máxima distinción visual
    fig = px.bar(counts, x='Especie', y='Registros', 
                 title=f"🦜 Top {n} Especies más Frecuentes",
                 color='Especie', color_discrete_sequence=CAT_COLORS)
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)
    return _apply_dark_style(fig)

def plot_class_dist(df):
    """Distribución por Clase con colores distintivos."""
    if df is None or df.empty:
        return None
    counts = df['Clase'].value_counts().reset_index()
    counts.columns = ['Clase', 'Registros']
    if len(counts) == 0:
        return None
    fig = px.pie(counts, values='Registros', names='Clase', 
                 title="🦎 Distribución por Clase Taxonómica", 
                 hole=0.4, color='Clase', color_discrete_sequence=CAT_COLORS)
    fig.update_traces(textfont=dict(color="#000000", size=11), pull=[0.02]*len(counts))
    fig.update_layout(title_font=dict(color="#000000"), legend=dict(font=dict(color="#000000")))
    return fig

def plot_spatial_richness(df):
    """Riqueza por Ecozona con barras de colores categóricos."""
    if df is None or df.empty or 'Ecozona' not in df.columns:
        return None
    richness = df.groupby('Ecozona')['Nombre científico'].nunique().reset_index(name='Riqueza')
    richness = richness.sort_values('Riqueza', ascending=False)
    # ✅ Color por categoría (Ecozona) en lugar de escala continua
    fig = px.bar(richness, x='Ecozona', y='Riqueza', 
                 title="🗺️ Riqueza de Especies por Ecozona",
                 color='Ecozona', color_discrete_sequence=CAT_COLORS, text_auto=True)
    fig.update_layout(showlegend=False)
    return _apply_dark_style(fig)

def plot_composition_bars(df, key_suffix=""):
    """✅ REEMPLAZA Treemap por BARRAS: Composición Ecozona→Departamento→Familia."""
    if df is None or df.empty:
        return None
    
    import streamlit as st
    st.subheader("🌳 Composición por Ubicación y Familia")
    
    # Agrupar: Familia × Ecozona, contando registros
    agg = df.groupby(['Familia', 'Ecozona']).size().reset_index(name='Registros')
    
    # Top 12 familias para legibilidad
    top_families = agg.groupby('Familia')['Registros'].sum().nlargest(12).index
    agg = agg[agg['Familia'].isin(top_families)]
    
    # ✅ Gráfico de barras agrupadas con colores por Ecozona
    fig = px.bar(agg, x='Familia', y='Registros', color='Ecozona',
                 title="📊 Registros por Familia y Ecozona (Top 12 Familias)",
                 color_discrete_sequence=CAT_COLORS,
                 barmode='group')
    
    fig.update_layout(xaxis_tickangle=-45, xaxis_title="Familia", yaxis_title="Número de Registros")
    return _apply_dark_style(fig)

def plot_family_richness_by_dept(df):
    """Riqueza de Familias por Departamento con colores por Departamento."""
    if df is None or df.empty:
        return None
    agg = df.groupby(['Departamento','Familia'])['Nombre científico'].nunique().reset_index(name='Riqueza')
    top = agg.groupby('Familia')['Riqueza'].sum().nlargest(10).index
    # ✅ Color categórico por Departamento
    fig = px.bar(agg[agg['Familia'].isin(top)], x='Riqueza', y='Familia', 
                 color='Departamento', title="🌿 Familias por Departamento (Top 10)",
                 color_discrete_sequence=CAT_COLORS, barmode='stack')
    fig.update_layout(yaxis={'categoryorder': 'array', 'categoryarray': top[::-1]})
    return _apply_dark_style(fig)

def plot_cooccurrence_matrix(df):
    """Matriz de co-ocurrencia con escala de alto contraste."""
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
    # ✅ Escala binaria de alto contraste: blanco/rojo oscuro
    fig = px.imshow(pivot, color_continuous_scale=['#FFFFFF', '#922B21'], 
                     title="🔗 Co-ocurrencia: Top 15 Especies × UM_id",
                     labels=dict(x="Especie", y="UM_id", color="Presencia"))
    fig.update_layout(xaxis_tickangle=-60, plot_bgcolor='white')
    return _apply_dark_style(fig)

def plot_cua_species_count(df):
    """CUA vs Cantidad de Especies con color por categoría CUA."""
    if df is None or df.empty or 'CUA' not in df.columns:
        return None
    species_per_cua = df.groupby('CUA')['Nombre científico'].nunique().reset_index(name='Especies')
    species_per_cua = species_per_cua.sort_values('Especies', ascending=False)
    # ✅ Color distinto por cada categoría CUA
    fig = px.bar(species_per_cua, x='CUA', y='Especies', 
                 title="📊 Especies Registradas por CUA",
                 color='CUA', color_discrete_sequence=CAT_COLORS, text_auto=True)
    fig.update_layout(xaxis_tickangle=-30, showlegend=False)
    return _apply_dark_style(fig)

def plot_cua_by_class_composition(df):
    """Composición por Clase dentro de cada CUA con colores por Clase."""
    if df is None or df.empty or 'CUA' not in df.columns:
        return None
    agg = df.groupby(['CUA', 'Clase']).size().reset_index(name='Registros')
    total = agg.groupby('CUA')['Registros'].transform('sum')
    agg['Pct'] = (agg['Registros'] / total * 100).round(1)
    # ✅ Color categórico por Clase para distinguir grupos taxonómicos
    fig = px.bar(agg, x='CUA', y='Pct', color='Clase',
                 title="🌍 Composición por Clase en cada CUA (%)",
                 color_discrete_sequence=CAT_COLORS,
                 text_auto='.1f', barmode='stack')
    fig.update_layout(yaxis_title="Porcentaje de Registros (%)", yaxis_range=[0, 105], xaxis_tickangle=-30)
    return _apply_dark_style(fig)
