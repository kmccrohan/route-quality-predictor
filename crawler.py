import re
import requests
import sqlite3

MAX_ROUTES = 100
routesVisited = set()
routes = 0
areasVisited = set()

def setup_database():
    conn = sqlite3.connect("routes.db")
    c = conn.cursor().execute("CREATE TABLE IF NOT EXISTS routes (id INTEGER PRIMARYKEY, html TEXT, mountain_project_id VARCHAR(255))")
    conn.commit()
    conn.close()


def downloadRoute(url):
    print("Route: " + url)
    # download route and add route to database
    
    # exit if max number of routes reached
    global routes
    routes += 1
    if routes == MAX_ROUTES:
        exit()

def crawlPage(html):
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', html)
    for url in urls:
        if url.startswith("https://www.mountainproject.com/area/"):
            if url not in areasVisited:
                areasVisited.add(url)
                print("Visiting area: " + url)
                crawlPage(str(requests.get(url).content))
        elif url.startswith("https://www.mountainproject.com/route/"):
            if url not in routesVisited:
                routesVisited.add(url)
                downloadRoute(url)

setup_database()
r = requests.get("https://www.mountainproject.com")
crawlPage(str(r.content))
