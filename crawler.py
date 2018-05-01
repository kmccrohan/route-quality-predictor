import re
import requests
import sqlite3

MAX_ROUTES = 75000
routesVisited = set()
routes = 0
areasVisited = set()
conn = None

def load_set():
    global conn
    global routesVisited

    routes = conn.cursor().execute("SELECT mountain_project_id FROM routes").fetchall()
    for route in routes:
        routesVisited.add(route[0])

def close_database():
    global conn
    conn.close()

def setup_database():
    global conn

    conn = sqlite3.connect("routes.db")
    c = conn.cursor().execute("CREATE TABLE IF NOT EXISTS routes (id INTEGER PRIMARYKEY, html TEXT, mountain_project_id VARCHAR(255), url TEXT, api TEXT)")
    conn.commit()

def downloadRoute(url, id):
    print("Route: " + url)
    # download route and add route to database
    try:
        html_data = str(requests.get(url).content)

        global conn
        conn.cursor().execute("INSERT INTO routes (html, mountain_project_id, url) VALUES (?,?,?)", (html_data, route_id, url))
        conn.commit()

        # exit if max number of routes reached
        global routes
        routes += 1
        if routes == MAX_ROUTES:
            close_database()
            exit()
    except requests.exceptions.RequestException as e:
        print(e)


def crawlPage(html):
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', html)
    for url in urls:
        if url.startswith("https://www.mountainproject.com/area/"):
            if url not in areasVisited:
                areasVisited.add(url)
                print("Visiting area: " + url)
                try:
                    pageHTML = str(requests.get(url).content)
                    crawlPage(pageHTML)
                except requests.exceptions.RequestException as e:
                    print(e)
        elif url.startswith("https://www.mountainproject.com/route/"):
            route_id = re.findall(r'[0-9]+', url)[0]
            if route_id not in routesVisited:
                routesVisited.add(route_id)
                downloadRoute(url, route_id)

setup_database()
load_set()
r = requests.get("https://www.mountainproject.com")
crawlPage(str(r.content))
close_database()
