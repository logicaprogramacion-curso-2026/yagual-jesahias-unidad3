import os
import csv
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV_PATH = "ventas.csv"
LOG_PATH = "log.txt"
PNG_PATH = "ingresos.png"

CSV_HEADERS = ["venta_id", "producto_id", "producto_nombre",
               "cantidad", "precio_unitario", "descuento_pct",
               "total", "fecha"]

def cargar_catalogo():

    catalogo = (
        (1, "Mouse Inalambrico", "Perifericos"),
        (2, "Teclado Mecanico", "Perifericos"),
        (3, "Monitor 24\"", "Pantallas"),
        (4, "Audifonos Bluetooth", "Audio"),
        (5, "Webcam HD", "Video"),
        (6, "Disco SSD 480GB", "Almacenamiento"),
    )
    return catalogo

def inicializar_precios_stock(catalogo):
    precios = {
        1: 12.50,
        2: 35.00,
        3: 120.00,
        4: 25.90,
        5: 18.75,
        6: 45.00,
    }
    stock = {
        1: 50,
        2: 30,
        3: 15,
        4: 40,
        5: 25,
        6: 20,
    }
    for producto in catalogo:
        pid = producto[0]
        if pid not in precios:
            precios[pid] = 0.0
        if pid not in stock:
            stock[pid] = 0
    return precios, stock

def buscar_producto(catalogo, producto_id):
    for producto in catalogo:
        if producto[0] == producto_id:
            return producto
    return None

def mostrar_catalogo(catalogo, precios, stock):
    print("\n" + "-" * 60)
    print(f"{'ID':<4}{'Producto':<24}{'Categoria':<16}{'Precio':<10}{'Stock':<6}")
    print("-" * 60)
    for producto in catalogo:
        pid, nombre, categoria = producto
        print(f"{pid:<4}{nombre:<24}{categoria:<16}${precios.get(pid, 0):<9.2f}{stock.get(pid, 0):<6}")
    print("-" * 60)

def agregar_producto(catalogo, precios, stock, nombre, categoria, precio, stock_inicial):
    nuevo_id = max(p[0] for p in catalogo) + 1 if catalogo else 1
    nuevo_producto = (nuevo_id, nombre, categoria)
    catalogo = catalogo + (nuevo_producto,)  # las tuplas son inmutables -> se crea una nueva
    precios[nuevo_id] = precio
    stock[nuevo_id] = stock_inicial
    return catalogo, nuevo_id


def actualizar_precio_stock(precios, stock, producto_id, nuevo_precio=None, nuevo_stock=None):
    if producto_id not in precios:
        raise KeyError(f"El producto {producto_id} no existe en precios/stock.")
    if nuevo_precio is not None:
        precios[producto_id] = nuevo_precio
    if nuevo_stock is not None:
        stock[producto_id] = nuevo_stock

def registrar_log(mensaje):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {mensaje}\n")
    except OSError as e:
        print(f"Aviso: no se pudo escribir en el log ({e}).")

def registrar_venta(catalogo, precios, stock, ventas_buffer, ids_ventas,
                     producto_id, cantidad):
    producto = buscar_producto(catalogo, producto_id)

    if producto is None:
        # RETO D: intento fallido por producto inexistente -> se registra en log.txt
        registrar_log(f"INTENTO FALLIDO - producto_id {producto_id} no existe en el catalogo.")
        print("Error: ese producto_id no existe en el catálogo.")
        return False

    if cantidad <= 0:
        registrar_log(f"INTENTO FALLIDO - cantidad invalida ({cantidad}) para producto_id {producto_id}.")
        print("Error: la cantidad debe ser mayor a 0.")
        return False

    stock_disponible = stock.get(producto_id, 0)
    if cantidad > stock_disponible:
        registrar_log(
            f"INTENTO FALLIDO - stock insuficiente para producto_id {producto_id} "
            f"(solicitado {cantidad}, disponible {stock_disponible})."
        )
        print(f"Error: stock insuficiente. Disponible: {stock_disponible}.")
        return False

    precio_unitario = precios.get(producto_id, 0.0)

    # RETO C: descuento del 5% si unidades >= 10
    descuento_pct = 0
    if cantidad >= 10:
        descuento_pct = 5

    subtotal = precio_unitario * cantidad
    total = subtotal * (1 - descuento_pct / 100)

    venta_id = (max(ids_ventas) + 1) if ids_ventas else 1
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    venta = {
        "venta_id": venta_id,
        "producto_id": producto_id,
        "producto_nombre": producto[1],
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "descuento_pct": descuento_pct,
        "total": round(total, 2),
        "fecha": fecha,
    }

    ventas_buffer.append(venta)
    ids_ventas.append(venta_id)
    stock[producto_id] = stock_disponible - cantidad

    registrar_log(f"VENTA OK - id {venta_id}, producto_id {producto_id}, "
                  f"cantidad {cantidad}, descuento {descuento_pct}%, total {venta['total']}.")

    if descuento_pct:
        print(f"Venta registrada con descuento del {descuento_pct}% -> total: ${venta['total']:.2f}")
    else:
        print(f"Venta registrada. Total: ${venta['total']:.2f}")
    return True

