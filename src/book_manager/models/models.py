
"""Define la estructura de las tablas de la base de datos."""

# Importamos los tipos de datos y las herramientas para definir relaciones.
from datetime import date
from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Clase base para los modelos de SQLAlchemy."""

    pass


class GeneroModel(Base):
    """Representa los géneros literarios."""

    __tablename__ = "generos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)


class EditorialModel(Base):
    """Representa las editoriales de los libros."""

    __tablename__ = "editoriales"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)


class MonedaModel(Base):
    """Representa las monedas utilizadas en el sistema."""

    __tablename__ = "monedas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    simbolo: Mapped[str] = mapped_column(String(10), nullable=False)


class TipoCotizacionModel(Base):
    """Representa los tipos de cotización disponibles."""

    __tablename__ = "tipos_cotizacion"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)

class PrecioModel(Base):
    """Representa el precio de un libro."""

    __tablename__ = "precios"

    id: Mapped[int] = mapped_column(primary_key=True)
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    moneda_id: Mapped[int] = mapped_column(
        ForeignKey("monedas.id"),
        nullable=False,
    )
    tipo_cotizacion_id: Mapped[int] = mapped_column(
        ForeignKey("tipos_cotizacion.id"),
        nullable=False,
    )

    moneda: Mapped["MonedaModel"] = relationship()
    tipo_cotizacion: Mapped["TipoCotizacionModel"] = relationship()


class LibroModel(Base):
    """Representa los libros registrados en el sistema."""

    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(primary_key=True)
    isbn: Mapped[str] = mapped_column(String(19), nullable=False, unique=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    autor: Mapped[str] = mapped_column(String(150), nullable=False)
    genero_id: Mapped[int] = mapped_column(
        ForeignKey("generos.id"),
        nullable=False,
    )
    editorial_id: Mapped[int] = mapped_column(
        ForeignKey("editoriales.id"),
        nullable=False,
    )
    precio_id: Mapped[int] = mapped_column(
        ForeignKey("precios.id"),
        nullable=False,
    )

    genero: Mapped["GeneroModel"] = relationship()
    editorial: Mapped["EditorialModel"] = relationship()
    precio: Mapped["PrecioModel"] = relationship()


class StockModel(Base):
    """Representa la cantidad disponible de cada libro."""

    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(primary_key=True)
    libro_id: Mapped[int] = mapped_column(
        ForeignKey("libros.id"),
        nullable=False,
        unique=True,
    )
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    libro: Mapped["LibroModel"] = relationship()


class CotizacionDolarModel(Base):
    """Representa una cotización del dólar en una fecha determinada."""

    __tablename__ = "cotizaciones_dolar"

    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    moneda_id: Mapped[int] = mapped_column(
        ForeignKey("monedas.id"),
        nullable=False,
    )
    tipo_cotizacion_id: Mapped[int] = mapped_column(
        ForeignKey("tipos_cotizacion.id"),
        nullable=False,
    )

    moneda: Mapped["MonedaModel"] = relationship()
    tipo_cotizacion: Mapped["TipoCotizacionModel"] = relationship()
