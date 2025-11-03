# task_project/data_access/repositories.py
from sqlalchemy.orm import Session
# Importación Absoluta (igual que en main.py para evitar errores de ruta)
from task_project.core.models import Task
from datetime import date
from typing import Optional


class TaskRepository:
    """
    Clase Repositorio. 
    Contrato para las operaciones CRUD (Create, Read, Update, Delete) de la Entidad Task.
    """

    def __init__(self, db: Session):
        # 🔑 Inyección de Dependencia: Recibe la Sesión de DB activa.
        # El Repositorio no abre ni cierra la conexión; solo la usa.
        self.db = db

    def create_task(self, title: str, description: str = "",
                    due_date: Optional[date] = None,
                    notification_days: int = 0,
                    notification_date: Optional[date] = None
                    ) -> Task:
        """Guarda un nuevo objeto Task en la base de datos."""

        # 1. Creamos la Instancia (el objeto Task)
        db_task = Task(
            title=title,
            description=description,
            due_date=due_date,
            notification_days=notification_days,
            notification_date=notification_date
        )

        # 2. Operaciones de SQLAlchemy usando la Sesión:
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)

        return db_task

    def get_all_tasks(self, completed: Optional[bool] = None) -> list[Task]:
        """Devuelve todas las tareas, opcionalmente filtradas por estado."""

        query = self.db.query(Task)

        if completed is not None:
            # Filtra si se pide ver solo completadas o solo pendientes
            query = query.filter(Task.is_completed == completed)

        return query.all()

    # Los métodos update y delete vendrán después.
