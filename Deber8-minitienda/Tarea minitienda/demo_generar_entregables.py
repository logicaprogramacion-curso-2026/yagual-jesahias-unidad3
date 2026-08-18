import os
from minitienda import (
    cargar_catalogo, inicializar_precios_stock, agregar_producto,
    actualizar_precio_stock, registrar_venta, guardar_ventas_csv,
    leer_ventas_csv, calcular_metricas, graficar_ingresos, registrar_log,
    CSV_PATH, LOG_PATH, PNG_PATH,
)

# Limpieza de entregables previos para una demo reproducible
for f in (CSV_PATH, LOG_PATH, PNG_PATH):
    if os.path.exists(f):
        os.remove(f)

catalogo = cargar_catalogo()
precios, stock = inicializar_precios_stock(catalogo)

ventas_buffer = []
ids_ventas = []

# --- RETO A: agregar un producto nuevo y actualizar precio/stock ---
catalogo, nuevo_id = agregar_producto(
    catalogo, precios, stock,
    nombre="Base Enfriadora Laptop", categoria="Accesorios",
    precio=22.50, stock_inicial=18,
)
registrar_log(f"CATALOGO - producto nuevo agregado id {nuevo_id} (Base Enfriadora Laptop).")
actualizar_precio_stock(precios, stock, producto_id=1, nuevo_precio=13.00, nuevo_stock=48)
registrar_log("CATALOGO - producto_id 1 actualizado (precio=13.00, stock=48).")

# --- Ventas simuladas (>= 10), incluyendo un caso con descuento (Reto C) ---
ventas_a_registrar = [
    (1, 2),
    (2, 1),
    (3, 3),
    (4, 5),
    (5, 4),
    (6, 2),
    (1, 12),   # >=10 unidades -> aplica descuento del 5%
    (2, 6),
    (nuevo_id, 3),
    (3, 1),
    (4, 8),
    (6, 10),   # >=10 unidades -> aplica descuento del 5%
]

for producto_id, cantidad in ventas_a_registrar:
    registrar_venta(catalogo, precios, stock, ventas_buffer, ids_ventas, producto_id, cantidad)

# --- RETO D: intento fallido con producto_id inexistente (se loguea) ---
registrar_venta(catalogo, precios, stock, ventas_buffer, ids_ventas, producto_id=999, cantidad=2)

# Guardar ventas en CSV
guardar_ventas_csv(ventas_buffer, CSV_PATH)
print(f"\nSe guardaron {len(ventas_buffer)} ventas en '{CSV_PATH}'.")

# Leer con pandas y calcular metricas con NumPy
df = leer_ventas_csv(CSV_PATH)
print("\nDataFrame de ventas:")
print(df)

metricas = calcular_metricas(df)

# Graficar y exportar a PNG (Reto B)
graficar_ingresos(df, guardar=True, path=PNG_PATH)

print("\nContenido de log.txt:")
with open(LOG_PATH, "r", encoding="utf-8") as f:
    print(f.read())
