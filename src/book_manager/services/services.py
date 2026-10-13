"""Módulo de Servicios del sistema."""

from abc import ABC, abstractmethod
from datetime import date
from typing import Generic, List, Optional, TypeVar

from book_manager.entities.entities import (
    CotizacionDolar,
    Editorial,
    EntidadBase,
    Genero,
    Libro,
    Moneda,
    Precio,
    Stock,
    TipoCotizacion,
)
from book_manager.repositories.repositories import (
    IRepositorio,
    RepositorioCotizacionDolar,
    RepositorioEditorial,
    RepositorioGenero,
    RepositorioLibro,
    RepositorioMoneda,
    RepositorioPrecio,
    RepositorioStock,
    RepositorioTipoCotizacion,
)

T = TypeVar("T", bound=EntidadBase)


# Interfaces y Clases Base de Servicios

class IServicio(ABC, Generic[T]):
    """Interfaz base para servicios que gestionan entidades."""

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[T]:
        """Recupera una entidad por su ID."""
        pass

    @abstractmethod
    def obtener_todos(self) -> List[T]:
        """Recupera todas las entidades disponibles."""
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina una entidad por su ID."""
        pass


class ServicioBase(IServicio[T], Generic[T]):
    """Clase base reutilizable para operaciones CRUD."""

    def __init__(self, repositorio: IRepositorio[T]) -> None:
        self._repositorio = repositorio

    def obtener_por_id(self, id: int) -> Optional[T]:
        return self._repositorio.leer_por_id(id)

    def obtener_todos(self) -> List[T]:
        return self._repositorio.leer_todos()

    def eliminar(self, id: int) -> bool:
        return self._repositorio.eliminar(id)


# Servicios Específicos

class GeneroService(ServicioBase[Genero]):
    """lógica de negocio de los géneros."""

    def __init__(
        self,
        repositorio: RepositorioGenero,
        repositorio_libro: Optional[RepositorioLibro] = None,
    ) -> None:
        super().__init__(repositorio)
        self.__repositorio_libro = repositorio_libro

    def crear(self, id_genero: int, nombre: str) -> Genero:
        if not nombre.strip():
            raise ValueError("El nombre del género no puede estar vacío.")
        genero = Genero(id_genero, nombre)
        return self._repositorio.crear(genero)

    def actualizar(self, id_genero: int, nombre: str) -> Genero:
        if not nombre.strip():
            raise ValueError("El nombre del género no puede estar vacío.")
        genero = Genero(id_genero, nombre)
        return self._repositorio.actualizar(genero)

    def eliminar(self, id_genero: int) -> bool:
        #validación de no eliminar si hay libros usándolo
        if self.__repositorio_libro:
            libros = self.__repositorio_libro.leer_todos()
            if any(l.genero.id == id_genero for l in libros):
                raise ValueError(
                    f"No se puede eliminar el género con ID {id_genero}: está siendo utilizado por uno o más libros."
                )
        elif hasattr(self._repositorio, "tiene_libros_asociados") and self._repositorio.tiene_libros_asociados(id_genero):
            raise ValueError(
                f"No se puede eliminar el género con ID {id_genero}: está siendo utilizado por uno o más libros."
            )
        return super().eliminar(id_genero)


class EditorialService(ServicioBase[Editorial]):
    """lógica de negocio de las editoriales."""

    def __init__(
        self,
        repositorio: RepositorioEditorial,
        repositorio_libro: Optional[RepositorioLibro] = None,
    ) -> None:
        super().__init__(repositorio)
        self.__repositorio_libro = repositorio_libro

    def crear(self, id_editorial: int, nombre: str) -> Editorial:
        if not nombre.strip():
            raise ValueError("El nombre de la editorial no puede estar vacío.")
        editorial = Editorial(id_editorial, nombre)
        return self._repositorio.crear(editorial)

    def actualizar(self, id_editorial: int, nombre: str) -> Editorial:
        if not nombre.strip():
            raise ValueError("El nombre de la editorial no puede estar vacío.")
        editorial = Editorial(id_editorial, nombre)
        return self._repositorio.actualizar(editorial)

    def eliminar(self, id_editorial: int) -> bool:
        # Validación de integridad referencial: no eliminar si hay libros usándola
        if self.__repositorio_libro:
            libros = self.__repositorio_libro.leer_todos()
            if any(l.editorial.id == id_editorial for l in libros):
                raise ValueError(
                    f"No se puede eliminar la editorial con ID {id_editorial}: está siendo utilizada por uno o más libros."
                )
        elif hasattr(self._repositorio, "tiene_libros_asociados") and self._repositorio.tiene_libros_asociados(id_editorial):
            raise ValueError(
                f"No se puede eliminar la editorial con ID {id_editorial}: está siendo utilizada por uno o más libros."
            )
        return super().eliminar(id_editorial)


class MonedaService(ServicioBase[Moneda]):
    """lógica de negocio de las monedas."""

    def __init__(self, repositorio: RepositorioMoneda) -> None:
        super().__init__(repositorio)

    def crear(self, id_moneda: int, nombre: str, simbolo: str) -> Moneda:
        if not nombre.strip():
            raise ValueError("El nombre de la moneda no puede estar vacío.")
        if not simbolo.strip():
            raise ValueError("El símbolo de la moneda no puede estar vacío.")
        moneda = Moneda(id_moneda, nombre, simbolo)
        return self._repositorio.crear(moneda)

    def actualizar(self, id_moneda: int, nombre: str, simbolo: str) -> Moneda:
        if not nombre.strip():
            raise ValueError("El nombre de la moneda no puede estar vacío.")
        if not simbolo.strip():
            raise ValueError("El símbolo de la moneda no puede estar vacío.")
        moneda = Moneda(id_moneda, nombre, simbolo)
        return self._repositorio.actualizar(moneda)


class TipoCotizacionService(ServicioBase[TipoCotizacion]):
    """lógica de los tipos de cotización."""

    def __init__(self, repositorio: RepositorioTipoCotizacion) -> None:
        super().__init__(repositorio)

    def crear(self, id_tipo_cotizacion: int, nombre: str) -> TipoCotizacion:
        if not nombre.strip():
            raise ValueError("El nombre del tipo de cotización no puede estar vacío.")
        tipo = TipoCotizacion(id_tipo_cotizacion, nombre)
        return self._repositorio.crear(tipo)

    def actualizar(self, id_tipo_cotizacion: int, nombre: str) -> TipoCotizacion:
        if not nombre.strip():
            raise ValueError("El nombre del tipo de cotización no puede estar vacío.")
        tipo = TipoCotizacion(id_tipo_cotizacion, nombre)
        return self._repositorio.actualizar(tipo)


class PrecioService(ServicioBase[Precio]):
    """lógica de negocio de los precios."""

    def __init__(
        self,
        repositorio: RepositorioPrecio,
        repositorio_moneda: RepositorioMoneda,
        repositorio_tipo: RepositorioTipoCotizacion,
    ) -> None:
        super().__init__(repositorio)
        self.__repositorio_moneda = repositorio_moneda
        self.__repositorio_tipo = repositorio_tipo

    def crear(
        self, id_precio: int, valor: float, id_moneda: int, id_tipo_cotizacion: int
    ) -> Precio:
        if valor <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

        moneda = self.__repositorio_moneda.leer_por_id(id_moneda)
        if moneda is None:
            raise ValueError("La moneda indicada no existe.")

        tipo = self.__repositorio_tipo.leer_por_id(id_tipo_cotizacion)
        if tipo is None:
            raise ValueError("El tipo de cotización indicado no existe.")

        precio = Precio(id_precio, valor, moneda, tipo)
        return self._repositorio.crear(precio)

    def actualizar(
        self, id_precio: int, valor: float, id_moneda: int, id_tipo_cotizacion: int
    ) -> Precio:
        if valor <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

        moneda = self.__repositorio_moneda.leer_por_id(id_moneda)
        if moneda is None:
            raise ValueError("La moneda indicada no existe.")

        tipo = self.__repositorio_tipo.leer_por_id(id_tipo_cotizacion)
        if tipo is None:
            raise ValueError("El tipo de cotización indicado no existe.")

        precio = Precio(id_precio, valor, moneda, tipo)
        return self._repositorio.actualizar(precio)


class LibroService(ServicioBase[Libro]):
    """lógica de negocio de los libros."""

    def __init__(
        self,
        repositorio: RepositorioLibro,
        repositorio_genero: RepositorioGenero,
        repositorio_editorial: RepositorioEditorial,
        repositorio_precio: RepositorioPrecio,
    ) -> None:
        super().__init__(repositorio)
        self.__repositorio_genero = repositorio_genero
        self.__repositorio_editorial = repositorio_editorial
        self.__repositorio_precio = repositorio_precio

    def crear(
        self,
        id_libro: int,
        isbn: str,
        titulo: str,
        autor: str,
        id_genero: int,
        id_editorial: int,
        id_precio: int,
    ) -> Libro:
        if not isbn.strip():
            raise ValueError("El ISBN no puede estar vacío.")
        if not titulo.strip():
            raise ValueError("El título no puede estar vacío.")
        if not autor.strip():
            raise ValueError("El autor no puede estar vacío.")

        genero = self.__repositorio_genero.leer_por_id(id_genero)
        if genero is None:
            raise ValueError("El género indicado no existe.")

        editorial = self.__repositorio_editorial.leer_por_id(id_editorial)
        if editorial is None:
            raise ValueError("La editorial indicada no existe.")

        precio = self.__repositorio_precio.leer_por_id(id_precio)
        if precio is None:
            raise ValueError("El precio indicado no existe.")

        libro = Libro(id_libro, isbn, titulo, autor, genero, editorial, precio)
        return self._repositorio.crear(libro)

    def actualizar(
        self,
        id_libro: int,
        isbn: str,
        titulo: str,
        autor: str,
        id_genero: int,
        id_editorial: int,
        id_precio: int,
    ) -> Libro:
        if not isbn.strip():
            raise ValueError("El ISBN no puede estar vacío.")
        if not titulo.strip():
            raise ValueError("El título no puede estar vacío.")
        if not autor.strip():
            raise ValueError("El autor no puede estar vacío.")

        genero = self.__repositorio_genero.leer_por_id(id_genero)
        if genero is None:
            raise ValueError("El género indicado no existe.")

        editorial = self.__repositorio_editorial.leer_por_id(id_editorial)
        if editorial is None:
            raise ValueError("La editorial indicada no existe.")

        precio = self.__repositorio_precio.leer_por_id(id_precio)
        if precio is None:
            raise ValueError("El precio indicado no existe.")

        libro = Libro(id_libro, isbn, titulo, autor, genero, editorial, precio)
        return self._repositorio.actualizar(libro)


class StockService:
    """lógica de negocio del stock."""

    def __init__(
        self, repositorio: RepositorioStock, repositorio_libro: RepositorioLibro
    ) -> None:
        self.__repositorio = repositorio
        self.__repositorio_libro = repositorio_libro

    def crear(self, id_stock: int, id_libro: int, cantidad: int) -> Stock:
        if cantidad < 0:
            raise ValueError("El stock no puede ser negativo.")

        libro = self.__repositorio_libro.leer_por_id(id_libro)
        if libro is None:
            raise ValueError("El libro indicado no existe.")

        stock = Stock(id_stock, libro, cantidad)
        return self.__repositorio.crear(stock)

    def obtener_por_libro(self, id_libro: int) -> Optional[Stock]:
        return self.__repositorio.leer_por_libro(id_libro)

    def actualizar(self, id_stock: int, id_libro: int, cantidad: int) -> Stock:
        if cantidad < 0:
            raise ValueError("El stock no puede ser negativo.")

        libro = self.__repositorio_libro.leer_por_id(id_libro)
        if libro is None:
            raise ValueError("El libro indicado no existe.")

        stock = Stock(id_stock, libro, cantidad)
        return self.__repositorio.actualizar(stock)

    def eliminar(self, id_libro: int) -> bool:
        return self.__repositorio.eliminar(id_libro)


class CotizacionDolarService:
    """lógica de las cotizaciones del dólar."""

    def __init__(
        self,
        repositorio: RepositorioCotizacionDolar,
        repositorio_moneda: RepositorioMoneda,
        repositorio_tipo: RepositorioTipoCotizacion,
    ) -> None:
        self.__repositorio = repositorio
        self.__repositorio_moneda = repositorio_moneda
        self.__repositorio_tipo = repositorio_tipo

    def crear(
        self,
        id_cotizacion: int,
        fecha: date,
        valor: float,
        id_moneda: int,
        id_tipo_cotizacion: int,
    ) -> CotizacionDolar:
        if valor <= 0:
            raise ValueError("El valor de la cotización debe ser mayor que cero.")

        moneda = self.__repositorio_moneda.leer_por_id(id_moneda)
        if moneda is None:
            raise ValueError("La moneda indicada no existe.")

        tipo = self.__repositorio_tipo.leer_por_id(id_tipo_cotizacion)
        if tipo is None:
            raise ValueError("El tipo de cotización indicado no existe.")

        cotizacion = CotizacionDolar(id_cotizacion, fecha, valor, moneda, tipo)
        return self.__repositorio.crear(cotizacion)

    def obtener_por_tipo_y_fecha(
        self, id_tipo_cotizacion: int, fecha: date
    ) -> Optional[CotizacionDolar]:
        return self.__repositorio.leer_por_tipo_y_fecha(id_tipo_cotizacion, fecha)

    def obtener_historico(self, id_tipo_cotizacion: int) -> List[CotizacionDolar]:
        return self.__repositorio.leer_historico_por_tipo(id_tipo_cotizacion)

    def actualizar(
        self,
        id_cotizacion: int,
        fecha: date,
        valor: float,
        id_moneda: int,
        id_tipo_cotizacion: int,
    ) -> CotizacionDolar:
        if valor <= 0:
            raise ValueError("El valor de la cotización debe ser mayor que cero.")

        moneda = self.__repositorio_moneda.leer_por_id(id_moneda)
        if moneda is None:
            raise ValueError("La moneda indicada no existe.")

        tipo = self.__repositorio_tipo.leer_por_id(id_tipo_cotizacion)
        if tipo is None:
            raise ValueError("El tipo de cotización indicado no existe.")

        cotizacion = CotizacionDolar(id_cotizacion, fecha, valor, moneda, tipo)
        return self.__repositorio.actualizar(cotizacion)

    def eliminar(self, id_tipo_cotizacion: int, fecha: date) -> bool:
        return self.__repositorio.eliminar(id_tipo_cotizacion, fecha)
