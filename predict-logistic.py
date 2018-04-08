from sklearn import linear_model
from sklearn.metrics import accuracy_score
from get_datasets import get_datasets


def main():

   data_train, data_test, stars_train, stars_test = get_datasets()
   print("Training size: %d" % len(data_train))

   logreg = linear_model.LogisticRegression()
   logreg.fit(data_train, stars_train)
   predictions = logreg.predict(data_test)
   print("Accuracy: %f\n" % accuracy_score(stars_test, predictions))
   print("Coef for each class and each attribute:\n")
   print(logreg.coef_)
   print("Summed coefficients:\n")
   print(logreg.coef_.sum(axis=0))

main()
