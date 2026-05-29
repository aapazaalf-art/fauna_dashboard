import plotly.express as px
import pandas as pd
import streamlit as st

# ... [mantener funciones existentes: plot_temporal, plot_top_species, plot_class_dist, plot_spatial] ...

def plot_hierarchical_distribution(df: pd.DataFrame):
    """
    Visualización jerárquica: Ecozona -> Departamento -> Familia.
    Usa Treemap para mostrar concentración relativa y permite navegación interactiva.
    """
    st.subheader("🌳 Distribución: Ecozona → Departamento → Familia")
    
    if df.empty:
        st.warning("Sin datos para visualización jerárquica.")
        return

    col_met, col_info = st.columns([1, 3])
    with col_met:
        metric = st.radio(
            "Métrica de concentración:",
            ["Registros (conteo filas)", "Especies Únicas"],
            horizontal=True,
            key="hier_metric"
        )
    with col_info:
        st.caption("💡 Haz clic en cualquier sección para profundizar. La proporción refleja la métrica seleccionada.")

    if metric == "Registros (conteo filas)":
        df_plot = df.copy()
        df_plot['Valor'] = 1
        fig = px.treemap(
            df_plot, 
            path=['Ecozona', 'Departamento', 'Familia'], 
            values='Valor',
            title="Concentración de Registros por Ubicación y Familia",
            color='Ecozona',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
    else:
        agg = df.groupby(['Ecozona', 'Departamento', 'Familia'])['Nombre científico'].nunique().reset_index(name='Valor')
        fig = px.treemap(
            agg, 
            path=['Ecozona', 'Departamento', 'Familia'], 
            values='Valor',
            title="Riqueza de Especies Únicas por Ubicación y Familia",
            color='Ecozona',
            color_discrete_sequence=px.colors.qualitative.Set3
        )

    fig.update_layout(margin=dict(t=40, l=20, r=20, b=20), title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
