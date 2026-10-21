"""Busca los libros del catálogo propio mediante el catálogo público de Cúspide."""

import csv
import json
import re
from decimal import Decimal, InvalidOperation
from html import unescape
from pathlib import Path
from urllib.parse import urlencode

import scrapy

from book_manager.scraper.items import CuspideLibroItem
from book_manager.scraper.loaders import CuspideLibroLoader


API_PRODUCTOS = "https://cuspide.com/wp-json/wc/store/v1/products"


def _normalizar(texto: str) -> str:
    """Normaliza espacios y mayúsculas para comparar títulos."""
    return " ".join((texto or "").casefold().split())


def _texto_plano(texto: str) -> str:
    """Quita etiquetas HTML y normaliza entidades y espacios."""
    return " ".join(re.sub(r"<[^>]+>", " ", unescape(texto or "")).split())


def _precio_api(producto: dict) -> str | None:
    """Convierte el precio de menor unidad de la API a unidades de moneda."""
    precios = producto.get("prices") or {}
    moneda = (precios.get("currency_code") or "").upper()
    valor = precios.get("price")
    unidad = precios.get("currency_minor_unit", 2)

    if valor is None or moneda != "ARS":
        return None

    try:
        unidad = int(unidad)
        importe = Decimal(str(valor)) / (Decimal(10) ** unidad)
    except (InvalidOperation, ValueError, TypeError):
        return None

    return f"{importe:.{unidad}f}"


