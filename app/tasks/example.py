import time
from app.core.celery import celery


@celery.task
def long_running_task(task_name: str):
    """Simula uma tarefa demorada."""
    print(f"Iniciando tarefa: {task_name}")
    time.sleep(10)
    print(f"Tarefa {task_name} concluída!")
    return {"message": f"Tarefa {task_name} finalizada com sucesso"}
