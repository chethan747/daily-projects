# Day 001 — Neural Net from Scratch

A tiny feedforward neural network written in **pure Python** — no numpy, no frameworks. One hidden layer, sigmoid activations, vanilla backpropagation. Small enough to read in one sitting.

## Run it

```bash
python3 demo.py
```

It trains on XOR (the classic non-linear problem a perceptron can't solve), then on a 2D "is the point inside the circle?" task — 200 random points, ~95%+ accuracy.

## What's inside

- `neural_net.py` — the network: forward pass, backprop, training loop (~90 lines)
- `demo.py` — trains and evaluates on both tasks

## The idea in one paragraph

Each neuron takes a weighted sum of its inputs, squashes it through a sigmoid, and passes it on. Training compares the output to the target, then walks the error backwards through the layers (the chain rule), nudging every weight a little in the direction that reduces the error. Repeat a few thousand times and the network learns.

Part of the [daily-projects](https://github.com/chethan747/daily-projects) series — one small build every day.
