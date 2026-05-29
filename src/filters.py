import streamlit as st
import pandas as pd

def setup_independent_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Configura filtros completamente independientes en el sidebar.
    - Las opciones de cada widget se calculan SIEMPRE desde el dataset completo.
    - La selección de uno NO limita las opciones de los demás.
    - El resultado final es la INTERSECCIÓN de todos los filtros activos.
    """
    st.sidebar.header("🔍 Filtros de Exploración")

    # 1. Extraer opciones desde el dataset COMPLETO (evita efecto cascada)
    opts_um = sorted(df['UM_id'].dropna().unique().tolist())
    opts_dept = sorted(df['Departamento'].dropna().unique().tolist())
    opts_eco = sorted(df['Ecozona'].dropna().unique().tolist())
    opts_year = sorted([int(y) for y in df['Año'].dropna().unique()])
    opts_mes = sorted([int(m) for m in df['Mes'].dropna().unique()])
    opts_class = sorted(df['Clase'].dropna().unique().tolist())
    opts_fam = sorted(df['Familia'].dropna().unique().tolist())
    opts_cua = sorted(df['CUA'].dropna().unique().tolist())

    # 2. Widgets independientes (default=[] significa "sin restricción inicial")
    sel_um = st.sidebar.multiselect("📍 Unidad Muestral (UM_id)", options=opts_um, default=[])
    sel_dept = st.sidebar.multiselect("🏛️ Departamento", options=opts_dept, default=[])
    sel_eco = st.sidebar.multiselect("🌍 Ecozona", options=opts_eco, default=[])
    sel_year = st.sidebar.multiselect("📅 Año", options=opts_year, default=[])
    sel_mes = st.sidebar.multiselect("🗓️ Mes", options=opts_mes, default=[])
    sel_class = st.sidebar.multiselect("🦎 Clase", options=opts_class, default=[])
    sel_fam = st.sidebar.multiselect("🌿 Familia", options=opts_fam, default=[])
    sel_cua = st.sidebar.multiselect("📊 CUA", options=opts_cua, default=[])

    # 3. Aplicar filtros sobre el dataset COMPLETO mediante máscara booleana
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

    # 4. Feedback visual de filtros activos
    active = []
    if sel_um: active.append(f"UM: {len(sel_um)}")
    if sel_dept: active.append(f"Depto: {len(sel_dept)}")
    if sel_eco: active.append(f"Eco: {len(sel_eco)}")
    if sel_year: active.append(f"Año: {len(sel_year)}")

    st.sidebar.caption("Filtros activos: " + " | ".join(active) if active else "Mostrando dataset completo")

    return df_filtered
