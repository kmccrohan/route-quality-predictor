import sqlite3

conn = None

def setup_database():
    global conn
    conn = sqlite3.connect("routes.db")

def close_database():
    global conn
    conn.close()

def add_test_column():
    conn.cursor().execute('ALTER TABLE routes ADD COLUMN test INT NOT NULL DEFAULT 0')
    conn.commit()

setup_database()
add_test_column()
close_database()
