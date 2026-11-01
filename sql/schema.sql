PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS studios (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    area INTEGER NOT NULL,
    price_per_hour REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    login TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    studio_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    booking_date TEXT NOT NULL,
    start_hour INTEGER NOT NULL,
    end_hour INTEGER NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0,
    total_price REAL NOT NULL,
    FOREIGN KEY (studio_id) REFERENCES studios(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
