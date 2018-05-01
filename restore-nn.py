import tensorflow as tf
from get_datasets import get_test_routes, binary_stars
import numpy as np
import sys

MODEL_PATH = sys.argv[1]
META_PATH = MODEL_PATH + '.meta'
BINARY_MODE = False
if "-b" in sys.argv:
    BINARY_MODE = True
n_classes = 5
NFEAUTRES = 15

def neural_net(data_test, stars_test):
    with tf.Session() as sess:
        new_saver = tf.train.import_meta_graph(META_PATH)
        new_saver.restore(sess, MODEL_PATH)

        graph = tf.get_default_graph()
        x = graph.get_tensor_by_name("x:0")
        y = graph.get_tensor_by_name("y:0")
        op_to_restore = graph.get_tensor_by_name("output_op:0")
        correct = tf.equal(tf.argmax(op_to_restore, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Test size:', len(stars_test))
        print('Accuracy:',accuracy.eval({x: data_test, y: stars_test}))

def convert_stars_obj(stars):
    return [[1 if (x + 1) == z else 0 for x in range(n_classes)] for z in stars]

data, stars = get_test_routes()
if BINARY_MODE:
    stars, stars_test = binary_stars(stars, stars)
    n_classes = 2
    y = tf.placeholder('float', [None, n_classes]) # label of the data
data = np.array(data, dtype=np.float32)
stars = np.array(stars, dtype=np.float32)
stars = convert_stars_obj(stars)

neural_net(data, stars)
