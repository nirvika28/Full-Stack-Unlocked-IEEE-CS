from pathlib import Path

from flask import Flask, request, jsonify  # type: ignore[import-not-found]
import sqlite3


app = Flask(__name__)
DATABASE_PATH = Path(__file__).with_name("events.db")


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


# =================================
# DATABASE CONNECTION
# =================================

def get_db():

    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# =================================
# CREATE DATABASE TABLE
# =================================

def create_table():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            club TEXT NOT NULL,

            date TEXT NOT NULL,

            venue TEXT NOT NULL,

            description TEXT,

            registrations INTEGER DEFAULT 0

        )
    """)

    conn.commit()

    conn.close()


# Create table when server starts

create_table()


# =================================
# API HEALTH CHECK
# =================================

@app.route("/", methods=["GET"])
def health_check():

    return jsonify({
        "message": "College Event Tracker API is running."
    })


# =================================
# GET ALL EVENTS
# =================================

@app.route("/api/events", methods=["GET"])
def get_events():

    conn = get_db()

    events = conn.execute(
        "SELECT * FROM events"
    ).fetchall()

    conn.close()


    return jsonify([
        dict(event)
        for event in events
    ])


# =================================
# CREATE EVENT
# =================================

@app.route("/api/events", methods=["POST"])
def create_event():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON."}), 400

    required_fields = ("title", "club", "date", "venue")
    missing_fields = [
        field for field in required_fields
        if not isinstance(data.get(field), str) or not data[field].strip()
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "fields": missing_fields
        }), 400

    description = data.get("description", "")
    if not isinstance(description, str):
        return jsonify({"error": "Description must be text."}), 400


    conn = get_db()


    cursor = conn.execute("""
        INSERT INTO events
        (title, club, date, venue, description)

        VALUES (?, ?, ?, ?, ?)
    """, (

        data["title"].strip(),
        data["club"].strip(),
        data["date"].strip(),
        data["venue"].strip(),
        description.strip()

    ))


    conn.commit()


    event_id = cursor.lastrowid

    conn.close()


    return jsonify({
        "message": "Event created",
        "id": event_id
    }), 201


# =================================
# REGISTER FOR EVENT
# =================================

@app.route(
    "/api/events/<int:event_id>/register",
    methods=["POST"]
)
def register_event(event_id):

    conn = get_db()


    cursor = conn.execute("""
        UPDATE events

        SET registrations =
            registrations + 1

        WHERE id = ?
    """, (event_id,))


    conn.commit()

    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Event not found."}), 404


    return jsonify({
        "message": "Registration successful"
    })


# =================================
# START SERVER
# =================================

if __name__ == "__main__":

    app.run(
        port=5000,
        debug=True
    )