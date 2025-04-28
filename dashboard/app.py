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