# News Digest MCP Bot

โปรเจกต์นี้เป็น **AI News Research Assistant** ที่ดึงข่าวจาก TheNewsAPI.com, สรุปด้วยโมเดล Huggingface `facebook/bart-large-cnn` และส่งข่าวสรุปไปยัง Discord ผ่าน Webhook  
โดยใช้แนวทาง Model Context Protocol (MCP) และรองรับการบันทึกบริบทผู้ใช้ด้วย Pinecone Vector DB (ยังพัฒนาเพิ่ม)

---

## Project Workspace Structure
```
news-digest-mcp-bot/
│
├── README.md # ไฟล์นี้ - อธิบายโปรเจกต์และการใช้งาน
├── pyproject.toml # Config ของ Poetry (dependencies, metadata)
├── poetry.lock # Lock file สำหรับเวอร์ชัน dependencies
├── .gitignore # ไฟล์ ignore สำหรับ git
│
├── news_digest_mcp_bot/ # โฟลเดอร์ source code หลัก (Python package)
│ ├── init.py
│ ├── main.py # สคริปต์หลักรันโปรเจกต์
│ ├── news_api.py # ดึงข่าวจาก TheNewsAPI
│ ├── summarizer.py # สรุปข่าวด้วย Huggingface BART model
│ ├── discord_bot.py # ส่งข้อความข่าวไป Discord Webhook
│ └── utils.py # ฟังก์ชันช่วยเหลือทั่วไป
│
├── tests/ # เก็บ unit test (ถ้ามี)
│ ├── init.py
│ └── test_main.py
│
└── data/ # เก็บข้อมูลเสริม เช่น log หรือข่าวเก่า (ถ้ามี)
```

---

## Environment Variables (ENV)

โปรเจกต์นี้ใช้ตัวแปรแวดล้อม (Environment Variables) ดังนี้:

| ชื่อ ENV Variable     | คำอธิบาย                                   |
|----------------------|--------------------------------------------|
| `THENEWS_API_KEY`     | API Key สำหรับ TheNewsAPI.com                |
| `DISCORD_WEBHOOK_URL` | URL สำหรับส่ง Webhook ไป Discord           |
| `HF_API_TOKEN`        | Token สำหรับเรียก Huggingface Inference API |

สามารถตั้งค่า ENV เหล่านี้ได้ผ่านไฟล์ `.env` (ถ้าใช้ `python-dotenv`) หรือเซ็ตในระบบปฏิบัติการ

---

## Workflow Diagram (MCP Style)
```
+-------------------+
|   User Request    |
+---------+---------+
          |
          v
+-------------------+      +--------------------+
| Fetch News from   | ---> | Summarize News with |
| TheNewsAPI       |      | facebook/bart-large-cnn |
+---------+---------+      +----------+---------+
          |                           |
          v                           v
+-------------------+        +------------------+
|  Save Context &   |        |  Format Digest   |
|  News History     |        +---------+--------+
| (e.g. Pinecone)   |                  |
+---------+---------+                  v
          |                  +-------------------+
          +----------------> |  Send Digest to   |
                             |    Discord Bot    |
                             +-------------------+
```