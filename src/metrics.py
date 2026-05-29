import streamlit as st

def compute_kpis(df: pd.DataFrame) -> dict:
    """Calcula indicadores clave recalculables."""
    total_records = len(df)
    unique_species = df['Nombre científico'].nunique()
    unique_families = df['Familia'].nunique()
    # Contar fotos válidas (no nulas y no vacías)
    valid_photos = df['Número de foto'].notna() & (df['Número de foto'].astype(str).str.strip() != '')
    photo_count = valid_photos.sum()

    return {
        "Total Registros": total_records,
        "Especies Únicas": unique_species,
        "Familias Únicas": unique_families,
        "Registros con Foto": photo_count
    }