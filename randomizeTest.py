import sqlite3
import random

conn = None

def setup_database():
    global conn
    conn = sqlite3.connect("routes.db")

def close_database():
    global conn
    conn.close()

def loop_routes():
    cur = conn.cursor()
    cur.execute('SELECT mountain_project_id FROM routes')
    result = cur.fetchall()
    for route in result:
        test = random.choice([0,0,0,0,1])
        cur.execute('UPDATE routes SET test = ? WHERE mountain_project_id = ?', [test, route[0]])
    conn.commit()

setup_database()
loop_routes()
close_database()
