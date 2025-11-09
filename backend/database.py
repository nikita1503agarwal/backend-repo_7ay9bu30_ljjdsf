from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client = AsyncIOMotorClient(DATABASE_URL)
db: AsyncIOMotorDatabase = _client[DATABASE_NAME]


async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    data = {**data, "created_at": now, "updated_at": now}
    result = await db[collection_name].insert_one(data)
    return {"_id": str(result.inserted_id), **data}


async def get_documents(
    collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50
) -> List[Dict[str, Any]]:
    cursor = db[collection_name].find(filter_dict or {}).sort("created_at", -1).limit(limit)
    docs: List[Dict[str, Any]] = []
    async for doc in cursor:
        doc["_id"] = str(doc.get("_id"))
        docs.append(doc)
    return docs
