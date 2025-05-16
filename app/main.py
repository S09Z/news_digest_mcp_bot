import os
import logging
from app.news_api import fetch_latest_news
from app.summarizer import summarize_text
from app.discord_bot import send_discord_message
# from app.vector_store import save_context_to_pinecone  # placeholder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # โหลดค่า ENV
    news_api_key = os.getenv("THENEWS_API_KEY")
    discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
    hf_api_token = os.getenv("HF_API_TOKEN")

    if not news_api_key or not discord_webhook or not hf_api_token:
        logger.error("Missing one or more required environment variables.")
        return

    # 1. ดึงข่าวล่าสุด
    logger.info("Fetching latest news...")
    news_items = fetch_latest_news(api_key=news_api_key, max_articles=5)
    if not news_items:
        logger.warning("No news fetched.")
        return

    for news in news_items:
        title = news.get("title", "No title")
        content = news.get("content") or news.get("description") or ""
        url = news.get("url", "")

        # 2. สรุปข่าวด้วย BART model
        logger.info(f"Summarizing news: {title}")
        summary = summarize_text(content, hf_api_token)

        # 3. บันทึกบริบทและข่าว (placeholder)
        # save_context_to_pinecone(title=title, summary=summary, url=url)

        # 4. เตรียมข้อความส่งไป Discord
        message = f"**{title}**\n\n{summary}\n\n[Read more]({url})"

        # 5. ส่งข้อความไป Discord
        logger.info(f"Sending summarized news to Discord: {title}")
        success = send_discord_message(webhook_url=discord_webhook, content=message)

        if not success:
            logger.error(f"Failed to send message for news: {title}")

if __name__ == "__main__":
    main()
