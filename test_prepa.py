# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from scapy.all import *
from scapy.layers.inet import ICMP, IP, TCP
from scapy.layers.l2 import ARP, Ether
from math import cos, sin
import numpy as np
import matplotlib.pyplot as plt


# Press the green button in the gutter to run the script.
def func(x):
    return 1 + cos(x ** 2) + sin(x)


def func2(x):
    return math.exp(-x) * cos(x ** 2)


if __name__ == '__main__':
    # Q1
    cos_vals = [(func(x), float(x)) for x in np.arange(math.pi / 8, (math.pi * 5) / 8, (math.pi / 2) / 1000)]
    print(cos_vals, len(cos_vals))
    print(cos_vals[1])
    print(f"Mon minimum est {min(cos_vals)}")

    exp_vals = [(func2(x), float(x)) for x in np.arange(-1, 1, (1 + 1) / 1000)]
    x_vals = [x[1] for x in exp_vals]
    exp_f_vals = [x[0] for x in exp_vals]

    # exp_vals_2 = [(func2(x), float(x)) for x in x_vals[:]]

    print(f"Origines : {[exp_vals]}")
    print(
        f"Dérivées : {[((func2(x_vals[x + 1]) - func2(x_vals[x])) / (x_vals[x + 1] - x_vals[x]), x_vals[x]) for x in range(0, 999)]}")


    plt.plot(x_vals, exp_f_vals)
    plt.plot(
        x_vals[:-1],
        [((func2(x_vals[x + 1]) - func2(x_vals[x])) / (x_vals[x + 1] - x_vals[x])) for x in range(0, 999)])
    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
