# vector_store.py

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, CollectionStatus
from typing import List
import hashlib
import os

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "news_digest_collection"

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def setup_collection():
    if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )

def store_vector(id: str, vector: List[float], payload: dict):
    point = PointStruct(id=int(hashlib.md5(id.encode()).hexdigest(), 16) % (10**10), vector=vector, payload=payload)
    client.upsert(collection_name=COLLECTION_NAME, points=[point])

def search_vector(query_vector: List[float], top_k=5):
    results = client.search(collection_name=COLLECTION_NAME, query_vector=query_vector, limit=top_k)
    return results
