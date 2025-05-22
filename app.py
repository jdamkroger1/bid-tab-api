from flask import Flask, request, jsonify
import psycopg2
import os
import statistics

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT"),
    )

@app.route("/")
def home():
    return "✅ Successfully connected to the database!"

@app.route("/items", methods=["GET"])
def get_item_stats():
    item = request.args.get("item")
    year = request.args.get("year", type=int)
    stat = request.args.get("stat", default="average")

    if not item or not year:
        return jsonify({"error": "Missing item or year"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT unit_price FROM bid_items
            WHERE item_description = %s AND year = %s
        """, (item, year))
        prices = [float(row[0]) for row in cur.fetchall()]
        cur.close()
        conn.close()

        if not prices:
            return jsonify({"item": item, "year": year, "result": None})

        result = {
            "average": sum(prices) / len(prices),
            "median": statistics.median(prices),
            "count": len(prices)
        }.get(stat, None)

        return jsonify({"item": item, "year": year, f"{stat}_price": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
