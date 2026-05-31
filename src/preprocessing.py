import pandas as pd
import numpy as np

def preprocess_fauna(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Normalizar texto
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace(['nan', 'NaN', 'None', ''], np.nan)
    
    # Convertir numéricos
    for col in ['Mes', 'Año', 'X-UTM', 'Y-UTM', 'Altitud (m)', 'Distancia (m)']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Crear Periodo
    if 'Mes' in df.columns and 'Año' in df.columns:
        valid = df['Mes'].notna() & df['Año'].notna()
        df['Periodo'] = ''
        df.loc[valid, 'Periodo'] = df.loc[valid, 'Mes'].astype(int).astype(str) + '/' + df.loc[valid, 'Año'].astype(int).astype(str)
    
    # Manejar nulos en categóricas
    for col in ['CUA', 'Clase', 'Familia', 'Departamento', 'Ecozona']:
        if col in df.columns:
            df[col] = df[col].fillna('Sin dato')
    
    return df
