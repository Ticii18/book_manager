"""Repositorios del sistema mediante SQLAlchemy."""

from abc import ABC, abstractmethod
from datetime import date
from typing import Generic, List, Optional, Type, TypeVar

from book_manager.database.connection import ConexionDB
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
from book_manager.models.models import (
    CotizacionDolarModel,
    EditorialModel,
    GeneroModel,
    LibroModel,
    MonedaModel,
    PrecioModel,
    StockModel,
    TipoCotizacionModel,
)

T = TypeVar("T", bound=EntidadBase)
M = TypeVar("M")


class IRepositorio(ABC, Generic[T]):
    """Interfaz base para todos los repositorios."""

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

# clase que obtiene el modelo y la entidad para alguna acción del CRUD.
class RepositorioBaseSQL(IRepositorio[T], Generic[T, M]):
    """Clase base para repositorios."""

    def __init__(self, modelo_cls: Type[M], db: Optional[ConexionDB] = None) -> None:
        self._modelo_cls = modelo_cls
        self._db = db or ConexionDB()

    @abstractmethod
    def _modelo_a_entidad(self, modelo: M) -> T:
        """Convierte un modelo de SQLAlchemy a su entidad de dominio."""
        pass

    def leer_por_id(self, id: int) -> Optional[T]:
        with self._db.obtener_sesion() as sesion:
            m = sesion.query(self._modelo_cls).filter_by(id=id).first()
            return self._modelo_a_entidad(m) if m else None

    def leer_todos(self) -> List[T]:
        with self._db.obtener_sesion() as sesion:
            modelos = sesion.query(self._modelo_cls).order_by(getattr(self._modelo_cls, "id")).all()
            return [self._modelo_a_entidad(m) for m in modelos]

    def eliminar(self, id: int) -> bool:
        with self._db.transaccion() as sesion:
            m = sesion.query(self._modelo_cls).filter_by(id=id).first()
            if m is None:
                return False
            sesion.delete(m)
            return True


# Repositorios Específicos

class RepositorioGenero(RepositorioBaseSQL[Genero, GeneroModel]):
    """Repositorio para la entidad Genero."""

    def __init__(self, db: Optional[ConexionDB] = None) -> None:
        super().__init__(GeneroModel, db)

    def _modelo_a_entidad(self, modelo: GeneroModel) -> Genero:
        return Genero(id_genero=modelo.id, nombre=modelo.nombre)

    def crear(self, genero: Genero) -> Genero:
        with self._db.transaccion() as sesion:
            if sesion.query(GeneroModel).filter_by(id=genero.id).first() is not None:
                raise ValueError("Ya existe un género con ese ID.")
            modelo = GeneroModel(id=genero.id, nombre=genero.nombre)
            sesion.add(modelo)
        return genero

    def actualizar(self, genero: Genero) -> Genero:
        with self._db.transaccion() as sesion:
            m = sesion.query(GeneroModel).filter_by(id=genero.id).first()
            if m is None:
                raise ValueError("No existe un género con ese ID.")
            m.nombre = genero.nombre
        return genero

    def tiene_libros_asociados(self, id_genero: int) -> bool:
        """Verifica si algún libro tiene asignado este género."""
        with self._db.obtener_sesion() as sesion:
            return sesion.query(LibroModel).filter_by(genero_id=id_genero).first() is not None


class RepositorioEditorial(RepositorioBaseSQL[Editorial, EditorialModel]):
    """Repositorio para la entidad Editorial."""

    def __init__(self, db: Optional[ConexionDB] = None) -> None:
        super().__init__(EditorialModel, db)

    def _modelo_a_entidad(self, modelo: EditorialModel) -> Editorial:
        return Editorial(id_editorial=modelo.id, nombre=modelo.nombre)

    def crear(self, editorial: Editorial) -> Editorial:
        with self._db.transaccion() as sesion:
            if sesion.query(EditorialModel).filter_by(id=editorial.id).first() is not None:
                raise ValueError("Ya existe una editorial con ese ID.")
            modelo = EditorialModel(id=editorial.id, nombre=editorial.nombre)
            sesion.add(modelo)
        return editorial

    def actualizar(self, editorial: Editorial) -> Editorial:
        with self._db.transaccion() as sesion:
            m = sesion.query(EditorialModel).filter_by(id=editorial.id).first()
            if m is None:
                raise ValueError("No existe una editorial con ese ID.")
            m.nombre = editorial.nombre
        return editorial

    def tiene_libros_asociados(self, id_editorial: int) -> bool:
        """Verifica si algún libro tiene asignada esta editorial."""
        with self._db.obtener_sesion() as sesion:
            return sesion.query(LibroModel).filter_by(editorial_id=id_editorial).first() is not None


