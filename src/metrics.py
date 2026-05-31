def compute_kpis(df: pd.DataFrame) -> dict:
    return {
        "Total Registros": len(df),
        "Especies Únicas": df['Nombre científico'].nunique(),
        "Familias Únicas": df['Familia'].nunique(),
        "Registros con Foto": (df['Número de foto'].notna() & (df['Número de foto'].astype(str).str.strip() != '')).sum()
    }
