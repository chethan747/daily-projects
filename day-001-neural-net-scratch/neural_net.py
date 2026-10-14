"""A tiny feedforward neural network written from scratch in pure Python.

No numpy, no frameworks. One hidden layer, sigmoid activations,
trained with vanilla backpropagation. Small enough to read in one sitting.
"""

import math
import random


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_derivative(y):
    # y is already sigmoid(x)
    return y * (1.0 - y)


class NeuralNet:
    def __init__(self, n_inputs, n_hidden, n_outputs, seed=7):
        rng = random.Random(seed)
        # weights[input][hidden], weights[hidden][output], plus biases
        self.w1 = [[rng.uniform(-1, 1) for _ in range(n_hidden)]
                   for _ in range(n_inputs)]
        self.b1 = [0.0] * n_hidden
        self.w2 = [[rng.uniform(-1, 1) for _ in range(n_outputs)]
                   for _ in range(n_hidden)]
        self.b2 = [0.0] * n_outputs

    def forward(self, x):
        self.last_x = x
        self.last_h = [sigmoid(sum(x[i] * self.w1[i][j] for i in range(len(x))) + self.b1[j])
                       for j in range(len(self.b1))]
        self.last_o = [sigmoid(sum(self.last_h[j] * self.w2[j][k] for j in range(len(self.last_h))) + self.b2[k])
                       for k in range(len(self.b2))]
        return self.last_o

    def train_step(self, x, target, lr=0.5):
        out = self.forward(x)
        # output layer deltas
        d_out = [(target[k] - out[k]) * sigmoid_derivative(out[k])
                 for k in range(len(out))]
        # hidden layer deltas
        d_hid = [sum(d_out[k] * self.w2[j][k] for k in range(len(out)))
                 * sigmoid_derivative(self.last_h[j])
                 for j in range(len(self.last_h))]
        # update output weights
        for j in range(len(self.last_h)):
            for k in range(len(out)):
                self.w2[j][k] += lr * d_out[k] * self.last_h[j]
        for k in range(len(out)):
            self.b2[k] += lr * d_out[k]
        # update hidden weights
        for i in range(len(x)):
            for j in range(len(self.last_h)):
                self.w1[i][j] += lr * d_hid[j] * x[i]
        for j in range(len(self.last_h)):
            self.b1[j] += lr * d_hid[j]
        # mean squared error for this sample
        return sum((target[k] - out[k]) ** 2 for k in range(len(out))) / len(out)

    def fit(self, X, Y, epochs=10000, lr=0.5, log_every=2000):
        for epoch in range(1, epochs + 1):
            loss = sum(self.train_step(x, y, lr) for x, y in zip(X, Y)) / len(X)
            if epoch % log_every == 0 or epoch == 1:
                print("epoch %5d  loss %.6f" % (epoch, loss))
        return loss

    def predict(self, x):
        return self.forward(x)
