from bs4 import BeautifulSoup
import sqlite3

def main():

  connection = sqlite3.connect("routes.db")
  routes = connection.execute("SELECT html,url FROM routes")
  #connection.execute("ALTER TABLE routes ADD COLUMN description_length INT")
  for route in routes:
    html = route[0]
    soup = BeautifulSoup(html, "html.parser")
    description = soup.select_one(".fr-view")
    if description:
      raw_text = description.get_text()
      connection.execute("UPDATE routes SET description = ?, description_length = ? WHERE url = ?", (raw_text, len(raw_text), route[1]))
    else:
      connection.execute("UPDATE routes SET description = ?, description_length = ? WHERE url = ?", ("", 0,route[1]))

    connection.commit()

main()
