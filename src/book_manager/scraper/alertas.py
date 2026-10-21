"""Compara precios internos en ARS con precios obtenidos de la web y genera alertas CSV."""

import csv
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

CARPETA_PROYECTO = Path(__file__).resolve().parents[1]
CARPETA_CSV = CARPETA_PROYECTO / "migrations" / "csv"
CARPETA_REPORTES = CARPETA_PROYECTO / "reportes"

CAMPOS_REPORTE = [
    "id_libro",
    "titulo",
    "precio_interno_ARS",
    "precio_web_ARS",
    "diferencia_ARS",
    "url_producto",
]


def _leer_csv(ruta: Path) -> list[dict[str, str]]:
    """Lee un CSV del catálogo ignorando columnas vacías al final."""
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo requerido: {ruta}")

    with ruta.open(encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        return [
            {
                clave: (valor or "").strip()
                for clave, valor in fila.items()
                if clave and valor is not None
            }
            for fila in lector
        ]


def _decimal_interno(valor: Any) -> Decimal | None:
    """Convierte un valor numérico del catálogo a Decimal."""
    if valor is None or str(valor).strip() == "":
        return None
    try:
        return Decimal(str(valor).strip().replace(",", "."))
    except InvalidOperation:
        return None


def _parsear_precio_web(valor: Any) -> Decimal | None:
    """Interpreta precios web argentinos, por ejemplo '$ 20.000,00'."""
    if valor is None:
        return None

    texto = re.sub(r"[^0-9,.\-]", "", str(valor).strip())
    if not texto or texto in {"-", ".", ","}:
        return None

    if "," in texto and "." in texto:
        # El separador que aparece último se toma como separador decimal.
        if texto.rfind(",") > texto.rfind("."):
            texto = texto.replace(".", "").replace(",", ".")
        else:
            texto = texto.replace(",", "")
    elif "," in texto:
        partes = texto.split(",")
        if len(partes[-1]) in (1, 2):
            texto = "".join(partes[:-1]) + "." + partes[-1]
        else:
            texto = "".join(partes)
    elif texto.count(".") > 1:
        partes = texto.split(".")
        if len(partes[-1]) in (1, 2):
            texto = "".join(partes[:-1]) + "." + partes[-1]
        else:
            texto = "".join(partes)
    elif "." in texto:
        # En formato argentino, un punto seguido de tres cifras suele
        # ser separador de miles: 20.000.
        parte_decimal = texto.rsplit(".", maxsplit=1)[-1]
        if len(parte_decimal) == 3:
            texto = texto.replace(".", "")

    try:
        precio = Decimal(texto)
    except InvalidOperation:
        return None

    return precio if precio >= 0 else None


def cargar_precios_internos() -> dict[str, dict[str, Any]]:
    """Devuelve los libros que tienen precio interno expresado en ARS."""
    libros = _leer_csv(CARPETA_CSV / "libros.csv")
    precios = _leer_csv(CARPETA_CSV / "Precio.csv")
    monedas = _leer_csv(CARPETA_CSV / "moneda.csv")

    simbolos = {
        fila.get("id_moneda", ""): fila.get("simbolo", "").upper()
        for fila in monedas
    }

    precios_por_id: dict[str, tuple[Decimal, str]] = {}
    for fila in precios:
        id_precio = fila.get("id_precio", "")
        valor = _decimal_interno(fila.get("valor"))
        simbolo = simbolos.get(fila.get("id_moneda", ""), "")
        if id_precio and valor is not None:
            precios_por_id[id_precio] = (valor, simbolo)

    resultado: dict[str, dict[str, Any]] = {}
    for libro in libros:
        id_libro = libro.get("id_libro", "")
        id_precio = libro.get("precio", "")
        precio_registrado = precios_por_id.get(id_precio)

        if not id_libro or precio_registrado is None:
            continue

        precio, simbolo = precio_registrado
        # No se comparan monedas distintas como si fueran ARS.
        if simbolo != "ARS":
            continue

        resultado[id_libro] = {
            "titulo": libro.get("titulo", ""),
            "precio_interno": precio,
            "moneda": "ARS",
        }

    return resultado


def generar_alertas(
    resultados_web: list[dict[str, Any]],
    diferencia_maxima: float | int | Decimal,
) -> Path:
    """Genera siempre un CSV; solo incluye productos que superan el límite."""
    limite = _decimal_interno(diferencia_maxima)
    if limite is None or limite < 0:
        raise ValueError("La diferencia máxima debe ser un número no negativo.")

    precios_internos = cargar_precios_internos()
    CARPETA_REPORTES.mkdir(parents=True, exist_ok=True)

    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    ruta_reporte = CARPETA_REPORTES / f"alertas_precios_{marca_tiempo}.csv"

    with ruta_reporte.open("w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_REPORTE)
        escritor.writeheader()

        for producto in resultados_web:
            id_libro = str(producto.get("id_libro", "")).strip()
            interno = precios_internos.get(id_libro)
            precio_web = _parsear_precio_web(producto.get("precio"))

            if interno is None or precio_web is None:
                continue

            precio_interno = interno["precio_interno"]
            diferencia = abs(precio_web - precio_interno)

            if diferencia > limite:
                escritor.writerow(
                    {
                        "id_libro": id_libro,
                        "titulo": interno["titulo"],
                        "precio_interno_ARS": f"{precio_interno:.2f}",
                        "precio_web_ARS": f"{precio_web:.2f}",
                        "diferencia_ARS": f"{diferencia:.2f}",
                        "url_producto": str(producto.get("url_producto", "")).strip(),
                    }
                )

    return ruta_reporte

