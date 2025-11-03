# task_project/interfaces/cli.py
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.theme import Theme
from rich.table import Table
from typing import Callable, Generator, Optional
from sqlalchemy.orm import Session
from datetime import date
import sys

# Importación del Servicio de Tareas (Absoluta)
from task_project.services.task_service import TaskService
# Importación del Servicio de Autenticación
from task_project.services.auth_service import AuthService


class CLIApp:
    """Clase principal de la Interfaz de Línea de Comandos (CLI)."""

    def __init__(self, db_session_generator: Callable[..., Generator[Session, None, None]]):
        # 🔑 Inyección de Dependencias
        custom_theme = Theme(
            {"info": "cyan", "warning": "yellow", "error": "bold red"})
        self.console = Console(theme=custom_theme)
        self.auth_service = AuthService()  # Asumiendo que ya tienes AuthService

        # 🚨 Inicialización del Servicio de Tareas con la dependencia de DB
        self.task_service = TaskService(db_session_generator)

        self.is_logged_in = False
        self.running = False

    def run(self):
        """Inicia el ciclo principal de la aplicación."""
        self.console.clear()
        self.console.print(Panel(
            "[bold green]Sistema de Gestión de Tareas[/bold green]", title="[info]Bienvenido[/info]"))

        # 1. Autenticación
        if not self._login_prompt():
            self.console.print(
                Panel("[bold red]❌ No se pudo iniciar sesión[/bold red]"), style="red")
            sys.exit(0)  # Sale si falla el login

        self.is_logged_in = True
        self.running = True
        self.main_loop()

    def _login_prompt(self) -> bool:
        """Muestra el prompt de login."""
        # Nota: Asumiendo que _login_prompt existe y devuelve True/False.
        # Aquí puedes llamar a tu login_module.login() si lo tienes separado.

        # Simulamos un login simple para no bloquear el flujo:
        self.console.print(" ")
        self.console.print(Panel("[bold cyan]Inicie Sesión[/bold cyan]"))
        usuario = Prompt.ask("[green]Usuario[/green]", default="admin")
        password = Prompt.ask("[green]Contraseña[/green]",
                              password=True, default="1234")

        # Verifica con el servicio de auth (o simple if/else)
        if usuario == "admin" and password == "1234":
            self.console.print(
                Panel("[bold green]✅ Acceso concedido[/bold green]"))
            return True
        else:
            self.console.print(
                Panel("[bold red]❌ Usuario o contraseña incorrectos[/bold red]"))
            return False

    def main_loop(self):
        """Muestra el menú principal y maneja las opciones."""
        while self.running:
            self.console.clear()
            self.console.print(Panel(
                "[bold blue]Menú Principal[/bold blue]", title="[info]Gestor de Tareas[/info]"))

            # Opciones del menú
            menu_options = [
                ("1", "Añadir nueva Tarea"),
                ("2", "Ver Tareas Pendientes"),
                ("3", "Salir")
            ]

            menu_table = Table(title="Opciones")
            menu_table.add_column("Opción", style="bold cyan")
            menu_table.add_column("Acción", style="green")

            for key, action in menu_options:
                menu_table.add_row(key, action)

            self.console.print(menu_table)

            choice = Prompt.ask(
                "[yellow]Elige una opción[/yellow]", choices=["1", "2", "3"])

            if choice == "1":
                self._add_task_prompt()
            elif choice == "2":
                # 🚨 CAMBIO AQUÍ
                self._list_tasks_prompt()
            elif choice == "3":
                self.running = False
                self.console.print(
                    Panel("[bold red]👋 ¡Hasta pronto![/bold red]"))
                sys.exit(0)

    def _add_task_prompt(self):
        """Solicita los datos al usuario y llama al TaskService para guardar la tarea."""
        self.console.clear()
        self.console.print(Panel("[bold cyan]Añadir Tarea Nueva[/bold cyan]"))

        title = Prompt.ask("[green]Título de la tarea[/green]")
        description = Prompt.ask(
            "[green]Descripción (opcional)[/green]", default="")

        # Solicitud de fecha de vencimiento (formato YYYY-MM-DD)
        due_date_str = Prompt.ask(
            "[green]Fecha de Vencimiento (YYYY-MM-DD, opcional)[/green]", default="")

        due_date = None
        if due_date_str:
            try:
                # Convertir la cadena a objeto date de Python
                due_date = date.fromisoformat(due_date_str)
            except ValueError:
                self.console.print(
                    "[bold red]❌ Formato de fecha inválido. Tarea guardada sin fecha de vencimiento.[/bold red]")

        # Solicitud de días de notificación
        notification_days_str = Prompt.ask(
            "[green]Días de antelación para notificar (ej: 3, 0 para no notificar)[/green]", default="0")

        try:
            notification_days = int(notification_days_str)
        except ValueError:
            self.console.print(
                "[bold red]❌ Días de notificación inválidos. Usando 0.[/bold red]")
            notification_days = 0

        try:
            # 🚨 Llama al TaskService (la lógica de negocio y guardado)
            new_task = self.task_service.add_task(
                title=title,
                description=description,
                due_date=due_date,
                notification_days=notification_days
            )

            self.console.print(Panel(
                f"[bold green]✅ Tarea guardada con éxito:[/bold green]\n"
                f"ID: {new_task.id}\n"
                f"Título: {new_task.title}\n"
                f"Vencimiento: {new_task.due_date.strftime('%Y-%m-%d') if new_task.due_date else 'N/A'}"
            ))

        except Exception as e:
            self.console.print(
                Panel(f"[bold red]❌ Error al guardar la tarea:[/bold red] {e}"))

        Prompt.ask("Presiona Enter para volver al menú...")

# task_project/interfaces/cli.py (NUEVO MÉTODO)

# ... (dentro de la clase CLIApp)

    def _list_tasks_prompt(self):
        """Obtiene las tareas pendientes y las muestra en una tabla."""
        self.console.clear()
        self.console.print(Panel("[bold cyan]Tareas Pendientes[/bold cyan]"))

        try:
            # 🚨 Llama al TaskService
            tasks = self.task_service.get_pending_tasks()
        except Exception as e:
            self.console.print(
                Panel(f"[bold red]❌ Error al obtener tareas:[/bold red] {e}"))
            Prompt.ask("Presiona Enter para continuar...")
            return

        if not tasks:
            self.console.print(
                Panel("[bold yellow]🎉 ¡No tienes tareas pendientes![/bold yellow]"))
        else:
            table = Table(title="Lista de Tareas Pendientes")
            table.add_column("ID", style="bold cyan", justify="center")
            table.add_column("Título", style="bold white")
            table.add_column("Vencimiento", style="yellow")
            table.add_column("Notificar", style="green")
            table.add_column("Días", style="magenta", justify="center")

            for task in tasks:
                # Formateo para la vista
                due_date_str = task.due_date.strftime(
                    '%Y-%m-%d') if task.due_date else 'N/A'

                table.add_row(
                    str(task.id),
                    task.title,
                    due_date_str,
                    task.notification_date.strftime(
                        '%Y-%m-%d') if task.notification_date else 'N/A',
                    str(task.notification_days)
                )

            self.console.print(table)

        Prompt.ask("Presiona Enter para volver al menú...")


if __name__ == '__main__':
    # Esto solo se usa para pruebas rápidas de la interfaz, pero el 'main.py' real
    # es el que llama a esta clase con las dependencias correctas.
    pass
