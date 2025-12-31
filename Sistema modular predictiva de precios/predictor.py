# predictor.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime

def predecir_precio(df_producto, dias_futuro=30):
    """
    Entrena un modelo de regresión lineal y predice precios futuros.
    Retorna: El precio futuro estimado y el porcentaje de variación.
    """
    # 1. Preparar datos (Ingeniería de Características)
    df_producto = df_producto.sort_values('fecha')
    df_producto['dia_num'] = (df_producto['fecha'] - df_producto['fecha'].min()).dt.days
    
    X = df_producto[['dia_num']]
    y = df_producto['precio']
    
    # 2. Entrenar Modelo
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    # 3. Predecir Futuro
    ultimo_dia = df_producto['dia_num'].max()
    dia_objetivo = np.array([[ultimo_dia + dias_futuro]])
    precio_predicho = modelo.predict(dia_objetivo)[0]
    
    # 4. Calcular tendencia
    precio_hoy = y.iloc[-1]
    variacion = ((precio_predicho - precio_hoy) / precio_hoy) * 100
    
    return precio_predicho, variacion