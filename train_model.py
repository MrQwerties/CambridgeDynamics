import tensorflow as tf
import numpy as np
from tensorflow.keras import datasets, layers, models
import random
import os


def train_model(files):
    lines = []
    for file in files:
        lines += open(file, 'r').read().split('\n')
    print(str(len(lines)) + ' examples loaded from ' + str(len(files)) + ' files')
    random.shuffle(lines)

    board_data = []
    blocks_data = []
    answers = []
    for line in lines:
        new_data, new_answer = (np.array([int(x) for x in part.split(', ')]) for part in line.split('|'))
        board_data.append([new_data[20 * i:20*(i + 1)] for i in range(10)])
        blocks_data.append(new_data[200:249])

        # Convert the action into a single number
        if new_answer[0] == 0:
            try:
                col = list(new_answer[1:11]).index(1)
                row = list(new_answer[11:31]).index(1)
                state = list(new_answer[31:35]).index(1)
            except ValueError:
                del(board_data[-1])
                del(blocks_data[-1])
                continue
            answers.append(4 * (20 * col + row) + state)
        else:
            answers.append(800)

    board_data = np.asarray(board_data).astype(np.float32)
    blocks_data = np.asarray(blocks_data).astype(np.float32)
    answers = np.asarray(answers).astype(np.float32)

    board_train = board_data[:9 * len(board_data)//10]
    blocks_train = blocks_data[:9 * len(board_data)//10]
    answers_train = answers[:9 * len(board_data)//10]

    board_test = board_data[9 * len(board_data)//10:]
    blocks_test = blocks_data[9 * len(board_data)//10:]
    answers_test = answers[9 * len(board_data)//10:]

    # model = tf.keras.models.Sequential([
    #     tf.keras.layers.Input(shape=(249,)),
    #     tf.keras.layers.Dense(24, activation='relu'),
    #     tf.keras.layers.Dropout(0.4),
    #     tf.keras.layers.Dense(801)
    # ])

    board_input = tf.keras.Input(shape=(10, 20, 1), name='board')
    # board_cnn = layers.Conv2D(64, (3, 4), activation='relu', input_shape=(10, 20, 1))(board_input)
    # board_cnn = layers.MaxPooling2D((2, 2))(board_cnn)
    # board_cnn = layers.Conv2D(64, (3, 3), activation='relu')(board_cnn)
    # board_cnn = layers.Flatten()(board_cnn)
    # board_cnn = layers.Dropout(0.2)(board_cnn)
    board_cnn = layers.Flatten()(board_input)
    board_cnn = layers.Dense(128)(board_cnn)
    board_cnn = layers.Dense(64)(board_cnn)
    board_cnn = layers.Dropout(0.2)(board_cnn)

    blocks_input = tf.keras.Input(shape=(49,), name='blocks')
    blocks_layer = layers.Dense(32)(blocks_input)
    blocks_layer = layers.Dense(32)(blocks_layer)

    output = layers.concatenate([board_cnn, blocks_layer])
    output = layers.Dense(32)(output)
    output = layers.Dense(32)(output)
    output = layers.Dropout(0.2)(output)
    output = layers.Dense(801)(output)
    model = tf.keras.Model(inputs=[board_input, blocks_input], outputs=[output])
    model.summary()

    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    opt = tf.keras.optimizers.Adam()
    model.compile(opt, loss=loss_fn, metrics=['accuracy'])
    for i in range(12):
        print('Epoch ' + str(5 * i))
        model.fit({'board': board_train, 'blocks': blocks_train}, answers_train, epochs=5)
        model.evaluate({'board': board_test, 'blocks': blocks_test}, answers_test, verbose=2)
        print()
    model.save('saved_models/cnn-0')


folder = 'training_data_ultra_complete'
train_model([folder + '/' + file for file in os.listdir('training_data_ultra_complete')])
