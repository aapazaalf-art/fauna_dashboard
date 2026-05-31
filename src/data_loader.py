import pandas as pd
import streamlit as st

@st.cache_data
def load_raw_data(filepath: str) -> pd.DataFrame:
    """Carga el Excel desde la ruta especificada con manejo de errores."""
    try:
        df = pd.read_excel(filepath)
        return df
    except FileNotFoundError:
        st.error(f"❌ Archivo no encontrado: {filepath}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {e}")
        return pd.DataFrame()
