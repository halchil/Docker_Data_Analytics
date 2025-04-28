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