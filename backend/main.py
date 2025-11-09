from __future__ import annotations

from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_document, get_documents
from schemas import Contact

app = FastAPI(title="Portfolio API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactResponse(BaseModel):
    success: bool
    message: str


@app.get("/test")
async def test() -> dict:
    return {"ok": True}


@app.post("/contact", response_model=ContactResponse)
async def submit_contact(payload: Contact) -> ContactResponse:
    try:
        await create_document("contact", payload.model_dump())
        return ContactResponse(success=True, message="Thanks! Your message has been received.")
    except Exception as e:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/contacts", response_model=List[Contact])
async def list_contacts(limit: int = 50) -> List[Contact]:
    docs = await get_documents("contact", limit=limit)
    # Convert to Contact models (drops _id for response simplicity)
    return [Contact(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
