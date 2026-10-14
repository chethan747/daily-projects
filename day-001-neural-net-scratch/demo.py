"""Demo: train the from-scratch network on XOR, then on a 2D blob task."""
import random
from neural_net import NeuralNet

print("=== XOR ===")
X_xor = [[0, 0], [0, 1], [1, 0], [1, 1]]
Y_xor = [[0], [1], [1], [0]]
net = NeuralNet(2, 4, 1)
net.fit(X_xor, Y_xor, epochs=12000, lr=0.5, log_every=4000)
correct = 0
for x, y in zip(X_xor, Y_xor):
    pred = net.predict(x)[0]
    label = round(pred)
    correct += label == y[0]
    print("in=%s raw=%.3f -> %d (expected %d)" % (x, pred, label, y[0]))
print("XOR accuracy: %d/4\n" % correct)

print("=== 2D blobs: is the point inside the circle? ===")
rng = random.Random(42)
X_blob, Y_blob = [], []
for _ in range(200):
    x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
    X_blob.append([x, y])
    Y_blob.append([1 if x * x + y * y < 0.35 else 0])
net2 = NeuralNet(2, 6, 1)
net2.fit(X_blob, Y_blob, epochs=6000, lr=0.5, log_every=2000)
correct = sum(round(net2.predict(x)[0]) == y[0] for x, y in zip(X_blob, Y_blob))
print("blob accuracy: %d/%d = %.1f%%" % (correct, len(X_blob), 100.0 * correct / len(X_blob)))
