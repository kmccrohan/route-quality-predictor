import csv

def read_lexicon(max_features):
    x_train = list(csv.reader(open("lexicons/lexicon-xtrain-" + str(max_features) + ".csv")))
    y_train = list(csv.reader(open("lexicons/lexicon-ytrain-" + str(max_features) + ".csv")))
    x_test = list(csv.reader(open("lexicons/lexicon-xtest-" + str(max_features) + ".csv")))
    y_test = list(csv.reader(open("lexicons/lexicon-ytest-" + str(max_features) + ".csv")))
    y_test = [int(y) for y in y_test[0]]
    x_train = [[float(x2) for x2 in x] for x in x_train]
    y_train = [int(y) for y in y_train[0]]
    x_test = [[float(x2) for x2 in x] for x in x_test]
    return x_train, x_test, y_train, y_test
