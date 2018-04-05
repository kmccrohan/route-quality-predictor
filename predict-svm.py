import numpy as np
import sqlite3
from sklearn import svm

def convert_to_numpy_array(query_results):
  as_2d_array = list(map(lambda x: list(x), query_results))
  return np.array(as_2d_array)

def get_data():
  conn = sqlite3.connect("routes.db")
  data = conn.cursor().execute("SELECT ROUND(stars), latitude, longitude, saftey, difficulty, Trad, Ice, Sport, TR, Alpine, Snow, Mixed, Aid, Boulder, Other FROM routes").fetchall()
  return convert_to_numpy_array(data)

def main():
  route_data = get_data()
  stars = route_data[:, 0]
  data = route_data[:, 1:]

  clf = svm.SVC()
  clf.fit(data, stars)


main()