class RepositorioMoneda(RepositorioBaseSQL[Moneda, MonedaModel]):
    """Repositorio para la entidad Moneda."""

    def __init__(self, db: Optional[ConexionDB] = None) -> None:
        super().__init__(MonedaModel, db)

    def _modelo_a_entidad(self, modelo: MonedaModel) -> Moneda:
        return Moneda(id_moneda=modelo.id, nombre=modelo.nombre, simbolo=modelo.simbolo)

    def crear(self, moneda: Moneda) -> Moneda:
        with self._db.transaccion() as sesion:
            if sesion.query(MonedaModel).filter_by(id=moneda.id).first() is not None:
                raise ValueError("Ya existe una moneda con ese ID.")
            modelo = MonedaModel(id=moneda.id, nombre=moneda.nombre, simbolo=moneda.simbolo)
            sesion.add(modelo)
        return moneda

    def actualizar(self, moneda: Moneda) -> Moneda:
        with self._db.transaccion() as sesion:
            m = sesion.query(MonedaModel).filter_by(id=moneda.id).first()
            if m is None:
                raise ValueError("No existe una moneda con ese ID.")
            m.nombre = moneda.nombre
            m.simbolo = moneda.simbolo
        return moneda


class RepositorioTipoCotizacion(RepositorioBaseSQL[TipoCotizacion, TipoCotizacionModel]):
    """Repositorio para la entidad TipoCotizacion."""

    def __init__(self, db: Optional[ConexionDB] = None) -> None:
        super().__init__(TipoCotizacionModel, db)

    def _modelo_a_entidad(self, modelo: TipoCotizacionModel) -> TipoCotizacion:
        return TipoCotizacion(id_tipo_cotizacion=modelo.id, nombre=modelo.nombre)

    def crear(self, tipo: TipoCotizacion) -> TipoCotizacion:
        with self._db.transaccion() as sesion:
            if sesion.query(TipoCotizacionModel).filter_by(id=tipo.id).first() is not None:
                raise ValueError("Ya existe un tipo de cotización con ese ID.")
            modelo = TipoCotizacionModel(id=tipo.id, nombre=tipo.nombre)
            sesion.add(modelo)
        return tipo

    def actualizar(self, tipo: TipoCotizacion) -> TipoCotizacion:
        with self._db.transaccion() as sesion:
            m = sesion.query(TipoCotizacionModel).filter_by(id=tipo.id).first()
            if m is None:
                raise ValueError("No existe un tipo de cotización con ese ID.")
            m.nombre = tipo.nombre
        return tipo


class RepositorioPrecio(RepositorioBaseSQL[Precio, PrecioModel]):
    """Repositorio para la entidad Precio."""

    def __init__(self, db: Optional[ConexionDB] = None) -> None:
        super().__init__(PrecioModel, db)

    def _modelo_a_entidad(self, modelo: PrecioModel) -> Precio:
        moneda = Moneda(
            id_moneda=modelo.moneda.id,
            nombre=modelo.moneda.nombre,
            simbolo=modelo.moneda.simbolo,
        )
        tipo = TipoCotizacion(
            id_tipo_cotizacion=modelo.tipo_cotizacion.id,
            nombre=modelo.tipo_cotizacion.nombre,
        )
        return Precio(
            id_precio=modelo.id,
            valor=modelo.valor,
            moneda=moneda,
            tipo_cotizacion=tipo,
        )

    def crear(self, precio: Precio) -> Precio:
        with self._db.transaccion() as sesion:
            if sesion.query(PrecioModel).filter_by(id=precio.id).first() is not None:
                raise ValueError("Ya existe un precio con ese ID.")
            modelo = PrecioModel(
                id=precio.id,
                valor=precio.valor,
                moneda_id=precio.moneda.id,
                tipo_cotizacion_id=precio.tipo_cotizacion.id,
            )
            sesion.add(modelo)
        return precio

    def actualizar(self, precio: Precio) -> Precio:
        with self._db.transaccion() as sesion:
            m = sesion.query(PrecioModel).filter_by(id=precio.id).first()
            if m is None:
                raise ValueError("No existe un precio con ese ID.")
            m.valor = precio.valor
            m.moneda_id = precio.moneda.id
            m.tipo_cotizacion_id = precio.tipo_cotizacion.id
        return precio


