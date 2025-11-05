# task_project/core/models.py

from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from sqlalchemy.orm import declarative_base

# El Cimiento de SQLAlchemy
Base = declarative_base()


class Task(Base):
    """Modelo ORM para la tabla 'tasks'."""

    __tablename__ = "tasks"

    # --- ATRIBUTOS (COLUMNAS) ---
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)

    #  CORRECCIÓN: Se agrega la descripción que faltaba en el error.
    description = Column(String, default="")

    is_completed = Column(Boolean, default=False)

    # Campos de Vencimiento y Notificación
    due_date = Column(Date, nullable=True)
    notification_days = Column(Integer, default=0)
    notification_date = Column(Date, nullable=True)

    # Tiempos de Auditoría
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.is_completed})>"
