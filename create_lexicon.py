import sys
from get_datasets import get_bag_of_words
import csv
import os

n = int(sys.argv[1])
data_train, data_test, stars_train, stars_test = get_bag_of_words(max_features=n)

if not os.path.exists("lexicons"):
    os.makedirs("lexicons")

with open("lexicons/lexicon-xtrain-" + str(n) + ".csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(data_train)

with open("lexicons/lexicon-xtest-" + str(n) + ".csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(data_test)

with open("lexicons/lexicon-ytrain-" + str(n) + ".csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerow(stars_train)

with open("lexicons/lexicon-ytest-" + str(n) + ".csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerow(stars_test)