class RepositorioLibro(RepositorioBaseSQL[Libro, LibroModel]):
    """Repositorio para la entidad Libro."""

    def __init__(self, db: Optional[ConexionDB] = None) -> None:
        super().__init__(LibroModel, db)

    def _modelo_a_entidad(self, modelo: LibroModel) -> Libro:
        genero = Genero(id_genero=modelo.genero.id, nombre=modelo.genero.nombre)
        editorial = Editorial(id_editorial=modelo.editorial.id, nombre=modelo.editorial.nombre)
        moneda = Moneda(
            id_moneda=modelo.precio.moneda.id,
            nombre=modelo.precio.moneda.nombre,
            simbolo=modelo.precio.moneda.simbolo,
        )
        tipo = TipoCotizacion(
            id_tipo_cotizacion=modelo.precio.tipo_cotizacion.id,
            nombre=modelo.precio.tipo_cotizacion.nombre,
        )
        precio = Precio(
            id_precio=modelo.precio.id,
            valor=modelo.precio.valor,
            moneda=moneda,
            tipo_cotizacion=tipo,
        )
        return Libro(
            id_libro=modelo.id,
            isbn=modelo.isbn,
            titulo=modelo.titulo,
            autor=modelo.autor,
            genero=genero,
            editorial=editorial,
            precio=precio,
        )

    def crear(self, libro: Libro) -> Libro:
        with self._db.transaccion() as sesion:
            if sesion.query(LibroModel).filter_by(id=libro.id).first() is not None:
                raise ValueError("Ya existe un libro con ese ID.")
            modelo = LibroModel(
                id=libro.id,
                isbn=libro.isbn,
                titulo=libro.titulo,
                autor=libro.autor,
                genero_id=libro.genero.id,
                editorial_id=libro.editorial.id,
                precio_id=libro.precio.id,
            )
            sesion.add(modelo)
        return libro

    def actualizar(self, libro: Libro) -> Libro:
        with self._db.transaccion() as sesion:
            m = sesion.query(LibroModel).filter_by(id=libro.id).first()
            if m is None:
                raise ValueError("No existe un libro con ese ID.")
            m.isbn = libro.isbn
            m.titulo = libro.titulo
            m.autor = libro.autor
            m.genero_id = libro.genero.id
            m.editorial_id = libro.editorial.id
            m.precio_id = libro.precio.id
        return libro


