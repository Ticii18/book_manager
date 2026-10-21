"""Busca en Cúspide los libros que ya existen en el catálogo."""

import csv
from pathlib import Path
from urllib.parse import urlencode, urljoin

import scrapy

from book_manager.scraper.items import CuspideLibroItem
from book_manager.scraper.loaders import CuspideLibroLoader


class CuspideSpider(scrapy.Spider):
    """Busca cada libro del catálogo y revisa hasta diez resultados."""

    name = "cuspide"
    allowed_domains = ["cuspide.com", "www.cuspide.com"]
    max_resultados = 10

    def start(self):
        """Genera una búsqueda por cada libro del catálogo propio."""
        ruta_csv = (
            Path(__file__).resolve().parents[2]
            / "migrations"
            / "csv"
            / "libros.csv"
        )

        with ruta_csv.open(
            encoding="utf-8-sig",
            newline="",
        ) as archivo:
            lector = csv.DictReader(archivo)

            for libro in lector:
                titulo = (libro.get("titulo") or "").strip()

                if not titulo:
                    continue

                parametros = urlencode({
                    "s": titulo,
                    "post_type": "product",
                })

                yield scrapy.Request(
                    url=f"https://cuspide.com/?{parametros}",
                    callback=self.parse_busqueda,
                    meta={
                        "id_libro": libro.get("id_libro", "").strip(),
                        "isbn": libro.get("isbn", "").strip(),
                        "titulo_catalogo": titulo,
                        "autor": libro.get("autor", "").strip(),
                    },
                )

    def parse_busqueda(self, response):
        """Procesa como máximo diez resultados de cada búsqueda."""
        productos = response.css(
            "li.product, .products .product, .product-item"
        )

        for producto in productos[:self.max_resultados]:
            url = producto.css(
                "a.woocommerce-LoopProduct-link::attr(href), "
                "a.woocommerce-loop-product__link::attr(href), "
                "a::attr(href)"
            ).get()

            titulo = producto.css(
                ".woocommerce-loop-product__title::text, "
                "h2::text, h3::text, .product-title::text"
            ).get()

            imagen = producto.css(
                "img::attr(data-src), img::attr(src)"
            ).get()

            if not url:
                continue

            yield response.follow(
                url,
                callback=self.parse_producto,
                meta={
                    **response.meta,
                    "titulo_resultado": (titulo or "").strip(),
                    "imagen_resultado": (
                        urljoin(response.url, imagen) if imagen else None
                    ),
                },
            )

    def parse_producto(self, response):
        """Extrae precio, imagen, formas de pago y descripción."""
        titulo_catalogo = response.meta["titulo_catalogo"]
        titulo_producto = response.css(
            "h1.product_title::text, h1::text"
        ).get() or response.meta.get("titulo_resultado", "")

        # Comprobamos que el producto coincida con el catálogo.
        normalizar = lambda texto: " ".join(texto.casefold().split())
        titulo_busqueda = normalizar(titulo_catalogo)
        titulo_encontrado = normalizar(titulo_producto)

        isbn = response.meta.get("isbn", "").replace("-", "").strip()
        texto_pagina = "".join(response.css("body ::text").getall())
        isbn_encontrado = bool(
            isbn and isbn in texto_pagina.replace("-", "").replace(" ", "")
        )
        titulo_coincide = (
            titulo_busqueda in titulo_encontrado
            or titulo_encontrado in titulo_busqueda
        )

        if not (isbn_encontrado or titulo_coincide):
            return

        loader = CuspideLibroLoader(
            item=CuspideLibroItem(),
            response=response,
        )

        loader.add_value("id_libro", response.meta["id_libro"])
        loader.add_value("isbn", response.meta.get("isbn"))
        loader.add_value("titulo_catalogo", titulo_catalogo)
        loader.add_value("autor", response.meta.get("autor"))
        loader.add_value("titulo_cuspide", titulo_producto)
        loader.add_value("url_producto", response.url)

        loader.add_css(
            "precio",
            ".summary .price, p.price, .product .price",
        )
        loader.add_css(
            "url_imagen",
            ".woocommerce-product-gallery img::attr(data-src), "
            ".woocommerce-product-gallery img::attr(src), "
            "img.wp-post-image::attr(src)",
        )
        loader.add_css(
            "descripcion_detallada",
            "#tab-description ::text, "
            ".woocommerce-Tabs-panel--description ::text, "
            ".woocommerce-product-details__short-description ::text",
        )

        # Buscamos información visible relacionada con cuotas y pagos.
        formas_pago = response.css(
            "[class*='cuota'] ::text, "
            "[class*='payment'] ::text, "
            "[class*='pago'] ::text"
        ).getall()
        loader.add_value("formas_pago", formas_pago)

        # Usamos la imagen del resultado si la ficha no proporciona otra.
        if not loader.get_collected_values("url_imagen"):
            loader.add_value(
                "url_imagen",
                response.meta.get("imagen_resultado"),
            )

        yield loader.load_item()
