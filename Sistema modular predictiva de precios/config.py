# config.py

# RUTA EXACTA DE TU EXCEL
# (Verifica que esta ruta sea la correcta, la que se ve en tu captura)
RUTA_ARCHIVO_EXCEL = r"Ruta de tu archivo\reporte_precios.xlsx"

# --- MAPEO DE COLUMNAS (Aquí estaba el error) ---
# Izquierda: Nombre en el código | Derecha: Nombre REAL en tu Excel
COLUMNA_FECHA = "fecha_registro"  # Antes era "Fecha"
COLUMNA_PRODUCTO = "nombre"       # Antes era "Producto"
COLUMNA_PRECIO = "precio"         # Este ya estaba bien

# CONFIGURACIÓN OPCIONAL (Si usas simulación)
PRODUCTOS_OBJETIVO = {
    "Smart TV Philips 43\" Full HD": 325,
    "Disco Duro Skyhawk 4TB (CCTV)": 175,
    "Bobina Cable UTP Hikvision (Ext)": 100
}