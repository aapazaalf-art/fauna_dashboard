import streamlit as st
import pandas as pd

def setup_independent_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Filtros independientes en sidebar. Opciones calculadas desde el dataset completo."""
    st.sidebar.header("🔍 Filtros de Exploración")
    
    # Extraer opciones únicas del dataset COMPLETO (evita efecto cascada)
    opts = {col: sorted(df[col].dropna().unique().tolist()) for col in ['UM_id', 'Departamento', 'Ecozona', 'Clase', 'Familia', 'CUA']}
    opts['Año'] = sorted([int(y) for y in df['Año'].dropna().unique()])
    opts['Mes'] = sorted([int(m) for m in df['Mes'].dropna().unique()])

    sel_um = st.sidebar.multiselect("📍 Unidad Muestral (UM_id)", options=opts['UM_id'], default=[])
    sel_dept = st.sidebar.multiselect("🏛️ Departamento", options=opts['Departamento'], default=[])
    sel_eco = st.sidebar.multiselect("🌍 Ecozona", options=opts['Ecozona'], default=[])
    sel_year = st.sidebar.multiselect("📅 Año", options=opts['Año'], default=[])
    sel_mes = st.sidebar.multiselect("🗓️ Mes", options=opts['Mes'], default=[])
    sel_class = st.sidebar.multiselect("🦎 Clase", options=opts['Clase'], default=[])
    sel_fam = st.sidebar.multiselect("🌿 Familia", options=opts['Familia'], default=[])
    sel_cua = st.sidebar.multiselect("📊 CUA", options=opts['CUA'], default=[])

    # Aplicar intersección lógica mediante máscara booleana
    mask = pd.Series(True, index=df.index)
    if sel_um: mask &= df['UM_id'].isin(sel_um)
    if sel_dept: mask &= df['Departamento'].isin(sel_dept)
    if sel_eco: mask &= df['Ecozona'].isin(sel_eco)
    if sel_year: mask &= df['Año'].isin(sel_year)
    if sel_mes: mask &= df['Mes'].isin(sel_mes)
    if sel_class: mask &= df['Clase'].isin(sel_class)
    if sel_fam: mask &= df['Familia'].isin(sel_fam)
    if sel_cua: mask &= df['CUA'].isin(sel_cua)

    df_filtered = df[mask].copy()
    
    # Feedback visual en sidebar
    active = [f"UM:{len(sel_um)}" if sel_um else "", 
              f"Depto:{len(sel_dept)}" if sel_dept else "",
              f"Eco:{len(sel_eco)}" if sel_eco else "",
              f"Año:{len(sel_year)}" if sel_year else ""]
    active = [a for a in active if a]
    st.sidebar.caption("Filtros activos: " + " | ".join(active) if active else "Mostrando dataset completo")
    
    return df_filtered
