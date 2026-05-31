import streamlit as st
import pandas as pd

def setup_independent_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("🔍 Filtros")
    
    opts = {
        'UM_id': sorted(df['UM_id'].dropna().unique().tolist()),
        'Departamento': sorted(df['Departamento'].dropna().unique().tolist()),
        'Ecozona': sorted(df['Ecozona'].dropna().unique().tolist()) if 'Ecozona' in df.columns else [],
        'Año': sorted([int(y) for y in df['Año'].dropna().unique()]),
        'Mes': sorted([int(m) for m in df['Mes'].dropna().unique()]),
        'Clase': sorted(df['Clase'].dropna().unique().tolist()),
        'Familia': sorted(df['Familia'].dropna().unique().tolist()),
        'CUA': sorted(df['CUA'].dropna().unique().tolist())
    }
    
    sel_um = st.sidebar.multiselect("UM_id", options=opts['UM_id'], default=[])
    sel_dept = st.sidebar.multiselect("Departamento", options=opts['Departamento'], default=[])
    sel_eco = st.sidebar.multiselect("Ecozona", options=opts['Ecozona'], default=[])
    sel_year = st.sidebar.multiselect("Año", options=opts['Año'], default=[])
    sel_mes = st.sidebar.multiselect("Mes", options=opts['Mes'], default=[])
    sel_class = st.sidebar.multiselect("Clase", options=opts['Clase'], default=[])
    sel_fam = st.sidebar.multiselect("Familia", options=opts['Familia'], default=[])
    sel_cua = st.sidebar.multiselect("CUA", options=opts['CUA'], default=[])
    
    mask = pd.Series(True, index=df.index)
    if sel_um: mask &= df['UM_id'].isin(sel_um)
    if sel_dept: mask &= df['Departamento'].isin(sel_dept)
    if sel_eco: mask &= df['Ecozona'].isin(sel_eco)
    if sel_year: mask &= df['Año'].isin(sel_year)
    if sel_mes: mask &= df['Mes'].isin(sel_mes)
    if sel_class: mask &= df['Clase'].isin(sel_class)
    if sel_fam: mask &= df['Familia'].isin(sel_fam)
    if sel_cua: mask &= df['CUA'].isin(sel_cua)
    
    return df[mask].copy()
