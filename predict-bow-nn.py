import tensorflow as tf
from read_lexicon import read_lexicon
from get_datasets import binary_stars
import numpy as np
import sys
import os

#one_hot == one component is one and the others are off
# 10 classes, 0-9
'''
0=0
0 = [1,0,0,0,0,0,0,0,0]
1=1
1 = [0,1,0,0,0,0,0,0,0]
2=2
2 = [0,0,1,0,0,0,0,0,0]
.....
8 = [0,0,0,0,0,0,0,1,0]
'''
NFEAUTRES = int(sys.argv[2])
MODEL_DIR = 'models/route_description_' + str(NFEAUTRES) + '_words'
BINARY_MODE = False
if "-b" in sys.argv:
    BINARY_MODE = True
    MODEL_DIR += '_binary'
MODEL_PATH = MODEL_DIR + '/model'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
n_nodes_hl1 = NFEAUTRES
n_nodes_hl2 = NFEAUTRES
n_nodes_hl3 = NFEAUTRES

n_classes = 5
batch_size = 100000 # batches of 100 data points


#place holding variables
#matrix - height by width [height, width]
x = tf.placeholder('float', [None, NFEAUTRES]) #input data
#if you attempt to feed something that is not of that shape
#then tf will throw an error

y = tf.placeholder('float', [None, n_classes]) # label of the data


def neural_network_model(data):

#computation graph
#dictionaries for each layer

    hidden_1_layer = {'weights':tf.Variable(tf.random_normal([NFEAUTRES, n_nodes_hl1])),
                      'biases':tf.Variable(tf.random_normal([n_nodes_hl1]))}

#biases are added in after the weights ... sum(input_data * weights ) + bias
#if all the input data is 0 no neuron would ever fire .. not ideal ... adds a value
# to get neurons to fire

    hidden_2_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
                      'biases':tf.Variable(tf.random_normal([n_nodes_hl2]))}

    hidden_3_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
                      'biases':tf.Variable(tf.random_normal([n_nodes_hl3]))}

    output_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
                    'biases':tf.Variable(tf.random_normal([n_classes]))}

	#sum(input_data * weights ) + bias
	#feed forward
    l1 = tf.add(tf.matmul(data,hidden_1_layer['weights']), hidden_1_layer['biases'])
	#activation function --rectified linear --
    l1 = tf.nn.relu(l1)

    l2 = tf.add(tf.matmul(l1,hidden_2_layer['weights']), hidden_2_layer['biases'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2,hidden_3_layer['weights']), hidden_3_layer['biases'])
    l3 = tf.nn.relu(l3)

    output = tf.add(tf.matmul(l3,output_layer['weights']), output_layer['biases'], name="output_op")

    return output

#specify how we want to run data through that model in a TF session

def train_neural_network():
    prediction = neural_network_model(x) #returns the array with one component on

	#cross entropy with logits (cost fnc)
	#calculate the difference that we got to the known label that we have
    cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y) )

	#minimize the cost  #back propagation
	#learning_rate = .001
    optimizer = tf.train.AdamOptimizer().minimize(cost)

	#cycle of fed forward and back prop
    max_epochs = int(sys.argv[1])
    min_loss = 100000000

    # use to save best run.
    saver = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        prev_epoc_loss = None
        for epoch in range(max_epochs):
            epoch_loss = 0
                        #tells us how many times we cycle
            for i in range(int(len(data_train)/batch_size)):
                                #chunks through the data
                epoch_x = data_train[i*batch_size: (i+1)*batch_size]
                epoch_y = stars_train[i*batch_size: (i+1)*batch_size]
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c

            print('Epoch', epoch, 'completed out of',max_epochs,'loss:',epoch_loss)

            if epoch_loss < min_loss:
                min_loss = epoch_loss
                saver.save(sess, MODEL_PATH)

            if epoch_loss == 0:
                break


        # restore the optimal session
        saver.restore(sess, MODEL_PATH)

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Min loss: ', min_loss)
        print('Training size:', len(stars_train))
        print('Test size:', len(stars_test))
        print('Accuracy:',accuracy.eval({x: data_test, y: stars_test}))


def convert_stars_obj(stars):
    return [[1 if (x + 1) == z else 0 for x in range(n_classes)] for z in stars]

data_train, data_test, stars_train, stars_test = read_lexicon(max_features=NFEAUTRES)
if BINARY_MODE:
    stars_train, stars_test = binary_stars(stars_train, stars_test)
    n_classes = 2
y = tf.placeholder('float', [None, n_classes], name="y") # label of the data
x = tf.placeholder('float', [None, NFEAUTRES], name="x") #input data

data_train = np.array(data_train, dtype=np.float32)
data_test = np.array(data_test, dtype=np.float32)
stars_train = np.array(stars_train, dtype=np.float32)
stars_test = np.array(stars_test, dtype=np.float32)
stars_test = convert_stars_obj(stars_test)
stars_train = convert_stars_obj(stars_train)



if (batch_size > len(data_train)):
    batch_size = len(data_train)

train_neural_network()
