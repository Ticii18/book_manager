import csv
from datetime import datetime
import json
import os
from pathlib import Path
from typing import Any
import urllib.parse
import urllib.request
from dotenv import load_dotenv
import pandas as pd

from book_manager.scraper.alertas import cargar_precios_internos, _parsear_precio_web

# Carpeta donde se guardarán los reportes generados
CARPETA_REPORTES = Path(__file__).resolve().parent

# Cargamos las variables de entorno desde el archivo .env
load_dotenv()
URL_API_CUSPIDE = os.getenv("API_PRODUCTOS_CUSPIDE")


def consultar_precios_cuspide(precios_internos: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Consulta la API pública de Cúspide para buscar los precios reales de los libros.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }
    resultados = []

    for id_libro, datos in precios_internos.items():
        titulo = datos.get("titulo", "").strip()
        if not titulo:
            continue

        parametros = urllib.parse.urlencode({"search": titulo, "per_page": 1})
        url = f"{URL_API_CUSPIDE}?{parametros}"

        try:
            peticion = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(peticion, timeout=10) as respuesta:
                if respuesta.status == 200:
                    productos = json.loads(respuesta.read().decode("utf-8"))
                    if productos and isinstance(productos, list):
                        producto = productos[0]
                        precios = producto.get("prices", {})
                        valor_raw = precios.get("price")
                        unidad_menor = int(precios.get("currency_minor_unit", 2))
                        if valor_raw is not None:
                            # La API devuelve el precio en centavos, dividimos por 10^2
                            precio_real = float(valor_raw) / (10 ** unidad_menor)
                            resultados.append({
                                "id_libro": id_libro,
                                "precio": str(precio_real),
                                "url_producto": producto.get("permalink", ""),
                            })
        except Exception as error:
            print(f"Aviso: No se pudo obtener el precio de '{titulo}' desde Cúspide: {error}")

    return resultados


def generar_reporte_excel(
    resultados_web: list[dict[str, Any]] | None = None,
    ruta_salida: str | Path | None = None,
) -> Path:
    """
    Genera un archivo Excel (.xlsx) con la comparación de precios.
    Si no se pasan 'resultados_web', consulta automáticamente la API real de Cúspide.

    Parámetros:
        resultados_web (list, opcional): Lista de diccionarios con los datos extraídos
            por el scraper. Si es None, consulta la API pública de Cúspide en vivo.
        ruta_salida (str o Path, opcional): Ruta personalizada donde guardar el Excel.

    Retorna:
        Path: Ruta al archivo Excel generado.
    """
    # 1. Cargamos los precios internos de nuestro catálogo
    precios_internos = cargar_precios_internos()

    # 2. Si no nos pasaron resultados de scraping previos, consultamos la API de Cúspide en vivo
    if resultados_web is None:
        print("Consultando precios en la API de Cúspide en tiempo real...")
        resultados_web = consultar_precios_cuspide(precios_internos)

    # Fecha y hora actual del momento de la extracción / generación
    fecha_extraccion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    filas = []

    # 3. Procesamos cada resultado web obtenido
    for item in resultados_web:
        id_libro = str(item.get("id_libro", "")).strip()

        # Buscamos si el libro existe en nuestro catálogo interno
        libro_interno = precios_internos.get(id_libro)

        # Limpiamos y convertimos el precio web a número
        precio_web_num = _parsear_precio_web(item.get("precio"))

        # Si encontramos el libro y tiene precio web válido, calculamos
        if libro_interno is not None and precio_web_num is not None:
            titulo = libro_interno["titulo"]
            precio_interno_num = float(libro_interno["precio_interno"])
            precio_web_val = float(precio_web_num)

            # Calculamos la diferencia entre ambos precios
            diferencia = round(abs(precio_web_val - precio_interno_num), 2)

            # Agregamos la fila con los nombres pedidos por la consigna
            filas.append(
                {
                    "Libro": titulo,
                    "Precio interno": precio_interno_num,
                    "Precio web": precio_web_val,
                    "Diferencia": diferencia,
                    "Fecha de extracción": fecha_extraccion,
                }
            )

    # 4. Creamos el DataFrame de pandas con las columnas solicitadas
    columnas = [
        "Libro",
        "Precio interno",
        "Precio web",
        "Diferencia",
        "Fecha de extracción",
    ]

    if filas:
        df = pd.DataFrame(filas)
    else:
        df = pd.DataFrame(columns=columnas)

    # 5. Determinamos la ruta final del archivo Excel
    if ruta_salida is None:
        CARPETA_REPORTES.mkdir(parents=True, exist_ok=True)
        marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_archivo = CARPETA_REPORTES / f"reporte_precios_{marca_tiempo}.xlsx"
    else:
        ruta_archivo = Path(ruta_salida)
        ruta_archivo.parent.mkdir(parents=True, exist_ok=True)

    # 6. Guardamos en formato Excel (.xlsx) usando openpyxl
    df.to_excel(ruta_archivo, index=False, engine="openpyxl")
    print(f"Reporte en Excel generado exitosamente: {ruta_archivo}")

    return ruta_archivo


def convertir_csv_alertas_a_excel(
    ruta_csv: str | Path,
    ruta_salida: str | Path | None = None,
) -> Path:
    """
    Función auxiliar: Lee un archivo CSV de alertas (generado en el Ejercicio 4)
    y lo convierte a un archivo Excel con el formato requerido en el Ejercicio 5.
    """
    ruta_csv = Path(ruta_csv)
    if not ruta_csv.exists():
        raise FileNotFoundError(f"No se encontró el archivo CSV: {ruta_csv}")

    filas = []
    fecha_extraccion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with ruta_csv.open(encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            try:
                filas.append(
                    {
                        "Libro": fila.get("titulo", ""),
                        "Precio interno": float(fila.get("precio_interno_ARS", 0)),
                        "Precio web": float(fila.get("precio_web_ARS", 0)),
                        "Diferencia": float(fila.get("diferencia_ARS", 0)),
                        "Fecha de extracción": fecha_extraccion,
                    }
                )
            except ValueError:
                continue

    columnas = [
        "Libro",
        "Precio interno",
        "Precio web",
        "Diferencia",
        "Fecha de extracción",
    ]
    df = pd.DataFrame(filas, columns=columnas)

    if ruta_salida is None:
        CARPETA_REPORTES.mkdir(parents=True, exist_ok=True)
        marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_archivo = CARPETA_REPORTES / f"reporte_desde_alertas_{marca_tiempo}.xlsx"
    else:
        ruta_archivo = Path(ruta_salida)
        ruta_archivo.parent.mkdir(parents=True, exist_ok=True)

    df.to_excel(ruta_archivo, index=False, engine="openpyxl")
    print(f"Reporte convertido a Excel exitosamente: {ruta_archivo}")

    return ruta_archivo
