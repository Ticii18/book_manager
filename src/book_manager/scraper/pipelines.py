"""Valida los productos y genera el reporte de alertas al terminar el scraper."""

import csv

from scrapy.exceptions import DropItem

from book_manager.scraper.alertas import generar_alertas


class CuspidePipeline:
    """Descarta items inválidos, evita duplicados y genera un CSV por ejecución."""

    @classmethod
    def from_crawler(cls, crawler):
        """Guarda el crawler para acceder al spider sin firmas obsoletas."""
        pipeline = cls()
        pipeline.crawler = crawler
        return pipeline

    def open_spider(self):
        """Inicializa las colecciones de la ejecución."""
        self.productos = []
        self.productos_procesados = set()
        self.productos_sin_formas_pago = 0

    def process_item(self, item):
        """Valida y almacena cada libro extraído."""
        if not item.get("id_libro"):
            raise DropItem("El producto no está vinculado a un libro del catálogo.")

        if not item.get("titulo_cuspide") or not item.get("url_producto"):
            raise DropItem("El producto no tiene título o URL.")

        if not item.get("precio"):
            raise DropItem("El producto no tiene un precio para comparar.")

        clave = (str(item.get("id_libro")), str(item.get("url_producto")))
        if clave in self.productos_procesados:
            raise DropItem("Producto duplicado.")

        self.productos_procesados.add(clave)
        self.productos.append(dict(item))

        if not item.get("formas_pago"):
            self.productos_sin_formas_pago += 1

        return item

    def close_spider(self):
        """Genera el CSV incluso si no se obtuvo ningún producto válido."""
        spider = self.crawler.spider
        ruta = generar_alertas(
            resultados_web=self.productos,
            diferencia_maxima=spider.diferencia_maxima,
        )

        with ruta.open(encoding="utf-8-sig", newline="") as archivo:
            cantidad_alertas = max(sum(1 for _ in csv.DictReader(archivo)), 0)

        spider.logger.info(
            "Reporte de alertas generado: %s", ruta
        )
        spider.logger.info(
            "Productos con precio procesados: %s; alertas generadas: %s",
            len(self.productos),
            cantidad_alertas,
        )

        if not self.productos:
            spider.logger.warning(
                "No se obtuvieron productos con precio. El CSV está generado, "
                "pero no confirma que no existan diferencias."
            )

        if self.productos_sin_formas_pago:
            spider.logger.warning(
                "No se pudieron verificar las formas de pago de %s producto(s).",
                self.productos_sin_formas_pago,
            )

