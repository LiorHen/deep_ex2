import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

tf.logging.set_verbosity(tf.logging.INFO)
mode = "train"


def network_model(data):
    """
    Runs the network
    Parameters:
        data (tf.placeholder): the input data
        perform_dropout (boolean): when True the dropout is performed.
    Output:
        the result of the network
    """

    # Input Layer.
    input_layer = tf.reshape(data, [-1, 28, 28, 1])

    # Convolutional Layer #1
    conv1 = tf.layers.conv2d(inputs=input_layer, filters=32, kernel_size=[5, 5], padding="same")

    # norm1
    batch_norm1 = tf.layers.batch_normalization(inputs=conv1)

    # Pooling Layer #1
    pool1 = tf.layers.max_pooling2d(inputs=batch_norm1, pool_size=[2, 2], strides=2)

    # Convolutional Layer #2
    conv2 = tf.layers.conv2d(inputs=pool1, filters=64, kernel_size=[5, 5], padding="same")

    # norm2
    batch_norm2 = tf.layers.batch_normalization(inputs=conv2)

    # Pooling Layer #1
    pool2 = tf.layers.max_pooling2d(inputs=batch_norm2, pool_size=[2, 2], strides=2)

    # Dense Layer #1
    pool2_flat = tf.reshape(pool2, [-1, 7 * 7 * 64])
    dense1 = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)

    dropout = tf.layers.dropout(inputs=dense1, rate=0.4, training=mode=="train")

    # Dense Layer #2
    dense2 = tf.layers.dense(inputs=dropout, units=1024, activation=tf.nn.relu)

    # the dense for the softmax
    predictions = tf.layers.dense(inputs=dense2, units=10)

    return predictions


def train_network(dataset):
    """
    trains the network
    """
    global mode

    x = tf.placeholder('float', [None, 784])
    y = tf.placeholder('float')

    # batch size
    batch_size = 100

    # number of iterations
    n_epochs = 5000

    # the learning rate
    learning_rate = 0.001

    # validation set
    validation_set = dataset.train

    # runs the network
    prediction = network_model(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for epoch in range(n_epochs):
            epoch_loss = 0
            epoch_x, epoch_y = dataset.train.next_batch(batch_size)
            _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
            epoch_loss += c
            tf.logging.info(epoch)
            if (epoch + 1) % 250 == 0:
                msg = 'Epoch' + epoch + 1 + 'completed out of' + n_epochs + 'loss:' + epoch_loss
                tf.logging.info(msg)

        mode = "test"
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        tf.logging.info('Accuracy:', accuracy.eval({x: dataset.test.images, y: dataset.test.labels}))

if __name__ == '__main__':
    tf.logging.info("Loading MNIST dataset")
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
    tf.logging.info("Initiating Training")
    train_network(mnist)
    tf.logging.info("Finished")
