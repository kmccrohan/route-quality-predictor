from sklearn import svm
from sklearn.metrics import accuracy_score
from get_datasets import get_datasets
import sys

def main():

  types = None
  args = sys.argv
  bi = False
  if "-b" in sys.argv:
      bi = True
      args.remove("-b")
  if len(args) > 1:
      types = sys.argv[1].split(',')
  data_train, data_test, stars_train, stars_test = get_datasets(types=types)
  print("Training size: %d" % len(data_train))

  if bi:
      stars_train, stars_test = binary_stars(stars_train, stars_test)

  clf = svm.SVC()
  clf.fit(data_train, stars_train)
  predictions = clf.predict(data_test)
  print("Accuracy: %f\n" % accuracy_score(stars_test, predictions))

main()
