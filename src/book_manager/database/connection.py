
"""Gestiona la conexión a la base de datos."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

# Importamos herramientas para crear un context manager.
from contextlib import contextmanager
from collections.abc import Generator


class ConexionDB:
    """Administra el motor de conexión y las sesiones de SQLAlchemy."""

    def __init__(self) -> None:
        """Inicializa el motor y la fábrica de sesiones."""
        load_dotenv()

        url_conexion = os.getenv("DATABASE_URL")

        if not url_conexion:
            raise ValueError(
                "No se encontró la URL de la base de datos en el archivo .env"
            )

        self._engine: Engine = create_engine(
            url_conexion,
            pool_pre_ping=True,
        )

        self._session_factory = sessionmaker(
            bind=self._engine,
            class_=Session,
            expire_on_commit=False,
        )

    def obtener_sesion(self) -> Session:
        """Crea y devuelve una sesión para utilizar la base de datos."""
        return self._session_factory()

    def cerrar_conexion(self) -> None:
        """Libera los recursos asociados al motor de conexión."""
        self._engine.dispose()

    @contextmanager
    def transaccion(self) -> Generator[Session, None, None]:
      """Administra una transacción y gestiona su confirmación o reversión."""
      # Creamos una sesión para la transacción.
      sesion = self._session_factory()
      try:
        # Entregamos la sesión para realizar las operaciones.
        yield sesion
        # Confirmamos los cambios si no ocurrió ningún error.
        sesion.commit()
        
      except Exception:
        # Revertimos los cambios si ocurre un error.
        sesion.rollback()
        raise
      finally:
        # Cerramos la sesión al finalizar.
        sesion.close()
