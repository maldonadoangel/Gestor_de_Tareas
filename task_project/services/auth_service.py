# task_project/services/auth_service.py

# Importamos las credenciales desacopladas
from task_project.settings import TASK_DEFAULT_USER, TASK_DEFAULT_PASSWORD


class AuthService:
    """Servicio de Lógica de Negocio para la Autenticación."""

    def authenticate_user(self, username: str, password: str) -> bool:
        """Verifica las credenciales usando la configuración."""
        # verifica los datos dentro de settings
        if username == TASK_DEFAULT_USER and password == TASK_DEFAULT_PASSWORD:
            return True
        return False
