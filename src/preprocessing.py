import pandas as pd
import numpy as np

def preprocess_fauna(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # 1. Normalizar texto
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace(['nan', 'NaN', 'None', ''], np.nan)

    # 2. Convertir numéricos
    num_cols = ['Mes', 'Año', 'X-UTM', 'Y-UTM', 'Altitud (m)', 'Distancia (m)']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3. Crear Periodo de forma segura
    if 'Mes' in df.columns and 'Año' in df.columns:
        valid = df['Mes'].notna() & df['Año'].notna()
        df['Periodo'] = ''
        df.loc[valid, 'Periodo'] = df.loc[valid, 'Mes'].astype(int).astype(str) + '/' + df.loc[valid, 'Año'].astype(int).astype(str)
        years = sorted(df['Año'].dropna().unique())
        cats = [f"{m}/{y}" for y in years for m in range(1, 13)]
        df['Periodo'] = pd.Categorical(df['Periodo'], categories=cats, ordered=True)
    else:
        df['Periodo'] = 'Sin dato'

    # 4. Manejo de nulos para filtros
    for col in ['CUA', 'Tipo de registro', 'Zona UTM', 'Clase', 'Familia', 'Departamento', 'Ecozona']:
        if col in df.columns:
            df[col] = df[col].fillna('Sin dato')

    return df
