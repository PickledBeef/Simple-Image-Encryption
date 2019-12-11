# Author: Jianan Ni
# Test for specific input

from datetime import datetime
import time

etf = 59140992
e   = 41154761

# Replace determine_d() and extend_gcd()    
def find_d(etf, e):
    if etf <= e:
        print("Error: find_d(): etf <= e.")
        
    i = 1
    while True:
        if e * i % etf == 1:
            return i
        i += 1
        
# Suppose that a > b
# Parameter --- array structure: [a, 1, b, -q, r]
def determine_d(a, b, array, length, xy=[0, 0]):
    if a <= b:
        print("Error: determine_d(): a <= b.")

    current = array[length]
    # this recursive function should stop at length = -1
    length -= 1 
    
    # Initialize xy
    if xy == [0, 0]:
        xy = [1, current[3]]
        return determine_d(a, b, array, length, xy)
    
    x = xy[0]
    y = xy[1]
    xy[0] = y
    xy[1] = y*current[3]+x # Easy to understand if I have time to draw an image of current process
    
    if length < 0: # Stop at length = -1 
        return xy
    
    return determine_d(a, b, array, length, xy)
    
    
# Extended Euclidean algorithms
# Suppose that a > b 
# Stop this recursive function at remainder = 1
# since there must have 1  after multiple recursions of coprime inputs a and b (see etf, e above).
def extend_gcd(a, b, array = []):
    if a <= b:
        print("Error: extend_gcd(): a <= b.")
        return None
        
    # There exists duplicate coprime check in function choose_e()
    '''
    if not co_prime(a, b):
        print("Error: extend_gcd(): Inputs are not coprime.")
        return None
    '''  
    
    q = a // b
    r = a % b
    # In fact, a*1 + b * (-q) = r
    array.append([a, 1, b, -q, r]) 
    if r == 1:
        return array
    return (extend_gcd(b, r, array))
    
def test_a(etf, e):
    array = extend_gcd(etf, e)
    length = len(array)
    xy = determine_d(etf, e, array, length-1)
    d = xy[1]
    
def test_b(etf, e):    
    d = find_d(etf, e)

# https://stackoverflow.com/a/52228375/8529265    
start = time.process_time()
test_a(etf, e)
end = time.process_time()
print(end - start)    

start = time.perf_counter()
test_a(etf, e)
end = time.perf_counter()
print(end - start)

start = time.process_time()
test_b(etf, e)
end = time.process_time()
print(end - start)    

start = time.perf_counter()
test_b(etf, e)
end = time.perf_counter()
print(end - start)
