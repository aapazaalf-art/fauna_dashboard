import pandas as pd
import streamlit as st

@st.cache_data
def load_raw_data(filepath: str) -> pd.DataFrame:
    """Carga el Excel desde la ruta especificada."""
    try:
        df = pd.read_excel(filepath)
        return df
    except Exception as e:
        st.error(f"Error al cargar {filepath}: {e}")
        st.stop()
        return pd.DataFrame()