import pandas as pd
import streamlit as st

@st.cache_data
def load_raw_data(filepath: str) -> pd.DataFrame:
    """Carga el Excel y valida existencia del archivo."""
    try:
        return pd.read_excel(filepath)
    except FileNotFoundError:
        st.error(f"❌ No se encontró el archivo en: {filepath}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {e}")
        return pd.DataFrame()
