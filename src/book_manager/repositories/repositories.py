from abc import ABC, abstractmethod
from datetime import date
from typing import Generic, List, Optional, TypeVar

from book_manager.entities.entities import (
    CotizacionDolar,
    EntidadBase,
    Editorial,
    Genero,
    Libro,
    Moneda,
    Precio,
    Stock,
    TipoCotizacion,
)

T = TypeVar("T", bound=EntidadBase)


class IRepositorio(ABC, Generic[T]):

    @abstractmethod
    def crear(self, entidad: T) -> T:
        pass

    @abstractmethod
    def leer_por_id(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    def leer_todos(self) -> List[T]:
        pass

    @abstractmethod
    def actualizar(self, entidad: T) -> T:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass


class RepositorioGenero(IRepositorio[Genero]):

    def __init__(self) -> None:
        self.__generos: List[Genero] = []

    def crear(self, genero: Genero) -> Genero:

        if self.leer_por_id(genero.id) is not None:
            raise ValueError("Ya existe un género con ese ID")

        self.__generos.append(genero)
        return genero

    def leer_por_id(self, id: int) -> Optional[Genero]:

        for genero in self.__generos:
            if genero.id == id:
                return genero

        return None

    def leer_todos(self) -> List[Genero]:
        return self.__generos.copy()

    def actualizar(self, genero: Genero) -> Genero:
        for indice, genero_actual in enumerate(self.__generos):
            if genero_actual.id == genero.id:
                self.__generos[indice] = genero
                return genero
        raise ValueError("No existe un género con ese ID")

    def eliminar(self, id: int) -> bool:
        for indice, genero in enumerate(self.__generos):
            if genero.id == id:
                del self.__generos[indice]
                return True

        return False


class RepositorioEditorial(IRepositorio[Editorial]):

    def __init__(self) -> None:
        self.__editoriales: List[Editorial] = []

    def crear(self, editorial: Editorial) -> Editorial:
        if self.leer_por_id(editorial.id) is not None:
            raise ValueError("Ya existe una editorial con ese ID.")

        self.__editoriales.append(editorial)
        return editorial

    def leer_por_id(self, id: int) -> Optional[Editorial]:
        for editorial in self.__editoriales:
            if editorial.id == id:
                return editorial

        return None

    def leer_todos(self) -> List[Editorial]:
        return self.__editoriales.copy()

    def actualizar(self, editorial: Editorial) -> Editorial:
        for indice, editorial_actual in enumerate(self.__editoriales):
            if editorial_actual.id == editorial.id:
                self.__editoriales[indice] = editorial
                return editorial

        raise ValueError("No existe una editorial con ese ID.")

    def eliminar(self, id: int) -> bool:
        for indice, editorial in enumerate(self.__editoriales):
            if editorial.id == id:
                del self.__editoriales[indice]
                return True

        return False


class RepositorioMoneda(IRepositorio[Moneda]):

    def __init__(self) -> None:
        self.__monedas: List[Moneda] = []

    def crear(self, moneda: Moneda) -> Moneda:
        if self.leer_por_id(moneda.id) is not None:
            raise ValueError("Ya existe una moneda con ese ID.")

        self.__monedas.append(moneda)
        return moneda

    def leer_por_id(self, id: int) -> Optional[Moneda]:
        for moneda in self.__monedas:
            if moneda.id == id:
                return moneda

        return None

    def leer_todos(self) -> List[Moneda]:
        return self.__monedas.copy()

    def actualizar(self, moneda: Moneda) -> Moneda:
        for indice, moneda_actual in enumerate(self.__monedas):
            if moneda_actual.id == moneda.id:
                self.__monedas[indice] = moneda
                return moneda

        raise ValueError("No existe una moneda con ese ID.")

    def eliminar(self, id: int) -> bool:
        for indice, moneda in enumerate(self.__monedas):
            if moneda.id == id:
                del self.__monedas[indice]
                return True

        return False


class RepositorioTipoCotizacion(IRepositorio[TipoCotizacion]):
    def __init__(self) -> None:
        self.__tipos: List[TipoCotizacion] = []

    def crear(self, tipo: TipoCotizacion) -> TipoCotizacion:
        if self.leer_por_id(tipo.id) is not None:
            raise ValueError("Ya existe un tipo de cotización con ese ID.")

        self.__tipos.append(tipo)
        return tipo

    def leer_por_id(self, id: int) -> Optional[TipoCotizacion]:
        for tipo in self.__tipos:
            if tipo.id == id:
                return tipo

        return None

    def leer_todos(self) -> List[TipoCotizacion]:
        return self.__tipos.copy()

    def actualizar(self, tipo: TipoCotizacion) -> TipoCotizacion:
        for indice, tipo_actual in enumerate(self.__tipos):
            if tipo_actual.id == tipo.id:
                self.__tipos[indice] = tipo
                return tipo

        raise ValueError("No existe un tipo de cotización con ese ID.")

    def eliminar(self, id: int) -> bool:
        for indice, tipo in enumerate(self.__tipos):
            if tipo.id == id:
                del self.__tipos[indice]
                return True

        return False


class RepositorioPrecio(IRepositorio[Precio]):

    def __init__(self) -> None:
        self.__precios: List[Precio] = []

    def crear(self, precio: Precio) -> Precio:
        if self.leer_por_id(precio.id) is not None:
            raise ValueError("Ya existe un precio con ese ID.")

        self.__precios.append(precio)
        return precio

    def leer_por_id(self, id: int) -> Optional[Precio]:
        for precio in self.__precios:
            if precio.id == id:
                return precio

        return None

    def leer_todos(self) -> List[Precio]:
        return self.__precios.copy()

    def actualizar(self, precio: Precio) -> Precio:
        for indice, precio_actual in enumerate(self.__precios):
            if precio_actual.id == precio.id:
                self.__precios[indice] = precio
                return precio

        raise ValueError("No existe un precio con ese ID.")

    def eliminar(self, id: int) -> bool:
        for indice, precio in enumerate(self.__precios):
            if precio.id == id:
                del self.__precios[indice]
                return True

        return False


class RepositorioLibro(IRepositorio[Libro]):

    def __init__(self) -> None:
        self.__libros: List[Libro] = []

    def crear(self, libro: Libro) -> Libro:
        if self.leer_por_id(libro.id) is not None:
            raise ValueError("Ya existe un libro con ese ID.")

        self.__libros.append(libro)
        return libro

    def leer_por_id(self, id: int) -> Optional[Libro]:
        for libro in self.__libros:
            if libro.id == id:
                return libro

        return None

    def leer_todos(self) -> List[Libro]:
        return self.__libros.copy()

    def actualizar(self, libro: Libro) -> Libro:
        for indice, libro_actual in enumerate(self.__libros):
            if libro_actual.id == libro.id:
                self.__libros[indice] = libro
                return libro

        raise ValueError("No existe un libro con ese ID.")

    def eliminar(self, id: int) -> bool:
        for indice, libro in enumerate(self.__libros):
            if libro.id == id:
                del self.__libros[indice]
                return True

        return False


class RepositorioStock(IRepositorio[Stock]):

    def __init__(self) -> None:
        self.__stocks: List[Stock] = []

    def crear(self, stock: Stock) -> Stock:
        if self.leer_por_libro(stock.libro.id) is not None:
            raise ValueError("Ya existe stock para ese libro.")

        self.__stocks.append(stock)
        return stock

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        for stock in self.__stocks:
            if stock.libro.id == libro_id:
                return stock

        return None

    def actualizar(self, stock: Stock) -> Stock:
        for indice, stock_actual in enumerate(self.__stocks):
            if stock_actual.libro.id == stock.libro.id:
                self.__stocks[indice] = stock
                return stock

        raise ValueError("No existe stock para ese libro.")

    def eliminar(self, libro_id: int) -> bool:
        for indice, stock in enumerate(self.__stocks):
            if stock.libro.id == libro_id:
                del self.__stocks[indice]
                return True

        return False


class RepositorioCotizacionDolar(IRepositorio[CotizacionDolar]):
    """Repositorio para gestionar cotizaciones del dólar."""

    def __init__(self) -> None:
        self.__cotizaciones: List[CotizacionDolar] = []

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:

        existente = self.leer_por_tipo_y_fecha(
            cotizacion.tipo_cotizacion.id, cotizacion.fecha
        )

        if existente is not None:
            raise ValueError("Ya existe una cotización para ese tipo y fecha.")

        self.__cotizaciones.append(cotizacion)
        return cotizacion

    def leer_por_tipo_y_fecha(
        self, tipo_id: int, fecha: date
    ) -> Optional[CotizacionDolar]:

        for cotizacion in self.__cotizaciones:
            if cotizacion.tipo_cotizacion.id == tipo_id and cotizacion.fecha == fecha:
                return cotizacion

        return None

    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:

        return [
            cotizacion
            for cotizacion in self.__cotizaciones
            if cotizacion.tipo_cotizacion.id == tipo_id
        ]

    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:

        existente = self.leer_por_tipo_y_fecha(
            cotizacion.tipo_cotizacion.id, cotizacion.fecha
        )

        if existente is None:
            raise ValueError("No existe una cotización para ese tipo y fecha.")

        indice = self.__cotizaciones.index(existente)
        self.__cotizaciones[indice] = cotizacion

        return cotizacion

    def eliminar(self, tipo_id: int, fecha: date) -> bool:

        cotizacion = self.leer_por_tipo_y_fecha(tipo_id, fecha)

        if cotizacion is None:
            return False

        self.__cotizaciones.remove(cotizacion)
        return True
