import tensorflow as tf
import numpy as np


def train_model(files):
    data = []
    answers = {'hold': [], 'column': [], 'row': [], 'state': []}
    for file in files:
        for line in open(file, 'r').read().split('\n'):
            new_data, new_answer = ([int(x) for x in part.split(', ')] for part in line.split('|'))
            if new_answer[0] == 0:
                data.append(new_data)

                answers['hold'].append(new_answer[0])
                answers['column'].append(new_answer[1:11].index(1))
                answers['row'].append(new_answer[11:31].index(1))
                answers['state'].append(new_answer[31:35].index(1))

    data = np.array(data)
    for key in answers:
        answers[key] = np.array(answers[key])

    data_train = data[:9 * len(data)//10]
    answers_train = {}
    for key in answers:
        answers_train[key] = answers[key][:9 * len(data)//10]

    data_test = data[9 * len(data)//10:]
    answers_test = {}
    for key in answers:
        answers_test[key] = answers[key][9 * len(data)//10:]

    models = {}
    models['hold'] = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(249,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(2)
    ])

    models['column'] = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(249,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(10)
    ])

    models['row'] = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(249,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(20)
    ])

    models['state'] = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(249,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(4)
    ])

    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    opt = tf.keras.optimizers.Adam()
    for key in models:
        print('Training ' + key + ' model')
        models[key].compile(opt, loss=loss_fn, metrics=['accuracy'])
        models[key].fit(data_train, answers_train[key], epochs=50, verbose=0)
        print('Evaluation of ' + key + ' model:')
        models[key].evaluate(data_test, answers_test[key], verbose=2)
        print()

    return data, answers


d, a = train_model(['training_data/game0_example.txt', 'training_data/game1_example.txt'])
