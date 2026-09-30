from book_manager.repositories.repositories import (
    RepositorioLibro, RepositorioGenero, RepositorioEditorial,
    RepositorioMoneda, RepositorioTipoCotizacion, RepositorioPrecio,
    RepositorioStock, RepositorioCotizacionDolar
)
from book_manager.services.services import (
    LibroService, GeneroService, EditorialService,
    MonedaService, TipoCotizacionService, PrecioService,
    StockService, CotizacionDolarService
)
from book_manager.ui.console import ConsoleUI

from book_manager.preload_data.preload_data import (
    cargar_monedas, cargar_tipos_cotizacion, cargar_generos,
    cargar_editoriales, cargar_precios, cargar_libros, cargar_stocks
)

def main(import_default_data: bool = True):
    print("Iniciando el sistema Book Manager...")

    repo_libro = RepositorioLibro()
    repo_genero = RepositorioGenero()
    repo_editorial = RepositorioEditorial()
    repo_moneda = RepositorioMoneda()
    repo_tipo = RepositorioTipoCotizacion()
    repo_precio = RepositorioPrecio()
    repo_stock = RepositorioStock()
    repo_cotizacion = RepositorioCotizacionDolar()

    if import_default_data:
        print("Cargando datos por defecto desde archivos CSV...")
        # Armamos los diccionarios con preload_data
        dic_monedas = cargar_monedas()
        dic_tipos = cargar_tipos_cotizacion()
        dic_generos = cargar_generos()
        dic_editoriales = cargar_editoriales()
        dic_precios = cargar_precios(dic_monedas, dic_tipos)
        dic_libros = cargar_libros(dic_generos, dic_editoriales, dic_precios)
        dic_stocks = cargar_stocks(dic_libros)

        # Insertamos las entidades armadas directamente en sus repositorios
        for m in dic_monedas.values(): repo_moneda.crear(m)
        for t in dic_tipos.values(): repo_tipo.crear(t)
        for g in dic_generos.values(): repo_genero.crear(g)
        for e in dic_editoriales.values(): repo_editorial.crear(e)
        for p in dic_precios.values(): repo_precio.crear(p)
        for l in dic_libros.values(): repo_libro.crear(l)
        for s in dic_stocks.values(): repo_stock.crear(s)
        print("Datos iniciales cargados correctamente.")

    servicios = {
        'genero': GeneroService(repo_genero),
        'editorial': EditorialService(repo_editorial),
        'moneda': MonedaService(repo_moneda),
        'tipo_cotizacion': TipoCotizacionService(repo_tipo),
        'precio': PrecioService(repo_precio, repo_moneda, repo_tipo),
        'libro': LibroService(repo_libro, repo_genero, repo_editorial, repo_precio),
        'stock': StockService(repo_stock, repo_libro),
        'cotizacion': CotizacionDolarService(repo_cotizacion, repo_moneda, repo_tipo)
    }

    ui = ConsoleUI(servicios)
    
    ui.iniciar()

if __name__ == "__main__":
    main(import_default_data=True)
