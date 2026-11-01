import sqlite3
from pathlib import Path

db = Path("data/photo_studio.sqlite")
with sqlite3.connect(db) as conn:
    conn.row_factory = sqlite3.Row
    print([row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")])
    print([dict(row) for row in conn.execute("SELECT COUNT(*) AS count FROM studios")])
    print([dict(row) for row in conn.execute("SELECT COUNT(*) AS count FROM users")])
    print([dict(row) for row in conn.execute("SELECT COUNT(*) AS count FROM bookings")])
    print([dict(row) for row in conn.execute("""SELECT b.id, s.name AS studio_name, u.login
        FROM bookings b JOIN studios s ON b.studio_id=s.id JOIN users u ON b.user_id=u.id
        WHERE b.is_cancelled=0 ORDER BY b.id""")])
    print([tuple(row) for row in conn.execute("PRAGMA foreign_key_list(bookings)")])
