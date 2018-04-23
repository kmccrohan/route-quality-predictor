# route-quality-predictor
Machine Learning to predict the quality of a climbing route based on various attributes, images, and descriptors.

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
