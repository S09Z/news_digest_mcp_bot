import requests
import logging

logger = logging.getLogger(__name__)

def summarize_text(text: str, hf_api_token: str) -> str:
    """
    เรียก Huggingface Inference API ใช้ model facebook/bart-large-cnn
    เพื่อสรุปข้อความ input text
    """
    if not text.strip():
        return "No content to summarize."

    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {hf_api_token}"}
    payload = {"inputs": text, "parameters": {"min_length": 30, "max_length": 130}}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        result = response.json()

        # API response เป็น list ของ dict {'summary_text': ...}
        summary = result[0].get("summary_text", "") if isinstance(result, list) else ""
        if not summary:
            return "Failed to generate summary."
        return summary.strip()
    except Exception as e:
        logger.error(f"Error summarizing text: {e}")
        return "Error occurred during summarization."
