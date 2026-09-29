from datetime import date

class EntidadBase:

    def __init__(self, id: int) -> None:
        self.__id = id

    @property
    def id(self) -> int:
        return self.__id


class Genero(EntidadBase):

    def __init__(self, id_genero: int, nombre: str) -> None:
        super().__init__(id_genero)
        self.__nombre = nombre

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = valor


class Editorial(EntidadBase):

    def __init__(self, id_editorial: int, nombre: str) -> None:
        super().__init__(id_editorial)
        self.__nombre = nombre

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = valor


class Moneda(EntidadBase):

    def __init__(self, id_moneda: int, nombre: str, simbolo: str) -> None:
        super().__init__(id_moneda)
        self.__nombre = nombre
        self.__simbolo = simbolo

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = valor

    @property
    def simbolo(self) -> str:
        return self.__simbolo

    @simbolo.setter
    def simbolo(self, valor: str) -> None:
        self.__simbolo = valor


class TipoCotizacion(EntidadBase):

    def __init__(self, id_tipo_cotizacion: int, nombre: str) -> None:
        super().__init__(id_tipo_cotizacion)
        self.__nombre = nombre

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = valor


class Precio(EntidadBase):

    def __init__(
        self,
        id_precio: int,
        valor: float,
        moneda: Moneda,
        tipo_cotizacion: TipoCotizacion,
    ) -> None:
        super().__init__(id_precio)
        self.__valor = valor
        self.__moneda = moneda
        self.__tipo_cotizacion = tipo_cotizacion

    @property
    def valor(self) -> float:
        return self.__valor

    @valor.setter
    def valor(self, valor: float) -> None:
        self.__valor = valor

    @property
    def moneda(self) -> Moneda:
        return self.__moneda

    @moneda.setter
    def moneda(self, valor: Moneda) -> None:
        self.__moneda = valor

    @property
    def tipo_cotizacion(self) -> TipoCotizacion:
        return self.__tipo_cotizacion

    @tipo_cotizacion.setter
    def tipo_cotizacion(self, valor: TipoCotizacion) -> None:
        self.__tipo_cotizacion = valor


class Stock(EntidadBase):

    def __init__(self, id_stock: int, libro: "Libro", cantidad: int) -> None:
        super().__init__(id_stock)
        self.__libro = libro
        self.__cantidad = cantidad

    @property
    def libro(self) -> "Libro":
        return self.__libro

    @libro.setter
    def libro(self, valor: "Libro") -> None:
        self.__libro = valor

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        self.__cantidad = valor


class Libro(EntidadBase):

    def __init__(
        self,
        id_libro: int,
        isbn: str,
        titulo: str,
        autor: str,
        genero: Genero,
        editorial: Editorial,
        precio: Precio,
    ) -> None:
        super().__init__(id_libro)
        self.__isbn = isbn
        self.__titulo = titulo
        self.__autor = autor
        self.__genero = genero
        self.__editorial = editorial
        self.__precio = precio

    @property
    def isbn(self) -> str:
        return self.__isbn

    @isbn.setter
    def isbn(self, valor: str) -> None:
        self.__isbn = valor

    @property
    def titulo(self) -> str:
        return self.__titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        self.__titulo = valor

    @property
    def autor(self) -> str:
        return self.__autor

    @autor.setter
    def autor(self, valor: str) -> None:
        self.__autor = valor

    @property
    def genero(self) -> Genero:
        return self.__genero

    @genero.setter
    def genero(self, valor: Genero) -> None:
        self.__genero = valor

    @property
    def editorial(self) -> Editorial:
        return self.__editorial

    @editorial.setter
    def editorial(self, valor: Editorial) -> None:
        self.__editorial = valor

    @property
    def precio(self) -> Precio:
        return self.__precio

    @precio.setter
    def precio(self, valor: Precio) -> None:
        self.__precio = valor


class CotizacionDolar(EntidadBase):

    def __init__(
        self,
        id_cotizacion: int,
        fecha: date,
        valor: float,
        moneda: Moneda,
        tipo_cotizacion: TipoCotizacion,
    ) -> None:
        super().__init__(id_cotizacion)
        self.__fecha = fecha
        self.__valor = valor
        self.__moneda = moneda
        self.__tipo_cotizacion = tipo_cotizacion

    @property
    def fecha(self) -> date:
        return self.__fecha

    @fecha.setter
    def fecha(self, valor: date) -> None:
        self.__fecha = valor

    @property
    def valor(self) -> float:
        return self.__valor

    @valor.setter
    def valor(self, valor: float) -> None:
        self.__valor = valor

    @property
    def moneda(self) -> Moneda:
        return self.__moneda

    @moneda.setter
    def moneda(self, valor: Moneda) -> None:
        self.__moneda = valor

    @property
    def tipo_cotizacion(self) -> TipoCotizacion:
        return self.__tipo_cotizacion

    @tipo_cotizacion.setter
    def tipo_cotizacion(self, valor: TipoCotizacion) -> None:
        self.__tipo_cotizacion = valor