def guardar_ventas_csv(ventas_buffer, path=CSV_PATH):
    archivo_existe = os.path.isfile(path)
    try:
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            if not archivo_existe:
                writer.writeheader()
            for venta in ventas_buffer:
                writer.writerow(venta)
    except OSError as e:
        print(f"Error al guardar el CSV: {e}")
        registrar_log(f"ERROR - no se pudo guardar ventas.csv ({e}).")
        return False
    return True


def leer_ventas_csv(path=CSV_PATH):
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(f"Error: el archivo '{path}' no existe todavía. Registra alguna venta primero.")
        registrar_log(f"ERROR - intento de lectura de {path} pero el archivo no existe.")
        return pd.DataFrame(columns=CSV_HEADERS)
    except pd.errors.EmptyDataError:
        print("Error: el archivo de ventas está vacío.")
        return pd.DataFrame(columns=CSV_HEADERS)
    else:
        return df


def resumen_por_producto(df):
    if df.empty:
        return pd.DataFrame(columns=["producto_nombre", "cantidad", "total"])
    resumen = (
        df.groupby("producto_nombre", as_index=False)[["cantidad", "total"]]
        .sum()
        .sort_values(by="total", ascending=False)
    )
    return resumen

def calcular_metricas(df):
    if df.empty:
        print("No hay ventas registradas todavía para calcular métricas.")
        return None

    totales = np.array(df["total"], dtype=float)
    cantidades = np.array(df["cantidad"], dtype=float)

    metricas = {
        "num_ventas": len(totales),
        "ingreso_total": float(np.sum(totales)),
        "ingreso_promedio": float(np.mean(totales)),
        "ingreso_std": float(np.std(totales)),
        "unidades_totales": int(np.sum(cantidades)),
        "unidades_promedio": float(np.mean(cantidades)),
    }

    try:
        precio_promedio_unidad = metricas["ingreso_total"] / metricas["unidades_totales"]
    except ZeroDivisionError:
        precio_promedio_unidad = 0.0
        registrar_log("ERROR - division por cero al calcular precio promedio por unidad.")
    metricas["precio_promedio_unidad"] = precio_promedio_unidad

    print("\n--- Métricas (NumPy) ---")
    print(f"N° de ventas          : {metricas['num_ventas']}")
    print(f"Ingreso total          : ${metricas['ingreso_total']:.2f}")
    print(f"Ingreso promedio/venta : ${metricas['ingreso_promedio']:.2f}")
    print(f"Desviacion estandar    : ${metricas['ingreso_std']:.2f}")
    print(f"Unidades totales       : {metricas['unidades_totales']}")
    print(f"Unidades promedio/venta: {metricas['unidades_promedio']:.2f}")
    print(f"Precio promedio/unidad : ${metricas['precio_promedio_unidad']:.2f}")

    return metricas

def graficar_ingresos(df, guardar=False, path=PNG_PATH, mostrar=False):
    resumen = resumen_por_producto(df)
    if resumen.empty:
        print("No hay datos para graficar.")
        return None

    fig, ax = plt.subplots(figsize=(9, 5.5))
    barras = ax.bar(resumen["producto_nombre"], resumen["total"], color="#4C72B0")

    ax.set_title("Ingresos por producto - MiniTienda")
    ax.set_xlabel("Producto")
    ax.set_ylabel("Ingresos ($)")
    ax.set_xticks(range(len(resumen["producto_nombre"])))
    ax.set_xticklabels(resumen["producto_nombre"], rotation=30, ha="right")

    for barra in barras:
        altura = barra.get_height()
        ax.annotate(f"${altura:,.2f}",
                    xy=(barra.get_x() + barra.get_width() / 2, altura),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8)

    fig.tight_layout()

    if guardar:
        try:
            fig.savefig(path, dpi=150)
            print(f"Grafico exportado como '{path}'.")
            registrar_log(f"EXPORT - grafico de ingresos guardado en {path}.")
        except OSError as e:
            print(f"Error al exportar el grafico: {e}")
            registrar_log(f"ERROR - no se pudo exportar el grafico ({e}).")

    if mostrar:
        plt.show()

    plt.close(fig)
    return resumen

