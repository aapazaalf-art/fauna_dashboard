import streamlit as st
import pandas as pd

def setup_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    """Configura filtros en sidebar con lógica jerárquica."""
    st.sidebar.header("🔍 Filtros de Exploración")

    # UM_id (Obligatorio/Multiselect)
    um_options = sorted(df['UM_id'].dropna().unique().tolist())
    selected_um = st.sidebar.multiselect("Unidad Muestral (UM_id)", options=um_options, 
                                         default=um_options[:5] if len(um_options) >= 5 else um_options)
    if not selected_um:
        st.sidebar.warning("Seleccione al menos una UM_id.")
        st.stop()
    
    df_filt = df[df['UM_id'].isin(selected_um)].copy()

    # Filtros secuenciales (cascada)
    deptos = sorted(df_filt['Departamento'].unique())
    sel_dept = st.sidebar.selectbox("Departamento", ["Todos"] + deptos)
    if sel_dept != "Todos": df_filt = df_filt[df_filt['Departamento'] == sel_dept]

    years = sorted(df_filt['Año'].dropna().unique())
    sel_year = st.sidebar.selectbox("Año", ["Todos"] + [int(y) for y in years])
    if sel_year != "Todos": df_filt = df_filt[df_filt['Año'] == sel_year]

    months = sorted(df_filt['Mes'].dropna().unique())
    sel_month = st.sidebar.selectbox("Mes", ["Todos"] + [int(m) for m in months])
    if sel_month != "Todos": df_filt = df_filt[df_filt['Mes'] == sel_month]

    clases = sorted(df_filt['Clase'].unique())
    sel_class = st.sidebar.selectbox("Clase", ["Todos"] + clases)
    if sel_class != "Todos": df_filt = df_filt[df_filt['Clase'] == sel_class]

    familias = sorted(df_filt['Familia'].unique())
    sel_fam = st.sidebar.selectbox("Familia", ["Todos"] + familias)
    if sel_fam != "Todos": df_filt = df_filt[df_filt['Familia'] == sel_fam]

    cuas = sorted(df_filt['CUA'].unique())
    sel_cua = st.sidebar.selectbox("CUA", ["Todos"] + cuas)
    if sel_cua != "Todos": df_filt = df_filt[df_filt['CUA'] == sel_cua]

    # Búsqueda de especie
    especies = sorted(df_filt['Nombre científico'].dropna().unique().tolist())
    sel_species = st.sidebar.multiselect("Especie (Nombre científico)", options=especies)
    if sel_species: df_filt = df_filt[df_filt['Nombre científico'].isin(sel_species)]

    return df_filt