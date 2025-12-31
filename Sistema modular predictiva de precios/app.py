import streamlit as st
import pandas as pd
import loader   # <--- Importamos el nuevo cargador de Excel
import predictor
import config

# Configuración de Página
st.set_page_config(page_title="Predicciones de Mercado por IA", layout="wide")
st.title("📈 Predicciones de Mercado por IA: Tablero de Control")
st.markdown(f"**Fuente de Datos:** `{config.RUTA_ARCHIVO_EXCEL}`")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Panel de Control")

if st.sidebar.button("🔄 Recargar Excel"):
    st.cache_data.clear() # Borra memoria caché para forzar lectura nueva
    st.sidebar.success("Datos actualizados desde el archivo local.")

# --- LÓGICA PRINCIPAL ---
try:
    # 1. Cargamos datos REALES del Excel
    df = loader.cargar_datos_reales()
    
    if df is not None and not df.empty:
        # Selector de Producto
        lista_productos = df['producto'].unique()
        prod_seleccionado = st.selectbox("📦 Seleccionar Producto:", lista_productos)
        
        # Filtrar datos del producto
        df_filtrado = df[df['producto'] == prod_seleccionado].sort_values('fecha')
        
        # 2. IA PREDICTIVA
        # Solo predecimos si hay más de 1 dato para tener tendencia
        if len(df_filtrado) > 1:
            precio_futuro, variacion = predictor.predecir_precio(df_filtrado, dias_futuro=30)
            precio_actual = df_filtrado['precio'].iloc[-1]
            
            # Tarjetas de Métricas
            col1, col2, col3 = st.columns(3)
            col1.metric("Precio Actual (Excel)", f"${precio_actual:,.0f}")
            col2.metric("Proyección IA (30 días)", f"${precio_futuro:,.0f}")
            col3.metric("Tendencia", f"{variacion:.2f}%", 
                        delta_color="normal" if variacion > 0 else "inverse")
            
            # Gráfico
            st.subheader("Historial Real + Tendencia")
            st.line_chart(df_filtrado.set_index('fecha')['precio'])
            
            # Recomendación
            if variacion < -5:
                st.success("📉 OPORTUNIDAD: La IA predice que el precio BAJARÁ.")
            elif variacion > 5:
                st.warning("📈 ALERTA: La tendencia es fuertemente ALCISTA.")
            else:
                st.info("⚖️ El precio se mantendrá estable.")
                
        else:
            st.warning("⚠️ No hay suficiente historial en el Excel para este producto aún.")
            st.write("Datos disponibles:", df_filtrado)

    elif df is None:
        st.error("❌ No se encuentra el archivo Excel. Verifica la ruta en 'config.py'.")
    else:
        st.info("El Excel existe pero está vacío.")

except Exception as e:
    st.error(f"Error crítico en la aplicación: {e}")