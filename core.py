from app.processor import encoder, utils
import numpy as np
from keras import backend
from keras.models import load_model
from dir import get_full_path


predictions = {0: 'ham', 1: 'spam', 2: 'fraud'}


def predict(body):
    file_content = utils.Process(body)
    mail = file_content.process()
    matrix = np.array([encoder.get_matrix(mail)])

    model = load_model(get_full_path('data/model.h5'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    result = model.predict_classes(matrix)
    backend.clear_session()
    return predictions.get(result[0])


    # pso_file = get_full_path('data/weights_final_pso.txt')
    # with open(pso_file, 'rb') as f:
    #     pos = pickle.load(f, encoding='latin1')
    # n_inputs = 6382
    # n_hidden_one = 20
    # n_hidden_two = 10
    # n_classes = 3
    # # Roll-back the weights and biases
    # W1 = pos[0:127640].reshape((n_inputs, n_hidden_one))
    # b1 = pos[127640:127660].reshape((n_hidden_one,))
    # W2 = pos[127660:127860].reshape((n_hidden_one, n_hidden_two))
    # b2 = pos[127860:127870].reshape((n_hidden_two,))
    # W3 = pos[127870:127900].reshape((n_hidden_two, n_classes))
    # b3 = pos[127900:127903].reshape((n_classes,))
    #
    # z1 = matrix.dot(W1) + b1  # Pre-activation in Layer 1
    # a1 = np.tanh(z1)  # Activation in Layer 1
    # z2 = a1.dot(W2) + b2  # Pre-activation in Layer 2
    # a1 = np.tanh(z2)  # Activation in Layer 2
    # z3 = a1.dot(W3) + b3  # Pre-activation in Layer 3
    # logits = z3  # Logits for Layer 3
    #
    # y_pred = np.argmax(logits, axis=1)

#
print(predict('i love you soo much'))