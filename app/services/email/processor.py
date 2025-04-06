from typing import List, Optional
from datetime import datetime
from app.models.schemas import EmailContent, ProcessedEmail

class EmailProcessor:
    def process_email(self, email: EmailContent) -> ProcessedEmail:
        """
        Procesa un email y extrae información relevante.
        Este método será extendido con IA más adelante.
        """
        return ProcessedEmail(
            email_id=email.email_id,
            thread_id=email.thread_id,
            content_summary=email.snippet,
            extracted_dates=[email.date],
            extracted_entities=[],  # Aquí irían entidades extraídas por IA
            metadata={
                "from": email.from_,
                "subject": email.subject
            }
        )

    async def process_email_batch(self, emails: List[EmailContent]) -> List[ProcessedEmail]:
        """
        Procesa un lote de emails en paralelo.
        """
        return [self.process_email(email) for email in emails] 