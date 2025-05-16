# ใช้ official Python 3.10 image
FROM python:3.10-slim

# ตั้ง working directory
WORKDIR /app

# ติดตั้ง dependencies
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# คัดลอกโค้ดแอปทั้งหมด
COPY . /app

# ENV vars (แนะนำตั้งใน docker-compose หรือ runtime)
ENV PYTHONUNBUFFERED=1

# รัน main.py เมื่อ container start
CMD ["python", "main.py"]