class RepositorioStock(RepositorioBaseSQL[Stock, StockModel]):
    """Repositorio para la entidad Stock."""

    def __init__(self, db: Optional[ConexionDB] = None) -> None:
        super().__init__(StockModel, db)
        self.__repo_libro = RepositorioLibro(db)

    def _modelo_a_entidad(self, modelo: StockModel) -> Stock:
        libro = self.__repo_libro._modelo_a_entidad(modelo.libro)
        return Stock(id_stock=modelo.id, libro=libro, cantidad=modelo.cantidad)

    def crear(self, stock: Stock) -> Stock:
        with self._db.transaccion() as sesion:
            if sesion.query(StockModel).filter_by(libro_id=stock.libro.id).first() is not None:
                raise ValueError("Ya existe stock para ese libro.")
            modelo = StockModel(id=stock.id, libro_id=stock.libro.id, cantidad=stock.cantidad)
            sesion.add(modelo)
        return stock

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        with self._db.obtener_sesion() as sesion:
            m = sesion.query(StockModel).filter_by(libro_id=libro_id).first()
            return self._modelo_a_entidad(m) if m else None

    def actualizar(self, stock: Stock) -> Stock:
        with self._db.transaccion() as sesion:
            m = sesion.query(StockModel).filter_by(libro_id=stock.libro.id).first()
            if m is None:
                raise ValueError("No existe stock para ese libro.")
            m.cantidad = stock.cantidad
        return stock

    def eliminar(self, libro_id: int) -> bool:
        """Elimina el registro de stock por ID de libro."""
        with self._db.transaccion() as sesion:
            m = sesion.query(StockModel).filter_by(libro_id=libro_id).first()
            if m is None:
                return False
            sesion.delete(m)
            return True


class RepositorioCotizacionDolar(RepositorioBaseSQL[CotizacionDolar, CotizacionDolarModel]):
    """Repositorio para la entidad CotizacionDolar."""

    def __init__(self, db: Optional[ConexionDB] = None) -> None:
        super().__init__(CotizacionDolarModel, db)

    def _modelo_a_entidad(self, modelo: CotizacionDolarModel) -> CotizacionDolar:
        moneda = Moneda(
            id_moneda=modelo.moneda.id,
            nombre=modelo.moneda.nombre,
            simbolo=modelo.moneda.simbolo,
        )
        tipo = TipoCotizacion(
            id_tipo_cotizacion=modelo.tipo_cotizacion.id,
            nombre=modelo.tipo_cotizacion.nombre,
        )
        return CotizacionDolar(
            id_cotizacion=modelo.id,
            fecha=modelo.fecha,
            valor=modelo.valor,
            moneda=moneda,
            tipo_cotizacion=tipo,
        )

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        with self._db.transaccion() as sesion:
            existente = (
                sesion.query(CotizacionDolarModel)
                .filter_by(
                    tipo_cotizacion_id=cotizacion.tipo_cotizacion.id,
                    fecha=cotizacion.fecha,
                )
                .first()
            )
            if existente is not None:
                raise ValueError("Ya existe una cotización para ese tipo y fecha.")

            modelo = CotizacionDolarModel(
                id=cotizacion.id,
                fecha=cotizacion.fecha,
                valor=cotizacion.valor,
                moneda_id=cotizacion.moneda.id,
                tipo_cotizacion_id=cotizacion.tipo_cotizacion.id,
            )
            sesion.add(modelo)
        return cotizacion

    def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: date) -> Optional[CotizacionDolar]:
        with self._db.obtener_sesion() as sesion:
            m = (
                sesion.query(CotizacionDolarModel)
                .filter_by(tipo_cotizacion_id=tipo_id, fecha=fecha)
                .first()
            )
            return self._modelo_a_entidad(m) if m else None

    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        with self._db.obtener_sesion() as sesion:
            modelos = (
                sesion.query(CotizacionDolarModel)
                .filter_by(tipo_cotizacion_id=tipo_id)
                .order_by(CotizacionDolarModel.fecha)
                .all()
            )
            return [self._modelo_a_entidad(m) for m in modelos]

    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        with self._db.transaccion() as sesion:
            m = (
                sesion.query(CotizacionDolarModel)
                .filter_by(
                    tipo_cotizacion_id=cotizacion.tipo_cotizacion.id,
                    fecha=cotizacion.fecha,
                )
                .first()
            )
            if m is None:
                raise ValueError("No existe una cotización para ese tipo y fecha.")
            m.valor = cotizacion.valor
            m.moneda_id = cotizacion.moneda.id
        return cotizacion

    def eliminar(self, tipo_id: int, fecha: date) -> bool:
        with self._db.transaccion() as sesion:
            m = (
                sesion.query(CotizacionDolarModel)
                .filter_by(tipo_cotizacion_id=tipo_id, fecha=fecha)
                .first()
            )
            if m is None:
                return False
            sesion.delete(m)
            return True
