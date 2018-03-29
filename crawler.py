import re
import requests

MAX_ROUTES = 100
routesVisited = set()
routes = 0
areasVisited = set()

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

r = requests.get("https://www.mountainproject.com")
crawlPage(str(r.content))
