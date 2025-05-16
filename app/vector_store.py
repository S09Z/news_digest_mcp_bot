import pinecone
import logging
from typing import Dict

logger = logging.getLogger(__name__)

# ตั้งค่า Pinecone environment และ index ชื่อของคุณ
PINECONE_API_KEY = None
PINECONE_ENV = None
INDEX_NAME = "news-digest-context"

def init_pinecone(api_key: str, environment: str):
    global PINECONE_API_KEY, PINECONE_ENV
    PINECONE_API_KEY = api_key
    PINECONE_ENV = environment

    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    if INDEX_NAME not in pinecone.list_indexes():
        pinecone.create_index(INDEX_NAME, dimension=768)  # dimension ตามโมเดล embedding
    logger.info(f"Pinecone initialized and index '{INDEX_NAME}' ready.")

def save_context_to_pinecone(id: str, metadata: Dict, vector: list):
    """
    บันทึกข้อมูล vector + metadata ลง Pinecone index
    id: string ระบุเอกลักษณ์ข้อมูล
    metadata: ข้อมูลเสริม เช่น title, url, summary
    vector: embedding vector (list ของ float)
    """
    try:
        index = pinecone.Index(INDEX_NAME)
        index.upsert([(id, vector, metadata)])
        logger.info(f"Saved vector data with id={id} to Pinecone.")
    except Exception as e:
        logger.error(f"Failed to save data to Pinecone: {e}")
