import plotly.express as px
import pandas as pd
import streamlit as st

def plot_temporal(df: pd.DataFrame):
    """Registros por Mes/Año (Tendencia)."""
    if df.empty: return st.warning("Sin datos para gráfico temporal.")
    counts = df.groupby('Periodo', observed=True).size().reset_index(name='Registros')
    fig = px.line(counts, x='Periodo', y='Registros', markers=True, 
                  title="📈 Tendencia de Registros por Periodo (Mes/Año)")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

def plot_top_species(df: pd.DataFrame, n=10):
    """Top N especies por conteo."""
    if df.empty: return st.warning("Sin datos para top especies.")
    counts = df['Nombre científico'].value_counts().reset_index()
    counts.columns = ['Especie', 'Registros']
    counts = counts.head(n)
    fig = px.bar(counts, x='Especie', y='Registros', 
                 title=f"🦜 Top {n} Especies más Registradas",
                 color='Registros', color_continuous_scale='Viridis')
    fig.update_layout(xaxis_tickangle=-45, yaxis_title="Número de Registros")
    st.plotly_chart(fig, use_container_width=True)

def plot_class_dist(df: pd.DataFrame):
    """Distribución por Clase Taxonómica."""
    if df.empty: return st.warning("Sin datos para distribución por Clase.")
    counts = df['Clase'].value_counts().reset_index()
    counts.columns = ['Clase', 'Registros']
    fig = px.pie(counts, values='Registros', names='Clase', 
                 title="🦎 Distribución por Clase Taxonómica", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

def plot_spatial(df: pd.DataFrame):
    """Scatter UTM con advertencia."""
    valid = df[['X-UTM', 'Y-UTM', 'Nombre científico', 'Clase', 'UM_id']].dropna()
    if valid.empty: return st.warning("Sin coordenadas válidas para visualización espacial.")
    fig = px.scatter(valid, x='X-UTM', y='Y-UTM', color='Clase', 
                     hover_data=['Nombre científico', 'UM_id'],
                     title="🗺️ Distribución Espacial (X-UTM vs Y-UTM)")
    st.caption("⚠️ Nota: Las coordenadas UTM requieren un sistema de referencia específico (Datum/Eje) para proyección cartográfica exacta. Esta visualización es relativa.")
    st.plotly_chart(fig, use_container_width=True)