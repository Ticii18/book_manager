## [Ejercicio 07]
- Se agregó la variable `API_URL` al archivo `.env` con la URL de la API del dólar.
- Se implementó `obtener_cotizaciones` para descargar las cotizaciones desde la API y registrarlas en la base de datos.
- Se actualizan las cotizaciones existentes para el mismo tipo y fecha.


## [Ejercicio 06]
- Se migraron los repositorios para utilizar persistencia en base de datos.
- Se implementó la clase genérica `RepositorioBaseSQL` heredando de `IRepositorio`.
- Se definió la interfaz `IServicio` y la clase base genérica `ServicioBase` para reutilizar lógica CRUD en los servicios.



## [Ejercicio 05]
- Se implementó la función `migrar_datos` para el procesamiento de CSV.
- Se generaron los archivos SQL con las sentencias de inserción dentro de `migrations/sql/`.
- Se cargaron los registros a la BD correctamente.


## [Ejercicio 04]
- Se definieron los modelos de las ocho tablas del sistema con SQLAlchemy.
- Se establecieron los tipos de datos y las claves primarias.
- Se agregaron las claves foráneas y relaciones entre las tablas.

## [Ejercicio 03]
- Se implementó un context manager para administrar las transacciones con SQLAlchemy.
- Se agregó la confirmación de cambios y la reversión ante errores.
- Se incorporó el cierre de la sesión al finalizar la transacción.

## [Ejercicio 02]
- Se implementó la clase `ConexionDB` para administrar el motor de conexión y las sesiones mediante SQLAlchemy.
- Se configuró la lectura de `DATABASE_URL` desde las variables de entorno.
- Se comprobó la conexión con PostgreSQL mediante una consulta de prueba.

# Changelog

## [Ejercicio 01]

- Se inició el Sprint 2 a partir de la rama Sprint_1.
- Se creó la estructura de directorios para la base de datos,
  los modelos y las migraciones SQL.
- Se prepararon los archivos iniciales connection.py y models.py.
- Se actualizaron las reglas de .gitignore para excluir archivos
  temporales de Python y credenciales locales.
