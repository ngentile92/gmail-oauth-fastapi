from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict

class EmailContent(BaseModel):
    """Raw email content from Gmail"""
    email_id: str = Field(..., description="Unique identifier for the email")
    from_: str = Field(..., description="Email address of the sender")
    subject: str = Field(..., description="Subject of the email")
    date: datetime = Field(..., description="Date of the email")
    snippet: str = Field(..., description="Brief preview")
    full_content: str = Field(..., description="Complete email content")
    thread_id: str = Field(..., description="Thread identifier")

class ProcessedEmail(BaseModel):
    """Email after initial processing"""
    email_id: str
    thread_id: str
    content_summary: str = Field(..., description="Summarized content")
    extracted_dates: List[datetime] = Field(default=[], description="Dates found in content")
    extracted_entities: List[str] = Field(default=[], description="Key entities found")
    metadata: Dict[str, str] = Field(default={}, description="Additional metadata")

class Task(BaseModel):
    """Task generated from email content"""
    task_id: str = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    due_date: Optional[datetime] = Field(None, description="Due date if any")
    priority: str = Field(default="medium", description="Task priority")
    source_email_id: str = Field(..., description="Original email ID")
    status: str = Field(default="pending", description="Task status")

class TaskBatch(BaseModel):
    """Batch of tasks with metadata"""
    tasks: List[Task] = Field(..., description="List of generated tasks")
    source_email_ids: List[str] = Field(..., description="Source email IDs")
    generation_date: datetime = Field(default_factory=datetime.now, description="When tasks were generated")
    metadata: Dict[str, str] = Field(default={}, description="Additional metadata")

class ThreadMessage(BaseModel):
    from_: str
    date: str
    content: str

class EmailResponse(BaseModel):
    email_id: str
    thread_id: str
    from_: str
    subject: str
    date: str
    snippet: str
    full_content: Optional[str] = None
    thread_messages: List[ThreadMessage] = []

    class Config:
        json_schema_extra = {
            "example": {
                "email_id": "12345",
                "thread_id": "thread123",
                "from_": "sender@example.com",
                "subject": "Meeting Tomorrow",
                "date": "2024-03-20T10:00:00Z",
                "snippet": "Let's discuss the project...",
                "full_content": "Full email content here...",
                "thread_messages": [
                    {
                        "from_": "person1@example.com",
                        "date": "2024-03-20T09:00:00Z",
                        "content": "Initial message"
                    }
                ]
            }
        } 