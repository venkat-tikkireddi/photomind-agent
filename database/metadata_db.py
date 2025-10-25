import sqlite3
import json

def create_tables(db_path="photos.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Photo metadata
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT,
            phash TEXT,
            sha256 TEXT,
            timestamp TEXT
        )
    """)
    # Faces
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            face_id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo_path TEXT,
            bbox TEXT,
            embedding TEXT
        )
    """)
    # Events/milestones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo_path TEXT,
            event_tag TEXT,
            score REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_photo_meta(meta_path, db_path="photos.db"):
    with open(meta_path, "r") as f:
        photos = json.load(f)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for photo in photos:
        cursor.execute(
            "INSERT INTO photos (path, phash, sha256, timestamp) VALUES (?, ?, ?, ?)",
            (photo["path"], photo["phash"], photo["sha256"], photo["timestamp"])
        )
    conn.commit()
    conn.close()

def insert_face_meta(face_path, db_path="photos.db"):
    with open(face_path, "r") as f:
        faces = json.load(f)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for face in faces:
        cursor.execute(
            "INSERT INTO faces (photo_path, bbox, embedding) VALUES (?, ?, ?)",
            (face["photo_path"], json.dumps(face["bbox"]), json.dumps(face["embedding"]))
        )
    conn.commit()
    conn.close()

def insert_event_meta(event_path, db_path="photos.db"):
    with open(event_path, "r") as f:
        events = json.load(f)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for event in events:
        cursor.execute(
            "INSERT INTO events (photo_path, event_tag, score) VALUES (?, ?, ?)",
            (event["photo_path"], event["event_tag"], event["score"])
        )
    conn.commit()
    conn.close()

def get_distinct_faces(db_path="photos.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT embedding FROM faces")
    faces = [row[0] for row in cursor.fetchall()]
    conn.close()
    # Here you'd run clustering logic (e.g., k-means), see next steps

def get_event_groups(db_path="photos.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT event_tag, COUNT(*) FROM events GROUP BY event_tag ORDER BY COUNT(*) DESC")
    groups = cursor.fetchall()
    conn.close()
    return groups


if __name__ == "__main__":
    create_tables()
    insert_photo_meta("photo_meta.json")
    insert_face_meta("face_meta.json")
    insert_event_meta("event_tags.json")
    print("Loaded all metadata into photos.db")
