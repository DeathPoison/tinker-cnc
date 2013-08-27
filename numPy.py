#!/usr/bin/env python
# coding: utf-8

import time
import numpy as np

def trad_version():
    t1 = time.time()
    X = range(10000000)
    Y = range(10000000)
    Z = []
    for i in range(len(X)):
        Z.append(X[i] + Y[i])
    return time.time() - t1

def numpy_version():
    t1 = time.time()
    X = np.arange(10000000)
    Y = np.arange(10000000)
    Z = X + Y
    return time.time() - t1

t_trad = trad_version()
t_numpy = numpy_version()
print("Benotigte Zeit für traditonelle Losung:")
print(t_trad)

print("Benotigte Zeit für Löoung mit NumPy:")
print(t_numpy)

print("Losung mit NumPy " + str(t_trad * 100 / t_numpy) + " % schneller")
