import requests
import logging
from news_digest_mcp_bot.utils.constant import NEWS_API_BASE_URL, NEWS_API_LANGUAGE, NEWS_API_LIMIT

logger = logging.getLogger(__name__)

def fetch_latest_news(api_key: str, max_articles: int = 5):
    """
    ดึงข่าวล่าสุดจาก TheNewsAPI.com
    คืนค่าเป็น list ของ dict ข่าว
    """
    url = NEWS_API_BASE_URL
    params = {
        "api_token": api_key,
        "language": NEWS_API_LANGUAGE,
        "limit": NEWS_API_LIMIT,
        "sort": "published_at",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = data.get("data", [])
        logger.info(f"Fetched {len(articles)} news articles.")
        return articles
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return []
