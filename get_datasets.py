import numpy as np
import sqlite3
from sklearn import datasets
from sklearn.model_selection import train_test_split

def convert_to_numpy_array(query_results):
  as_2d_array = list(map(lambda x: list(x), query_results))
  return np.array(as_2d_array)

def get_data(types):
  conn = sqlite3.connect("routes.db")
  data = None
  if types is None:
      data = conn.cursor().execute("SELECT ROUND(stars), latitude, longitude, saftey, difficulty, Trad, Ice, Sport, TR, Alpine, Snow, Mixed, Aid, Boulder, Other FROM routes").fetchall()
  else:
      types = [ " %s = 1" % t for t in types]
      where_clause = " OR ".join(types)
      data = conn.cursor().execute("SELECT ROUND(stars), latitude, longitude, saftey, difficulty FROM routes WHERE %s" % where_clause).fetchall()
  return convert_to_numpy_array(data)

def get_datasets(types=None):
   route_data = get_data(types)
   stars = route_data[:, 0]
   data = route_data[:, 1:]
   return train_test_split(data, stars, test_size=0.20)
