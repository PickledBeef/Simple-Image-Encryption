# Author: Hao Ding

import random

def find_d(e, r):
    i = 1
    while True:
        if e * i % r == 1:
            return i
        i += 1

def find_e(r):
    for i in range(r):
        if r % (i+2) != 0:
            return i+2


def encryption(n, e, N):
    x = 1
    for i in range(e):
        x = x * n % N
    return x


def decryption(c, d, N):
    x = 1
    for i in range(d):
        x = x * c % N
    return x


# start a simple test
p = 83
q = 97
N = p*q
r = (p-1)*(q-1)
e = find_e(r)
d = find_d(e, r)


print("N = ", N, ", e = ", e, ", r = ", r)
n1 = random.randrange(1000)
print("n1 = ",n1)
c = encryption(n1, e, N)
print("c = ",c)
n2 = decryption(c, d, N)
print("n2 = ", n2)

# verify the final output
print(n1 == n2)