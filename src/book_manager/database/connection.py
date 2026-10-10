
"""Gestiona la conexión a la base de datos."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


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
