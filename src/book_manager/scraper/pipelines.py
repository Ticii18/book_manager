"""Validación de los resultados extraídos por el scraper."""

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class CuspidePipeline:
    """Valida los libros y descarta resultados duplicados."""

    def open_spider(self, spider):
        """Inicializa el registro de productos procesados."""
        self.productos_procesados = set()

    def process_item(self, item, spider):
        """Comprueba los datos mínimos y evita duplicados."""
        datos = ItemAdapter(item)

        if not datos.get("id_libro"):
            raise DropItem("El resultado no pertenece al catálogo.")

        if not datos.get("titulo_cuspide"):
            raise DropItem("El resultado no tiene título.")

        if not datos.get("url_producto"):
            raise DropItem("El resultado no tiene URL de producto.")

        clave = (
            datos.get("id_libro"),
            datos.get("url_producto"),
        )

        if clave in self.productos_procesados:
            raise DropItem("El producto ya fue procesado.")

        self.productos_procesados.add(clave)
        return item
