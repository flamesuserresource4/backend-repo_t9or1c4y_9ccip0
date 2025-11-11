import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection

# Environment variables provided by the platform
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: MongoClient = MongoClient(DATABASE_URL)
db = _client[DATABASE_NAME]


def _collection(name: str) -> Collection:
    return db[name]


def create_document(collection_name: str, data: Dict[str, Any]) -> str:
    now = datetime.utcnow()
    payload = {**data, "created_at": now, "updated_at": now}
    result = _collection(collection_name).insert_one(payload)
    return str(result.inserted_id)


def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
    cursor = _collection(collection_name).find(filter_dict or {}).limit(limit)
    docs = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])  # make JSON serializable
        docs.append(doc)
    return docs


def update_document(collection_name: str, filter_dict: Dict[str, Any], update_fields: Dict[str, Any]) -> int:
    update_fields["updated_at"] = datetime.utcnow()
    result = _collection(collection_name).update_many(filter_dict, {"$set": update_fields})
    return result.modified_count


def delete_document(collection_name: str, filter_dict: Dict[str, Any]) -> int:
    result = _collection(collection_name).delete_many(filter_dict)
    return result.deleted_count
