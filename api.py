import re
import requests
import sqlite3
import json
import time

conn = None
CHUNK_SIZE = 100

def setup_database():
    global conn
    conn = sqlite3.connect("routes.db")

def close_database():
    global conn
    conn.close()

def query_routes(ids):
    try:
        url = "https://www.mountainproject.com/data/get-routes?routeIds=" + ','.join(ids) + "&&key=200141500-3a451ba2c98e95d4945db023a65ea3d2"
        return requests.get(url).json()
    except requests.exceptions.RequestException as e:
        print(e)
        return None

def add_json(jsons):
    cur = conn.cursor()
    for route in jsons["routes"]:
        cur.execute('UPDATE routes SET api = ? WHERE mountain_project_id = ?', [json.dumps(route), route["id"]])
    conn.commit()

def loop_routes():
    chunk_size = 160
    cur = conn.cursor()
    cur.execute('SELECT mountain_project_id FROM routes WHERE api is NULL')
    while True:
        result = cur.fetchmany(CHUNK_SIZE)
        ids = [r[0] for r in result]
        if not result:
            exit()
        else:
             jsons = query_routes(ids)
             if jsons is not None:
                 add_json(jsons)
                 time.sleep(5)

setup_database()
loop_routes()
close_database()
