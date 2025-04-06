from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ThreadMessage(BaseModel):
    from_: str
    date: str
    content: str

class EmailResponse(BaseModel):
    from_: str = ""  # Using from_ since 'from' is a Python keyword
    subject: str
    date: str
    snippet: str
    full_content: str
    thread_messages: List[ThreadMessage] = []

    class Config:
        json_schema_extra = {
            "example": {
                "from": "contact@example.com",
                "subject": "Hello",
                "date": "2024-04-01",
                "snippet": "Hi, I wanted to reach out...",
                "full_content": "Full email content here...",
                "thread_messages": [
                    {
                        "from": "other@example.com",
                        "date": "2024-04-01",
                        "content": "Previous message in thread..."
                    }
                ]
            }
        } 