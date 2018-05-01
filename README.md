# route-quality-predictor
Machine Learning to predict the quality of a climbing route based on various attributes, images, and descriptors.

## Binary classification
Note for any predictor, you can add `-b` to the end of the command line args to run
in binary classification mode where a 3 or 4 star route is 1, and other routes are 0.

## Create a lexicon stored as csv files for bag of word use.
```
python3 create_lexicon.py featuresInLexicon
```
Your lexicon will be saved in `./lexicons`.

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
Where `featuresInLexicon` in lexicon should correspond to a lexicon you created using
the `create_lexicon.py` script. Your neural network model will be saved in `./models`.

## predict-bow-svm.py
```
python3 predict-bow-svm.py featuresInLexicon
```

## predict-nn.py
```
python3 predict-nn.py numberOfEpochs
```
Your neural network model will be saved in `./models`.

# How to get route data.
```
# will create table and crawl, getting specified number of routes and parsing description out of html
python3 crawler.py max_num_routes testMode
# will download the api json for each route that doesn't have it
python3 api.py
# will parse the api json for each route that has not been parsed
python3 api_parse.py
```
Where `testMode` is `0` for normal routes (used in regular training and testing)
or `1` special group of routes reserved for extra validation and restoration of the neural network models.

# How to restore a neural net and run the "test" items in database on it.
Route description neural net. Make sure if the model was created in binary mode, you run
this file also in binary mode.
```
python3 restore-bow-nn.py path_to_model
# ex:
python3 restore-bow-nn.py ./models/route_description_100_words_binary/model -b
```

Route features neural net.
```
python3 restore-nn.py path_to_model
# ex:
python3 restore-nn.py ./models/route_features_model_binary/model -b
```
