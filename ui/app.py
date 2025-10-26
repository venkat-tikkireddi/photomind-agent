import streamlit as st
import sqlite3
import os
import shutil
import hashlib

DB_PATH = "../photos.db"  # Update path if needed
DEST_ROOT = "organized_photos"     # Output folder, can edit

def fetch_events_and_photos(db_path=DB_PATH):
    # resolve relative path to this file
    if not os.path.isabs(db_path):
        db_path = os.path.join(os.path.dirname(__file__), db_path)
        #print(f"Resolved DB path: {db_path}")

    # no DB file => return empty results
    if not os.path.exists(db_path):
        #print(f"Database file not found at {db_path}")
        return [], {}

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # ensure events table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
        if not cursor.fetchone():
            return [], {}

        cursor.execute("SELECT event_tag, COUNT(*) FROM events GROUP BY event_tag ORDER BY COUNT(*) DESC")
        events_summary = cursor.fetchall()

        cursor.execute("SELECT photo_path, event_tag FROM events")
        photo_groups = {}
        for photo_path, event_tag in cursor.fetchall():
            photo_groups.setdefault(event_tag, []).append(photo_path)

        return events_summary, photo_groups
    except sqlite3.DatabaseError:
        return [], {}
    finally:
        if conn:
            conn.close()

def organize_photos(group, photo_paths, dest_root=DEST_ROOT):
    group_folder = os.path.join(dest_root, group)
    os.makedirs(group_folder, exist_ok=True)
    for photo in photo_paths:
        if os.path.exists(photo):
            shutil.copy2(photo, group_folder)

def main():
    st.title("PhotoMind Agent: Smart Album Organizer")

    # Instructions for user
    st.info("""
        **Instructions:**
        1. Review the suggested photo groups/albums.
        2. Organize them with a click.
        3. Add custom labels/tags for better filtering and search.
    """)

    events_summary, photo_groups = fetch_events_and_photos(DB_PATH)

    if not events_summary:
        st.warning("No database or no 'events' table found. Create/populate photos.db or update DB_PATH before organizing photos.")
        return

    st.header("Agent-Suggested Photo Groups")
    for event_tag, count in events_summary:
        with st.expander(f"{event_tag} ({count} photos)"):
            photos = photo_groups.get(event_tag, [])
            for idx, photo in enumerate(photos):
                if os.path.exists(photo):
                    st.image(photo, width=150)
                    # create a short, stable unique key per photo widget to avoid duplicates
                    short_hash = hashlib.md5(photo.encode("utf-8")).hexdigest()[:8]
                    tag_key = f"{event_tag}_{idx}_{short_hash}"
                    tag = st.text_input(f"Tag for {os.path.basename(photo)}", key=tag_key)
                    if tag:
                        st.write(f"Tag saved: {tag}")  # You can expand this to save tags in DB!
            if st.button(f"Organize '{event_tag}' Album", key=f"organize_{event_tag}"):
                organize_photos(event_tag, photos)
                st.success(f"Album for '{event_tag}' created in {DEST_ROOT}!")

    if st.button("Create Master Album", key="create_master_album"):
        master_folder = os.path.join(DEST_ROOT, "Master_Album")
        os.makedirs(master_folder, exist_ok=True)
        for photos in photo_groups.values():
            for photo in photos:
                if os.path.exists(photo):
                    shutil.copy2(photo, master_folder)
        st.success("Master Album created!")

if __name__ == "__main__":
    main()