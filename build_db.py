import argparse
import httpx
import json
import sqlite_utils


def build_tables(data, db):
    for key in data:
        db[key].insert_all(data[key], pk="id")

    db["guidebook_event"].transform(types={"locations": int, "tracks": int})
    db["guidebook_poi"].transform(types={"categories": int})
    # Foreign keys
    db["guidebook_event"].add_foreign_key("locations", "guidebook_location", "id")
    db["guidebook_event"].add_foreign_key("tracks", "guidebook_schedule", "id")
    db["guidebook_poi_category"].add_foreign_key("poi_id", "guidebook_poi", "id")
    db["guidebook_poi_category"].add_foreign_key(
        "poicategory_id", "guidebook_poicategory", "id"
    )
    db["guidebook_event_location"].add_foreign_key("event_id", "guidebook_event", "id")
    db["guidebook_event_location"].add_foreign_key(
        "location_id", "guidebook_location", "id"
    )
    db["guidebook_event_scheduleTrack"].add_foreign_key(
        "event_id", "guidebook_event", "id"
    )
    db["guidebook_event_scheduleTrack"].add_foreign_key(
        "schedule_id", "guidebook_schedule", "id"
    )
    db["guidebook_poi"].add_foreign_key("categories", "guidebook_poicategory", "id")
    db["guidebook_poi_location"].add_foreign_key("poi_id", "guidebook_poi", "id")
    db["guidebook_poi_location"].add_foreign_key(
        "location_id", "guidebook_location", "id"
    )

    # Extract out a poi_sessions table
    for poi in db["guidebook_poi"].rows:
        session_ids = extract_session_ids(poi["links"])
        if session_ids:
            db["poi_sessions"].insert_all(
                (
                    {"event_id": session_id, "poi_id": poi["id"]}
                    for session_id in session_ids
                ),
                foreign_keys=[
                    ("event_id", "guidebook_event", "id"),
                    ("poi_id", "guidebook_poi", "id"),
                ],
            )

    # Configure search
    db["guidebook_event"].enable_fts(["name", "description"])
    db["guidebook_poi"].enable_fts(["name", "description"])


def extract_session_ids(links_cell):
    if not links_cell:
        return []
    links = json.loads(links_cell)
    try:
        sessions = [
            block["links"] for block in links if block["categoryTitle"] == "Sessions"
        ][0]
    except IndexError:
        return []
    return [s["target_object_id"] for s in sessions]


if __name__ == "__main__":
    # Use argparse to get db_path and json_path arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("db_path", help="Path to the database file")
    parser.add_argument(
        "json_path", help="Path to the JSON file", type=argparse.FileType("r")
    )
    args = parser.parse_args()
    db_path = args.db_path

    db = sqlite_utils.Database(args.db_path)
    data = json.load(args.json_path)
    build_tables(data, db)
