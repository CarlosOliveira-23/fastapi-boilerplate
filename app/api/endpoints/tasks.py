from fastapi import APIRouter
from app.tasks.example import long_running_task

router = APIRouter()


@router.post("/start-task/{task_name}")
def start_task(task_name: str):
    """Inicia uma tarefa assíncrona no Celery."""
    task = long_running_task.delay(task_name)
    return {"task_id": task.id, "message": f"Tarefa {task_name} iniciada"}
