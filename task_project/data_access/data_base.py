# task_project/data_access/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..core.models import Base  # Importación relativa
from typing import Generator
import os  # Necesario para manejar rutas de archivo

# 1. Dirección de la Base de Datos (URL)
# Usaremos una ruta absoluta para asegurar que tasks.db se cree en la raíz del proyecto
DB_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', '..', 'tasks.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"


# 2. El Motor (Engine)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 3. El Constructor de Sesiones (SessionLocal)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Creación Inicial de Tablas


def init_db():
    """Crea todas las tablas de la DB si aún no existen."""
    Base.metadata.create_all(bind=engine)
    print(f"[*] Base de datos inicializada en: {DB_FILE}")

# 5. La Llave de Agua (Patrón de Inyección de Dependencia)


def get_db() -> Generator[Session, None, None]:
    """Provee una sesión de DB y asegura su cierre."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
