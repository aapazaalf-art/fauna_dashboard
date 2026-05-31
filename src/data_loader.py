import pandas as pd
import streamlit as st

@st.cache_data
def load_raw_data(filepath: str) -> pd.DataFrame:
    try:
        return pd.read_excel(filepath)
    except Exception as e:
        st.error(f"❌ Error al cargar {filepath}: {e}")
        return pd.DataFrame()
