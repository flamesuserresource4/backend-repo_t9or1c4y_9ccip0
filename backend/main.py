from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os

from database import db, create_document, get_documents

app = FastAPI(title="NovaPlay API")

# CORS for frontend preview
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*" if FRONTEND_URL == "*" else FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "NovaPlay backend is running"}


@app.get("/test")
async def test_db():
    try:
        # try a simple ping and list collections
        collections = await_list_collections()
        return {
            "backend": "ok",
            "database": "ok",
            "database_url": os.getenv("DATABASE_URL"),
            "database_name": os.getenv("DATABASE_NAME"),
            "connection_status": "connected",
            "collections": collections,
        }
    except Exception as e:
        return {
            "backend": "ok",
            "database": "error",
            "error": str(e),
        }


def await_list_collections() -> List[str]:
    try:
        return sorted(db.list_collection_names())
    except Exception:
        return []


class Lead(BaseModel):
    email: str
    source: str = "landing"


@app.post("/leads")
async def capture_lead(lead: Lead):
    lead_id = create_document("leads", lead.model_dump())
    return {"status": "ok", "id": lead_id}
