import requests

def parsePage(html):
    print(html)


r = requests.get("https://www.mountainproject.com/route/113768316/minutes-to-midnight")
parsePage(r.content)
