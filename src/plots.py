def plot_cua_species_visual(df: pd.DataFrame):
    """
    Visualización mejorada para CUA: Treemap jerárquico CUA → Especies.
    Muestra las especies más destacadas por categoría de uso actual.
    """
    if df.empty or 'CUA' not in df.columns: 
        return None
    
    # Agrupar: CUA → Especies, contando registros
    agg = df.groupby(['CUA', 'Nombre científico']).size().reset_index(name='Registros')
    
    # Filtrar top 3 especies por CUA para evitar saturación visual
    top_species = agg.sort_values('Registros', ascending=False).groupby('CUA').head(3)
    
    fig = px.treemap(
        top_species,
        path=['CUA', 'Nombre científico'],
        values='Registros',
        title="📊 Especies Destacadas por CUA (Top 3 por categoría)",
        color='Registros',
        color_continuous_scale='Viridis',
        hover_data={'Registros': True, 'Nombre científico': True}
    )
    
    # Accesibilidad: texto oscuro y legible
    fig.update_traces(
        texttemplate='%{label}<br>📄 %{value}',
        textposition='middle center',
        textfont=dict(size=13, color='#000000', family='Arial, sans-serif')
    )
    fig.update_layout(
        title_font=dict(size=18, color='#000000'),
        font=dict(size=12, color='#000000'),
        margin=dict(t=50, l=20, r=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig
