import time
import numpy as np
import matplotlib.pyplot as plt
from cubingtools import *

def benchmark(ns, lengths):
    results = np.zeros((len(ns), len(lengths)))

    for i, n in enumerate(ns):
        for j, L in enumerate(lengths):
            total = 0.0

            cube = CubeN(n)

            start = time.perf_counter()
            cube.scramble(L)
            end = time.perf_counter()

            total += (end - start)
            results[i, j] = total

    return results


def plot(ns, lengths, results):
    plt.imshow(
        results,
        aspect="auto",
        origin="lower",
        extent=[min(lengths), max(lengths), min(ns), max(ns)],
    )
    plt.colorbar(label="Time (seconds)")
    plt.xlabel("Scramble length (L)")
    plt.ylabel("Cube size (N)")
    plt.title("Scramble Performance Surface")
    plt.show()


if __name__ == "__main__":
    ns = list(range(5, 101, 10))          # cube sizes
    lengths = list(range(1, 1001, 50))    # scramble sizes

    results = benchmark(ns, lengths)
    plot(ns, lengths, results)