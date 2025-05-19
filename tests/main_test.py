import pytest
from news_digest_mcp_bot.news_api import fetch_latest_news
from news_digest_mcp_bot.summarizer import summarize_text
from news_digest_mcp_bot.discord_bot import send_discord_message

def test_fetch_latest_news(monkeypatch):
    # Mock requests.get ให้คืนค่าข่าวตัวอย่าง
    class MockResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return {
                "data": [
                    {"title": "Test News", "content": "Some content", "url": "http://example.com"}
                ]
            }

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    news = fetch_latest_news("fake_api_key", max_articles=1)
    assert len(news) == 1
    assert news[0]["title"] == "Test News"

def test_summarize_text(monkeypatch):
    # Mock requests.post คืน summary
    class MockResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return [{"summary_text": "Short summary"}]

    def mock_post(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)
    summary = summarize_text("Long content here", "fake_token")
    assert summary == "Short summary"

def test_send_discord_message(monkeypatch):
    class MockResponse:
        status_code = 204
        text = ""

    def mock_post(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)
    success = send_discord_message("fake_webhook_url", "Hello")
    assert success is True
