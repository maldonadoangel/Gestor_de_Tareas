# task_project/services/task_service.py

from datetime import date, timedelta
from typing import Callable, Generator, Optional
from sqlalchemy.orm import Session

# Importación de Capas Inferiores (Absoluta para evitar errores de ruta)
from task_project.data_access.repository import TaskRepository
from task_project.core.models import Task


class TaskService:
    """
    Clase de Servicio para la lógica de negocio de las tareas.
    Se encarga de cálculos (como fechas) y de coordinar con el Repositorio.
    """

    def __init__(self, db_session_generator: Callable[..., Generator[Session, None, None]]):
        """
        Recibe el generador de sesiones de DB por Inyección de Dependencias.
        """
        self.get_db = db_session_generator

    def _calculate_notification_date(self, due_date: date, notification_days: int) -> Optional[date]:
        """
        Lógica de Negocio: Calcula la fecha de aviso.
        Si la fecha de vencimiento es hoy o en el pasado, no se notifica.
        """
        if notification_days > 0 and due_date:
            # Restamos los días de notificación a la fecha de vencimiento.
            notification_date = due_date - timedelta(days=notification_days)
            # Solo notificamos si la fecha de notificación es hoy o en el futuro
            if notification_date >= date.today():
                return notification_date
        return None

    def add_task(self, title: str, description: str,
                 due_date: Optional[date], notification_days: int) -> Task:
        """
        Lógica de Transacción: 
        1. Calcula la fecha de notificación.
        2. Abre una sesión de DB.
        3. Crea el Repositorio con esa sesión.
        4. Llama al método de guardado del Repositorio.
        """

        # 1. Lógica de Negocio: Cálculo de la fecha
        notification_date = self._calculate_notification_date(
            due_date, notification_days)

        # 2. Manejo de la Sesión de DB (Patrón Context Manager con el generador)
        # Esto automáticamente abre la sesión, la usa y la CIERRA (gracias a 'finally' en get_db)
        for db in self.get_db():
            # 3. Inicializa el Repositorio con la Sesión activa
            repo = TaskRepository(db)

            # 4. Llama al Repositorio para guardar los datos
            new_task = repo.create_task(
                title=title,
                description=description,
                due_date=due_date,
                notification_days=notification_days,
                notification_date=notification_date  # Pasa el valor calculado
            )
            return new_task

    # El método list_tasks vendrá después.
