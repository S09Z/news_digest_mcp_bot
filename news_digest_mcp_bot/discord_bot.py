import requests
import logging

logger = logging.getLogger(__name__)

def send_discord_message(webhook_url: str, content: str) -> bool:
    """
    ส่งข้อความ content ไป Discord ผ่าน webhook_url
    คืนค่า True/False แสดงสถานะสำเร็จ
    """
    data = {
        "content": content,
        "allowed_mentions": {"parse": []},  # ป้องกันการ mention ทุกคน
    }

    try:
        response = requests.post(webhook_url, json=data, timeout=10)
        if response.status_code == 204:
            logger.info("Message sent to Discord successfully.")
            return True
        else:
            logger.error(f"Failed to send message to Discord. Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Exception sending Discord message: {e}")
        return False
