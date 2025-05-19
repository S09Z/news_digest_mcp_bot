FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# ✅ คัดลอกเฉพาะไฟล์ config ก่อน เพื่อใช้ cache ได้ดี
COPY pyproject.toml poetry.lock* /app/

# ✅ ติดตั้ง dependencies แบบไม่มี virtualenv
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# ✅ คัดลอก source code หลังสุด เพื่อไม่ให้ cache invalidated
COPY . /app

ENV PYTHONPATH=/app


# ✅ ใช้ PYTHONPATH เฉพาะในขั้น run (ไม่ต้อง set ENV ถาวร)
CMD ["python", "news_digest_mcp_bot/main.py"]
