from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class Contact(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=5000)
    company: Optional[str] = None
    budget: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "message": "I'd love to collaborate on an AI project focusing on LLM tooling.",
                "company": "Analytical Engines",
                "budget": "$3k-$5k",
            }
        }
