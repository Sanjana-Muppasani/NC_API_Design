from fastapi import APIRouter, HTTPException
from db.connection import get_db_connection
from src.models.event_models import EventDetailResponse, EventsResponse

router = APIRouter()

@router.get("/api/events", response_model=EventsResponse)
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


@router.get("/api/events/{id}",response_model=EventDetailResponse)
def get_event_by_event_id(id):

    try:
        id = int(id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="ID must be int"
        )

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
                    SELECT
                        e.id,
                        e.title,
                        e.description,
                        e.starts_at,
                        e.ends_at,
                        v.name AS location,
                        v.address,
                        v.capacity,
                        e.created_at
                    FROM events AS e
                    INNER JOIN venues AS v
                        ON e.venue_id = v.id
                    WHERE e.id = %s
                """, (id,))

        columns = [desc[0] for desc in cur.description]
        row = cur.fetchone()

        if row is None:
            raise HTTPException(status_code=404,detail="Event not found")
        event = dict(zip(columns, row))
        return {"event": event}

    finally:
        cur.close()
        conn.close()