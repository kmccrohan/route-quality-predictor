from get_datasets import get_bag_of_words
from sklearn import svm
from sklearn.metrics import accuracy_score

def main():
  data_train, data_test, stars_train, stars_test = get_bag_of_words()
  print("Training size: %d" % len(data_train))

  clf = svm.SVC()
  clf.fit(data_train, stars_train)
  predictions = clf.predict(data_test)
  print("Accuracy: %f\n" % accuracy_score(stars_test, predictions))

main()