class CuspideSpider(scrapy.Spider):
    """Busca hasta diez resultados por título del catálogo interno."""

    name = "cuspide"
    allowed_domains = ["cuspide.com", "www.cuspide.com"]
    max_resultados = 10

    def __init__(self, diferencia_maxima=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if diferencia_maxima is None:
            raise ValueError(
                "Debés ingresar diferencia_maxima antes de ejecutar el scraper."
            )

        try:
            self.diferencia_maxima = float(
                str(diferencia_maxima).replace(",", ".")
            )
        except ValueError as error:
            raise ValueError("La diferencia máxima debe ser numérica.") from error

        if self.diferencia_maxima < 0:
            raise ValueError("La diferencia máxima no puede ser negativa.")

    async def start(self):
        """Genera una consulta pública por cada libro del catálogo interno."""
        ruta_csv = (
            Path(__file__).resolve().parents[2]
            / "migrations"
            / "csv"
            / "libros.csv"
        )

        with ruta_csv.open(encoding="utf-8-sig", newline="") as archivo:
            for libro in csv.DictReader(archivo):
                titulo = (libro.get("titulo") or "").strip()
                if not titulo:
                    continue

                parametros = urlencode(
                    {"search": titulo, "per_page": self.max_resultados}
                )
                yield scrapy.Request(
                    url=f"{API_PRODUCTOS}?{parametros}",
                    callback=self.parse_busqueda,
                    meta={
                        "id_libro": (libro.get("id_libro") or "").strip(),
                        "isbn": (libro.get("isbn") or "").strip(),
                        "titulo_catalogo": titulo,
                        "autor": (libro.get("autor") or "").strip(),
                        "handle_httpstatus_all": True,
                    },
                )

    def parse_busqueda(self, response):
        """Procesa como máximo diez productos devueltos por cada búsqueda."""
        if response.status != 200:
            self.logger.warning(
                "Cúspide no permitió consultar el catálogo público (HTTP %s) "
                "para el título '%s'. No se simularán precios.",
                response.status,
                response.meta.get("titulo_catalogo", ""),
            )
            return

        try:
            productos = json.loads(response.text)
        except json.JSONDecodeError:
            self.logger.warning(
                "La respuesta del catálogo no fue JSON válido para '%s'.",
                response.meta.get("titulo_catalogo", ""),
            )
            return

        if not isinstance(productos, list):
            self.logger.warning(
                "La API no devolvió una lista de productos para '%s'.",
                response.meta.get("titulo_catalogo", ""),
            )
            return

        titulo_catalogo = response.meta["titulo_catalogo"]
        titulo_busqueda = _normalizar(titulo_catalogo)
        isbn = re.sub(r"[^0-9Xx]", "", response.meta.get("isbn", ""))
        productos_buscados = productos[: self.max_resultados]

        for producto in productos_buscados:
            titulo_producto = (producto.get("name") or "").strip()
            url_producto = producto.get("permalink")
            sku = re.sub(r"[^0-9Xx]", "", str(producto.get("sku") or ""))
            titulo_normalizado = _normalizar(titulo_producto)

            coincide_titulo = bool(
                titulo_normalizado
                and (
                    titulo_busqueda in titulo_normalizado
                    or titulo_normalizado in titulo_busqueda
                )
            )
            coincide_isbn = bool(isbn and isbn in sku)

            if not url_producto or not (coincide_titulo or coincide_isbn):
                continue

            yield scrapy.Request(
                url=url_producto,
                callback=self.parse_producto,
                meta={
                    **response.meta,
                    "titulo_resultado": titulo_producto,
                    "api_producto": producto,
                    "handle_httpstatus_all": True,
                },
            )

    def parse_producto(self, response):
        """Combina datos de la API pública con los que estén disponibles en la ficha."""
        producto_api = response.meta.get("api_producto") or {}
        titulo_catalogo = response.meta["titulo_catalogo"]
        titulo_api = (producto_api.get("name") or "").strip()
        titulo_html = (
            response.css("h1.product_title::text, h1::text").get() or ""
        ).strip()
        titulo_producto = titulo_html or titulo_api or response.meta.get(
            "titulo_resultado", ""
        )

        texto_pagina = "".join(response.css("body ::text").getall())
        isbn = re.sub(r"[^0-9Xx]", "", response.meta.get("isbn", ""))
        sku = re.sub(r"[^0-9Xx]", "", str(producto_api.get("sku") or ""))
        isbn_encontrado = bool(isbn and (isbn in sku or isbn in re.sub(
            r"[^0-9Xx]", "", texto_pagina
        )))

        titulo_busqueda = _normalizar(titulo_catalogo)
        titulo_candidatos = [
            _normalizar(titulo_html),
            _normalizar(titulo_api),
            _normalizar(response.meta.get("titulo_resultado", "")),
        ]
        titulo_coincide = any(
            candidato
            and (
                titulo_busqueda in candidato
                or candidato in titulo_busqueda
            )
            for candidato in titulo_candidatos
        )

        if not (isbn_encontrado or titulo_coincide):
            return

        precios_api = _precio_api(producto_api)
        imagenes = producto_api.get("images") or []
        imagen_api = (
            imagenes[0].get("src")
            if imagenes and isinstance(imagenes[0], dict)
            else None
        )
        descripcion_api = _texto_plano(
            producto_api.get("description")
            or producto_api.get("short_description", "")
        )

        loader = CuspideLibroLoader(
            item=CuspideLibroItem(),
            response=response,
        )
        loader.add_value("id_libro", response.meta["id_libro"])
        loader.add_value("isbn", response.meta.get("isbn"))
        loader.add_value("titulo_catalogo", titulo_catalogo)
        loader.add_value("autor", response.meta.get("autor"))
        loader.add_value("titulo_cuspide", titulo_producto)
        loader.add_value("url_producto", producto_api.get("permalink") or response.url)

        # Si la ficha está accesible, se prioriza su dato; si no, se usa la API.
        loader.add_css(
            "precio",
            ".summary .price, p.price, .product .price",
        )
        loader.add_value("precio", precios_api)

        loader.add_css(
            "url_imagen",
            ".woocommerce-product-gallery img::attr(data-src), "
            ".woocommerce-product-gallery img::attr(src), "
            "img.wp-post-image::attr(src)",
        )
        loader.add_value("url_imagen", imagen_api)

        loader.add_css(
            "descripcion_detallada",
            "#tab-description ::text, "
            ".woocommerce-Tabs-panel--description ::text, "
            ".woocommerce-product-details__short-description ::text",
        )
        loader.add_value("descripcion_detallada", descripcion_api)

        formas_pago = []
        if response.status == 200:
            formas_pago = [
                " ".join(texto.split())
                for texto in response.css(
                    "[class*='cuota'] ::text, "
                    "[class*='payment'] ::text, "
                    "[class*='pago'] ::text"
                ).getall()
                if texto.strip()
            ]
        loader.add_value("formas_pago", formas_pago)

        if response.status == 403:
            self.logger.warning(
                "La ficha del producto respondió 403. Se usaron los datos "
                "públicos disponibles; las formas de pago no pudieron verificarse: %s",
                producto_api.get("permalink") or response.url,
            )

        yield loader.load_item()

