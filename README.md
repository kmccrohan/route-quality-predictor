# route-quality-predictor
Machine Learning to predict the quality of a climbing route based on various attributes, images, and descriptors.

## Binary classification
Note for any predictor, you can add `-b` to the end of the command line args to run
in binary classification mode where a 3 or 4 star route is 1, and other routes are 0.

## Create a lexicon stored as csv files for bag of word use.
```
python3 create_lexicon.py featuresInLexicon
```

## predict-svm.py
```
python3 predict-svm.py                # if you want all routes
python3 predict-svm.py Trad,Sport,TR  # if you want only these types of routes
```

## predict-knn.py
```
python3 predict-knn.py 5      # 5 is k for knn
```

## predict-bow-nn.py
```
python3 predict-bow-nn.py numberOfEpochs featuresInLexicon
```

## predict-bow-svm.py
```
python3 predict-bow-svm.py featuresInLexicon
```

## predict-nn.py
```
python3 predict-nn.py numberOfEpochs
```

# How to get route data.
```
python3 crawler.py max_num_routes <0 or 1 for test mode>
python3 api.py
python3 api_parse.py
```
