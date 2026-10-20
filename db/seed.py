import psycopg2
import json
import os 
import dotenv

from connection import get_db_connection

conn = get_db_connection()
cur = conn.cursor()


with open('db/tables.sql', 'r') as file:
    sql_content = file.read()
    cur.execute(sql_content)

with open ("db/data/users.json") as f: 
    users_data = json.load(f)

with open("db/data/events.json") as f: 
    events_data = json.load(f)

with open("db/data/rsvps.json") as f: 
    rsvps_data = json.load(f)

with open("db/data/venues.json") as f: 
    venues_data = json.load(f)  

for user in users_data: 
    cur.execute(
        """INSERT INTO users (email, password, name) 
        VALUES (%s, %s, %s)""", 
        (user["email"], user["password"], user["name"])
    )

for venue in venues_data: 
    cur.execute(
        """INSERT INTO venues (name, address, capacity) 
        VALUES (%s, %s, %s)""", 
        (venue["name"], venue["address"], venue["capacity"])
    )

for event in events_data: 
    cur.execute(
        """INSERT INTO events (title, description, starts_at, ends_at, organiser_id, venue_id)
        VALUES (%s, %s, %s, %s, %s, %s)""", 
        (event["title"], event["description"], event["starts_at"], event["ends_at"], event["organiser_id"], event["venue_id"])
    )

for rsvp in rsvps_data: 
    cur.execute(
        """INSERT INTO rsvps (attendee_id, event_id)
        VALUES (%s, %s)""", 
        (rsvp["attendee_id"], rsvp["event_id"])
    )

conn.commit()
conn.close()
conn.close()
