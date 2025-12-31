import pandas as pd
import config

def cargar_datos_reales():
    """
    Lee el Excel generado por el monitor de precios.
    Corrige el error de formatos de fecha mixtos.
    """
    try:
        # 1. Leer el Excel
        df = pd.read_excel(config.RUTA_ARCHIVO_EXCEL)
        
        # 2. Seleccionar y Renombrar columnas según tu config
        df = df[[config.COLUMNA_FECHA, config.COLUMNA_PRODUCTO, config.COLUMNA_PRECIO]]
        df.columns = ['fecha', 'producto', 'precio']
        
        # 3. CORRECCIÓN DEL ERROR (Aquí está la magia ✨)
        # 'format=mixed' permite que convivan fechas con y sin milisegundos
        df['fecha'] = pd.to_datetime(df['fecha'], format='mixed')
        
        # 4. Limpieza de Precio
        if df['precio'].dtype == 'O': # Si es texto
            df['precio'] = df['precio'].astype(str).str.replace('$', '', regex=False)
            df['precio'] = df['precio'].str.replace('.', '', regex=False) # Quita miles
            df['precio'] = df['precio'].str.replace(',', '.', regex=False) # Coma decimal
        
        df['precio'] = pd.to_numeric(df['precio'])
        
        return df

    except Exception as e:
        print(f"Error detallado leyendo Excel: {e}")
        return pd.DataFrame()