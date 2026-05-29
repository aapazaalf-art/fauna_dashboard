def plot_hierarchical_distribution(df: pd.DataFrame):
    st.subheader("🌳 Distribución: Ecozona → Departamento → Familia")
    if df.empty:
        return st.warning("Sin datos para visualización jerárquica.")

    metric = st.radio(
        "Métrica de concentración:",
        ["Registros (conteo)", "Especies Únicas"],
        horizontal=True,
        key="hier_metric"
    )
    st.caption("💡 Haz clic en cualquier segmento para profundizar. El número central indica la cantidad exacta.")

    if metric == "Registros (conteo)":
        df_plot = df.copy()
        df_plot['Valor'] = 1
    else:
        df_plot = df.groupby(['Ecozona', 'Departamento', 'Familia'])['Nombre científico'].nunique().reset_index(name='Valor')

    fig = px.treemap(
        df_plot,
        path=['Ecozona', 'Departamento', 'Familia'],
        values='Valor',
        title=f"Concentración por {metric}",
        color='Ecozona',
        color_discrete_sequence=px.colors.qualitative.Set3,
        hover_data={'Ecozona': True, 'Departamento': True, 'Familia': True, 'Valor': True}
    )

    # 🔢 Mostrar cantidad numérica centrada en cada cuadro
    fig.update_traces(
        texttemplate='%{label}<br>%{value:.0f}',
        textposition='middle center',
        textfont=dict(size=14, color='white', family='Arial')
    )
    fig.update_layout(margin=dict(t=40, l=20, r=20, b=20), title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
