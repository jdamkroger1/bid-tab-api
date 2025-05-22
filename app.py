from flask import Flask
import psycopg2
import os

app = Flask(__name__)

@app.route("/")
def home():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT"),
        )
        conn.close()
        return "✅ Successfully connected to the database!"
    except Exception as e:
        return f"❌ Database connection failed:<br><pre>{e}</pre>"
Add test app.py for database connection
