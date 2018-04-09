from sklearn import neighbors
from sklearn.metrics import accuracy_score
from get_datasets import get_datasets
import sys

def main():

   data_train, data_test, stars_train, stars_test = get_datasets(attrs=["latitude","longitude"])
   print("Training size: %d" % len(data_train))

   knn=neighbors.KNeighborsClassifier(n_neighbors=int(sys.argv[1]))
   knn.fit(data_train, stars_train)
   predictions = knn.predict(data_test)
   print("Accuracy: %f\n" % accuracy_score(stars_test, predictions))

main()
