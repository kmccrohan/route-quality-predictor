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
    i = 0
    for route in result:
        test = 0 if i < 80000 else 1
        i += 1
        #test = random.choice([0,0,0,0,1])
        cur.execute('UPDATE routes SET test = ? WHERE mountain_project_id = ?', [test, route[0]])
    conn.commit()

setup_database()
loop_routes()
close_database()
