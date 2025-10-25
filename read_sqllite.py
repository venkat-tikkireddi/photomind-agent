import sqlite3
conn = sqlite3.connect("photos.db")
cursor = conn.cursor()

print("Photos:")
for row in cursor.execute("SELECT * FROM photos LIMIT 5"):
    print(row)

print("\nFaces:")
for row in cursor.execute("SELECT * FROM faces LIMIT 5"):
    print(row)

print("\nEvents:")
for row in cursor.execute("SELECT * FROM events LIMIT 5"):
    print(row)

conn.close()
