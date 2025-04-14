# 作成順

# システム構成図


# Docker_Data_Analytics


Docker_Data_Analytics/

├── scraper/

│   ├── Dockerfile

│   ├── requirements.txt

│   └── scraper.py

├── db/

│   └── docker-compose.yaml

├── dashboard/

│   ├── Dockerfile

│   ├── requirements.txt

│   └── app.py

└── shared/

│    └── .env



# db/docker-compose.yaml
version: '3.8'
services:
  db:
    image: postgres:13
    container_name: my_postgres
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - mynet

networks:
  mynet:
volumes:
  pgdata:

# scraper/Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY scraper.py .
CMD ["python", "scraper.py"]

# scraper/requirements.txt
requests
beautifulsoup4
psycopg2-binary

# scraper/scraper.py
import requests
from bs4 import BeautifulSoup
import psycopg2
import os

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME", "mydb"),
    user=os.getenv("DB_USER", "user"),
    password=os.getenv("DB_PASS", "password"),
    host=os.getenv("DB_HOST", "db"),
    port="5432"
)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS headlines (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL
    );
""")

response = requests.get("https://news.ycombinator.com")
soup = BeautifulSoup(response.text, "html.parser")
headlines = soup.select(".storylink")

for h in headlines:
    cur.execute("INSERT INTO headlines (title) VALUES (%s)", (h.text,))

conn.commit()
cur.close()
conn.close()

# dashboard/Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# dashboard/requirements.txt
streamlit
psycopg2-binary

# dashboard/app.py
import streamlit as st
import psycopg2
import os

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME", "mydb"),
    user=os.getenv("DB_USER", "user"),
    password=os.getenv("DB_PASS", "password"),
    host=os.getenv("DB_HOST", "db"),
    port="5432"
)
cur = conn.cursor()
cur.execute("SELECT title FROM headlines ORDER BY id DESC LIMIT 10;")
results = cur.fetchall()
cur.close()
conn.close()

st.title("最新ニュース")
for row in results:
    st.write("- ", row[0])

# shared/.env
DB_NAME=mydb
DB_USER=user
DB_PASS=password
DB_HOST=db



# 実行ステップ
① PostgreSQL 起動
```
cd db
docker-compose up -d
```

② スクレイパー実行（1回試す）

```
cd ../scraper
docker build -t news-scraper .
docker run --network=db_mynet --env-file ../shared/.env news-scraper
```

※ cron で定期実行したい場合はホスト側で cron ジョブに追加するか、別途 scheduler コンテナを組むのが理想です。
③ Streamlit ダッシュボード起動

```
cd ../dashboard
docker build -t news-dashboard .
docker run -p 8501:8501 --network=db_mynet --env-file ../shared/.env news-dashboard
```

→ ブラウザで http://localhost:8501 を開けば表示されます。