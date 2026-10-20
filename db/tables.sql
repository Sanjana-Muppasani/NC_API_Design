CREATE TABLE users(
    id SERIAL PRIMARY KEY, 
    email varchar(255) UNIQUE NOT NULL, 
    password varchar(255) NOT NULL, 
    name varchar(225) NOT NULL, 
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE venues(
    id SERIAL PRIMARY KEY, 
    name VARCHAR(225),
    address TEXT ,
    capacity INT
);


CREATE TABLE events(
    id SERIAL PRIMARY KEY, 
    title VARCHAR(255) NOT NULL, 
    description VARCHAR(225), 
    starts_at TIMESTAMPTZ NOT NULL,
    ends_at TIMESTAMPTZ NOT NULL,
    organiser_id INT REFERENCES users(id), --fk
    venue_id INT REFERENCES venues(id), --fk 
    created_at TIMESTAMPTZ DEFAULT NOW()

);

CREATE TABLE rsvps(
    id SERIAL PRIMARY KEY,
    attendee_id INT REFERENCES users(id), --foreign key
    event_id INT REFERENCES events(id),
    created_at TIMESTAMPTZ DEFAULT NOW() 
)