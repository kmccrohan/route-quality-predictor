import sqlite3

def setup_database():
    global conn
    conn = sqlite3.connect("routes.db")

def close_database():
    global conn
    conn.close()


setup_database()
duplicates = conn.cursor().execute("SELECT mountain_project_id FROM routes GROUP BY (mountain_project_id) HAVING COUNT(*) > 1").fetchall()
for dup in duplicates:
    id = dup[0]
    conn.cursor().execute("DELETE FROM routes WHERE url = (SELECT url FROM routes WHERE mountain_project_id=? LIMIT 1)", id)
conn.commit()
close_database()
