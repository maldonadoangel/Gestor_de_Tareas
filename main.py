# task_project/main.py (Corrección de Importación)

# Quitamos el punto (.) y usamos el nombre completo del paquete
from task_project.data_access.data_base import init_db, get_db
from task_project.interface.cli import CLIApp
# ...
if __name__ == "__main__":

    # ...
    init_db()
    app = CLIApp(db_session_generator=get_db)
    app.run()
