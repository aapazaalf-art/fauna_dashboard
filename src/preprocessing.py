import pandas as pd
import numpy as np

def preprocess_fauna(df: pd.DataFrame) -> pd.DataFrame:
    """Limpieza, normalización de tipos y creación de columnas derivadas."""
    df = df.copy()

    # 1. Normalizar texto (quitar espacios, manejar nulos)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace(['nan', 'NaN', 'None', ''], np.nan)

    # 2. Convertir a numéricos coerciendo errores
    num_cols = ['Mes', 'Año', 'X-UTM', 'Y-UTM', 'Altitud (m)', 'Distancia (m)']
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3. Crear columna Periodo (Mes/Año) y ordenarla cronológicamente
    df['Periodo'] = (df['Mes'].astype('Int64').astype(str) + '/' + 
                     df['Año'].astype('Int64').astype(str))
    # Generar categorías ordenadas
    years = sorted(df['Año'].dropna().unique())
    df['Periodo'] = pd.Categorical(
        df['Periodo'],
        categories=[f"{m}/{y}" for y in years for m in range(1, 13)],
        ordered=True
    )

    # 4. Manejo de nulos para filtros categóricos
    for col in ['CUA', 'Tipo de registro', 'Zona UTM', 'Clase', 'Familia', 'Departamento']:
        if col in df.columns:
            df[col] = df[col].fillna('Sin dato')

    return df