def pedir_entero(mensaje):
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
        except ValueError:
            print("Entrada invalida: debes ingresar un numero entero.")
            continue
        else:
            return valor


def pedir_float(mensaje):
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = float(entrada)
        except ValueError:
            print("Entrada invalida: debes ingresar un numero (puede tener decimales).")
            continue
        else:
            return valor


def pedir_texto(mensaje):
    while True:
        entrada = input(mensaje).strip()
        if entrada == "":
            print("La entrada no puede estar vacia.")
            continue
        return entrada

def menu():
    catalogo = cargar_catalogo()
    precios, stock = inicializar_precios_stock(catalogo)

    ventas_buffer = []   # lista: ventas pendientes de guardar en esta sesion
    ids_ventas = []       # lista: IDs usados en esta sesion

    opciones_validas = {"1", "2", "3", "4", "5", "6", "7", "0"}

    while True:
        print("\n" + "=" * 40)
        print("        MENU - MiniTienda")
        print("=" * 40)
        print("1) Ver catalogo")
        print("2) Registrar venta")
        print("3) Agregar producto / actualizar precio-stock")
        print("4) Guardar ventas en CSV")
        print("5) Ver metricas (NumPy + Pandas)")
        print("6) Graficar ingresos por producto")
        print("7) Exportar grafico a PNG")
        print("0) Salir")
        print("=" * 40)

        opcion = input("Elige una opcion: ").strip()

        if opcion not in opciones_validas:
            print("Opcion invalida, intenta de nuevo.")
            continue  # vuelve al inicio del while sin procesar nada mas

        if opcion == "1":
            mostrar_catalogo(catalogo, precios, stock)

        elif opcion == "2":
            mostrar_catalogo(catalogo, precios, stock)
            producto_id = pedir_entero("ID del producto a vender: ")
            cantidad = pedir_entero("Cantidad: ")
            registrar_venta(catalogo, precios, stock, ventas_buffer, ids_ventas,
                             producto_id, cantidad)

        elif opcion == "3":
            print("\na) Agregar producto nuevo   b) Actualizar precio/stock existente")
            sub = input("Elige a/b: ").strip().lower()
            if sub == "a":
                nombre = pedir_texto("Nombre del producto: ")
                categoria = pedir_texto("Categoria: ")
                precio = pedir_float("Precio: ")
                stock_inicial = pedir_entero("Stock inicial: ")
                catalogo, nuevo_id = agregar_producto(
                    catalogo, precios, stock, nombre, categoria, precio, stock_inicial
                )
                registrar_log(f"CATALOGO - producto nuevo agregado id {nuevo_id} ({nombre}).")
                print(f"Producto agregado con id {nuevo_id}.")
            elif sub == "b":
                producto_id = pedir_entero("ID del producto a actualizar: ")
                if buscar_producto(catalogo, producto_id) is None:
                    print("Ese producto_id no existe.")
                    registrar_log(f"INTENTO FALLIDO - actualizar producto_id {producto_id} inexistente.")
                else:
                    nuevo_precio = pedir_float("Nuevo precio: ")
                    nuevo_stock = pedir_entero("Nuevo stock: ")
                    actualizar_precio_stock(precios, stock, producto_id, nuevo_precio, nuevo_stock)
                    registrar_log(f"CATALOGO - producto_id {producto_id} actualizado "
                                  f"(precio={nuevo_precio}, stock={nuevo_stock}).")
                    print("Producto actualizado.")
            else:
                print("Opcion no reconocida.")

        elif opcion == "4":
            if not ventas_buffer:
                print("No hay ventas nuevas en esta sesion para guardar.")
            else:
                ok = guardar_ventas_csv(ventas_buffer, CSV_PATH)
                if ok:
                    print(f"{len(ventas_buffer)} venta(s) guardadas en '{CSV_PATH}'.")
                    ventas_buffer.clear()

        elif opcion == "5":
            df = leer_ventas_csv(CSV_PATH)
            calcular_metricas(df)

        elif opcion == "6":
            df = leer_ventas_csv(CSV_PATH)
            graficar_ingresos(df, guardar=False)

        elif opcion == "7":
            # RETO B: exportar grafico a PNG6
            df = leer_ventas_csv(CSV_PATH)
            graficar_ingresos(df, guardar=True, path=PNG_PATH)

        elif opcion == "0":
            if ventas_buffer:
                guardar_ventas_csv(ventas_buffer, CSV_PATH)
                print(f"{len(ventas_buffer)} venta(s) pendientes guardadas automaticamente.")
            print("Gracias por usar MiniTienda. Hasta pronto.")
            break  # rompe el bucle while y termina el programa


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")
        registrar_log(f"ERROR INESPERADO - {e}")
    finally:
        print("Sesion finalizada.")
