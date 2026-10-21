"""Procesadores para normalizar los datos obtenidos de Cúspide."""

import re

from itemloaders import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Identity


def limpiar_texto(valor):
    """Elimina espacios y saltos de línea innecesarios."""
    if not valor:
        return None
    return " ".join(valor.split())


def limpiar_precio(valor):
    """Normaliza el texto del precio sin alterar su importe."""
    return limpiar_texto(valor)


class CuspideLibroLoader(ItemLoader):
    """Organiza los datos extraídos de cada libro."""

    default_input_processor = MapCompose(limpiar_texto)
    default_output_processor = TakeFirst()

    precio_in = MapCompose(limpiar_precio)
    formas_pago_out = Identity()
