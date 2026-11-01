import re
import sqlite3
from pathlib import Path

sql = Path("sql/queries.sql").read_text(encoding="utf-8")
queries = [chunk.strip() for chunk in sql.split(";") if chunk.strip()]
parameters = {
    1: (), 2: (70,), 3: (2500,), 4: (), 5: (), 6: (1,),
    7: ("2026-01-01",), 8: (50, "2026-01-01"), 9: (), 10: (),
    11: (0,), 12: (),
}
with sqlite3.connect("data/photo_studio.sqlite") as conn:
    for index, query in enumerate(queries, 1):
        rows = conn.execute(query, parameters[index]).fetchall()
        print(index, len(rows))
