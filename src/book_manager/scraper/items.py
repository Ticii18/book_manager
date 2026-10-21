"""Define los datos que se obtienen de los libros de Cúspide."""

import scrapy


class CuspideLibroItem(scrapy.Item):
    """Contiene la información extraída de un libro."""

    id_libro = scrapy.Field()
    isbn = scrapy.Field()
    titulo_catalogo = scrapy.Field()
    titulo_cuspide = scrapy.Field()
    autor = scrapy.Field()
    url_producto = scrapy.Field()
    precio = scrapy.Field()
    url_imagen = scrapy.Field()
    formas_pago = scrapy.Field()
    descripcion_detallada = scrapy.Field()
