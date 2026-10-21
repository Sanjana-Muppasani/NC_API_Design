from fastapi import APIRouter, HTTPException
from db.connection import get_db_connection
from models.event_models import EventResponse, EventsResponse

router = APIRouter()

@router.get("/api/events")
def get_all_events(): 
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
            SELECT
                e.id,
                e.title,
                e.starts_at,
                e.ends_at,
                v.address
            FROM events AS e
            LEFT JOIN venues AS v
                ON e.venue_id = v.id
            ORDER BY
                e.starts_at ASC,
                e.id ASC
        """)
    rows = cur.fetchall()

    events = [
            {
                "id": row[0],
                "title": row[1],
                "starts_at": row[2],
                "ends_at": row[3],
                "location": row[4],
            }
            for row in rows
        ]

    cur.close()
    conn.close()
    return {"events": events}