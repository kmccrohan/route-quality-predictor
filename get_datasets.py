import numpy as np
import sqlite3
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

lemmer=WordNetLemmatizer()
stemmer = SnowballStemmer('english')

def convert_to_numpy_array(query_results):
  as_2d_array = list(map(lambda x: list(x), query_results))
  return np.array(as_2d_array)

def get_data(types, attrs):
  conn = sqlite3.connect("routes.db")
  attr_clause = "latitude, longitude, saftey, difficulty, description_length, Trad, Ice, Sport, TR, Alpine, Snow, Mixed, Aid, Boulder, Other"
  where_clause = "test = 0"
  if types is not None:
      types = [ " %s = 1" % t for t in types]
      where_clause += " AND ("
      where_clause += " OR ".join(types)
      where_clause += ")"
      attr_clause = "latitude, longitude, saftey, difficulty, description_length"
  if attrs is not None:
      attr_clause = ", ".join(attrs)
  query = ("SELECT ROUND(stars), %s FROM routes" % attr_clause)
  if where_clause is not None:
      query += " WHERE " + where_clause
  data = conn.cursor().execute(query).fetchall()
  conn.close()
  return convert_to_numpy_array(data)

def get_datasets(types=None, attrs=None,):
   route_data = get_data(types, attrs)
   stars = route_data[:, 0]
   data = route_data[:, 1:]
   return train_test_split(data, stars, test_size=0.20)

def binary_stars(stars_train, stars_test):
    return [1 if x > 3 else 0 for x in stars_train], [1 if x > 3 else 0 for x in stars_test]

def lemmatize_stem(data):
    for d in data:
        d[1] = ' '.join([stemmer.stem(word) for word in d[1].split(' ')])
        d[1] = ' '.join([lemmer.lemmatize(word) for word in d[1].split(' ')])
    return data

def get_words(types):
    route_data = get_data(types, attrs=["description"])
    route_data = np.array([np.array(x) for x in route_data if x[1] is not None and x[1] is not ""])
    route_data = lemmatize_stem(route_data)
    stars = route_data[:, 0]
    stars = [int(float(s)) for s in stars]
    data = route_data[:, 1:]
    data = np.array([d[0] for d in data])
    return train_test_split(data, stars, test_size=0.20)

def tfid(bag):
    tfidf_transformer = TfidfTransformer()
    return tfidf_transformer.fit_transform(bag)

def get_bag_of_words(types=None, max_features=100):
    vectorizer = CountVectorizer(stop_words="english", max_features=max_features)
    xtrain, xtest, ytrain, ytest = get_words(types)
    X = vectorizer.fit_transform(xtrain)
    X = tfid(X)
    testVectorizer = CountVectorizer(vocabulary=vectorizer.get_feature_names())
    X_test = testVectorizer.fit_transform(xtest)
    X_test = tfid(X_test)

    return X.toarray(), X_test.toarray(), ytrain, ytest
