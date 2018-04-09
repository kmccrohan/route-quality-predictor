import numpy as np
import sqlite3
from sklearn import datasets
from sklearn.model_selection import train_test_split

def convert_to_numpy_array(query_results):
  as_2d_array = list(map(lambda x: list(x), query_results))
  return np.array(as_2d_array)

def get_data(types, attrs):
  conn = sqlite3.connect("routes.db")
  attr_clause = "latitude, longitude, saftey, difficulty, Trad, Ice, Sport, TR, Alpine, Snow, Mixed, Aid, Boulder, Other"
  where_clause = None
  if types is not None:
      types = [ " %s = 1" % t for t in types]
      where_clause = " OR ".join(types)
      attr_clause = "latitude, longitude, saftey, difficulty"
  if attrs is not None:
      attr_clause = ", ".join(attrs)
  query = ("SELECT ROUND(stars), %s FROM routes" % attr_clause)
  if where_clause is not None:
      query += " WHERE " + where_clause
  data = conn.cursor().execute(query).fetchall()
  return convert_to_numpy_array(data)

def get_datasets(types=None, attrs=None,):
   route_data = get_data(types, attrs)
   stars = route_data[:, 0]
   data = route_data[:, 1:]
   return train_test_split(data, stars, test_size=0.20)
