import csv
import os

from book_manager.entities.entities import (
    Moneda,
    TipoCotizacion,
    Genero,
    Editorial,
    Precio,
    Libro,
    Stock
)

CSV_BASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'migrations', 'csv')

def cargar_monedas() -> dict[int, Moneda]:
    """
    Lee el archivo moneda.csv y devuelve un diccionario donde la clave es el ID de la moneda
    y el valor es el objeto Moneda ya instanciado.
    """
    monedas = {}
    ruta_archivo = os.path.join(CSV_BASE_PATH, 'moneda.csv')
    
    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        # DictReader puede leer csv usando nombres de las columnas como claves de un diccionario
        lector = csv.DictReader(archivo)
        
        for fila in lector:
            id_moneda = int(fila['id_moneda'])
            nombre = fila['nombre']
            simbolo = fila['simbolo']
            
            nueva_moneda = Moneda(id_moneda=id_moneda, nombre=nombre, simbolo=simbolo)
            
            monedas[id_moneda] = nueva_moneda
            
    return monedas

def cargar_tipos_cotizacion() -> dict[int, TipoCotizacion]:
    """
    Lee el archivo tipo_cotizacion.csv y devuelve un diccionario de objetos TipoCotizacion.
    """
    tipos = {}
    ruta_archivo = os.path.join(CSV_BASE_PATH, 'tipo_cotizacion.csv')
    
    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        
        for fila in lector:
            id_tipo = int(fila['id_tipo_cotizacion'])
            nombre = fila['nombre']
            
            nuevo_tipo = TipoCotizacion(id_tipo_cotizacion=id_tipo, nombre=nombre)
            tipos[id_tipo] = nuevo_tipo
            
    return tipos

def cargar_generos() -> dict[int, Genero]:
    generos = {}
    ruta_archivo = os.path.join(CSV_BASE_PATH, 'generos.csv')
    
    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            id_genero = int(fila['id_genero'])
            nombre = fila['nombre']
            generos[id_genero] = Genero(id_genero=id_genero, nombre=nombre)
            
    return generos

def cargar_editoriales() -> dict[int, Editorial]:
    editoriales = {}
    ruta_archivo = os.path.join(CSV_BASE_PATH, 'editorial.csv')
    
    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            id_editorial = int(fila['id_editorial'])
            nombre = fila['nombre']
            editoriales[id_editorial] = Editorial(id_editorial=id_editorial, nombre=nombre)
            
    return editoriales

# === ENTIDADES DEPENDIENTES ===

def cargar_precios(monedas: dict[int, Moneda], tipos: dict[int, TipoCotizacion]) -> dict[int, Precio]:
    """
    Lee Precio.csv. Como el Precio depende de Moneda y TipoCotizacion, 
    esta función exige que le pasemos esos diccionarios ya armados como parámetros.
    """
    precios = {}
    ruta_archivo = os.path.join(CSV_BASE_PATH, 'Precio.csv')
    
    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        
        for fila in lector:
            id_precio = int(fila['id_precio'])
            valor = float(fila['valor'])
            
            id_moneda_foranea = int(fila['id_moneda'])
            id_tipo_foranea = int(fila['id_tipo_cotizacion'])
            
            objeto_moneda = monedas[id_moneda_foranea]
            objeto_tipo = tipos[id_tipo_foranea]
            
            nuevo_precio = Precio(
                id_precio=id_precio, 
                valor=valor, 
                moneda=objeto_moneda, 
                tipo_cotizacion=objeto_tipo
            )
            precios[id_precio] = nuevo_precio
            
    return precios

def cargar_libros(generos: dict[int, Genero], editoriales: dict[int, Editorial], precios: dict[int, Precio]) -> dict[int, Libro]:
    libros = {}
    ruta_archivo = os.path.join(CSV_BASE_PATH, 'libros.csv')
    
    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        
        for fila in lector:
            id_libro = int(fila['id_libro'])
            isbn = fila['isbn']
            titulo = fila['titulo']
            autor = fila['autor']
            
            id_genero_foranea = int(fila['genero'])
            id_editorial_foranea = int(fila['editorial'])
            id_precio_foranea = int(fila['precio'])
            
            objeto_genero = generos[id_genero_foranea]
            objeto_editorial = editoriales[id_editorial_foranea]
            objeto_precio = precios[id_precio_foranea]
            
            nuevo_libro = Libro(
                id_libro=id_libro, 
                isbn=isbn, 
                titulo=titulo, 
                autor=autor,
                genero=objeto_genero,
                editorial=objeto_editorial,
                precio=objeto_precio
            )
            libros[id_libro] = nuevo_libro
            
    return libros

def cargar_stocks(libros: dict[int, Libro]) -> dict[int, Stock]:
    stocks = {}
    ruta_archivo = os.path.join(CSV_BASE_PATH, 'stock.csv')
    
    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        
        for fila in lector:
            id_stock = int(fila['id_stock'])
            
            # validacion para que no falle al leer un " - " en stock, se puede arreglar modificando el csv simplemente agregando un 0
            cantidad_str = fila['cantidad']
            if cantidad_str == "-":
                cantidad = 0
            else:
                cantidad = int(cantidad_str)
                
            id_libro_foranea = int(fila['libro'])
            objeto_libro = libros[id_libro_foranea]
            
            nuevo_stock = Stock(
                id_stock=id_stock,
                libro=objeto_libro,
                cantidad=cantidad
            )
            stocks[id_stock] = nuevo_stock
            
    return stocks

