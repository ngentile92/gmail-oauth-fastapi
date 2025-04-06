from typing import List
from datetime import datetime
import uuid
from app.models.schemas import ProcessedEmail, Task, TaskBatch

class TaskGenerator:
    def generate_task(self, email: ProcessedEmail) -> Task:
        """
        Genera una tarea a partir de un email procesado.
        Este método será extendido con IA más adelante.
        """
        return Task(
            task_id=str(uuid.uuid4()),
            title=f"Review: {email.metadata.get('subject', 'No subject')}",
            description=email.content_summary,
            due_date=email.extracted_dates[0] if email.extracted_dates else None,
            priority="medium",
            source_email_id=email.email_id,
            status="pending"
        )

    def generate_tasks(self, email: ProcessedEmail) -> List[Task]:
        """
        Genera una o más tareas a partir de un email procesado.
        """
        # Por ahora, generamos una tarea por email
        return [self.generate_task(email)]

    def get_user_tasks(self, user_id: str, status: str = None) -> List[Task]:
        """
        Obtiene las tareas de un usuario.
        TODO: Implementar persistencia de tareas.
        """
        return []  # Por ahora retorna lista vacía 