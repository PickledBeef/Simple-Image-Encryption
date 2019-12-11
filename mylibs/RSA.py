# RSA algorithm
# Author: Jianan Ni
# Date: 11/2612019
# You can find a simple , clear but slow RSA code in "test2.py"

from random import randint
from datetime import datetime
from math import sqrt
from .test3 import quick_mod
from os import path

# Imported functions:
# 1.
# random.randint(a, b)
# Return a random integer N such that a <= N <= b.
# 2.
# math.sqrt(x)¶
# Return the square root of x.
# 3.
# class datetime.datetime
# A combination of a date and a time. Attributes: year, month, day, hour, minute, second, microsecond, and tzinfo.
# Link: https://docs.python.org/2/library/datetime.html

def main():
    # Initialize constants for the following functions
    global CONSTANTS  
    CONSTANTS = Const()
    
    '''
    # Generate prime numbers and get runtime
    start=datetime.now()
    primes = generate_primes()
    time_generate = datetime.now() - start
    print(primes)
    time_print = datetime.now() - start - time_generate
    write_to_file(primes)
    time_save = datetime.now() - start - time_generate - time_print
    primes_read =  read_from_file()
    time_read = datetime.now() - start - time_generate - time_print - time_save
    primes_read = [int(i) for i in primes_read.split(", ")] 
    time_transform = datetime.now() - start - time_generate - time_print - time_save - time_read
    
    # get runtime in string format
    time_generate = str(time_generate.seconds) + '.' + str(time_generate.microseconds)
    time_print    = str(time_print.seconds)    + '.' + str(time_print.microseconds)
    time_save     = str(time_save.seconds)     + '.' + str(time_save.microseconds)
    time_read     = str(time_read.seconds)     + '.' + str(time_read.microseconds)
    time_transform= str(time_transform.seconds)+ '.' + str(time_transform.microseconds)
    
    # print runtime of each process
    print("Time for generating primes : %s second(s)" %(time_generate))
    print("Time for printing primes   : %s second(s)" %(time_print))
    print("Time for saving primes     : %s second(s)" %(time_save))
    print("Time for reading primes    : %s second(s)" %(time_read))
    print("Time for transform read    : %s second(s)" %(time_transform))
    '''
    
    primes =  read_from_file()
    primes = [int(i) for i in primes.split(", ")]
    p, q = pick_two(primes)
    print("p: ", p)
    print("q: ", q)
    n = p*q
    etf = Euler_totient(p, q) # Euler's totient function
    
    # Choose an integer e :
    # 1) 1 < e < etf 
    # 2) e and etf are coprime, which means gcd(e, etf) = 1
    e = choose_e(etf)
    if not e:
        return None
    
    # Determine d as d ≡ e^(−1) (mod etf); that is, d is the modular multiplicative inverse of e modulo etf.
    # See details of modular multiplicative inverse in "modular multiplicative inverse.png"
    # This means: solve for d the equation d⋅e ≡ 1 (mod etf).
    # Be more clear: There exists an integer k such that e * d = k * etf + 1
    # d can be computed efficiently by using the Extended Euclidean algorithm.
    # Since e * d = k * etf + 1 =>  e * d - k * etf = 1,
    # there exists two integers x, y such that etf*x + e*y = 1.
    # Solve the equation etf*x + e*y= 1 to get d that is y.
    print("etf  : ", etf)
    print("e    : ", e)
    
    array = extend_gcd(etf, e)
    length = len(array)
    xy = determine_d(etf, e, array, length-1)
    d = xy[1]
    
    # This is a slower but easy-understanding function, 
    # which do what determine_d() and extend_gcd() do
    # d = find_d(etf, e);
    
    print("Original d: %d" %d)
    # Verify if d is positive
    while (d < 0):
        d += etf  
    print("Positive d: %d" %d)
    
    # create keys
    public  = [n, e]
    private = [n, d]
    
    public_path = "public.txt"
    private_path = "private.txt"
    
    if not path.exists("./output/"+public_path):
        with open("./output/"+public_path, 'w') as file:
            file.write(", ".join([str(i) for i in public]))
            
    if not path.exists("./output/"+private_path):
        with open("./output/"+private_path, 'w') as file:
            file.write(", ".join([str(i) for i in private]))
    return [n,e,d]


def encrypt(num, e, n):
    #return num^e%n 
    return quick_mod(num, e, n)
    
def decrypt(num, d, n):
    #return num^d%n 
    return quick_mod(num, d, n)
    
    
# There is a simple and clear logic to combine determine_d() and extend_gcd()
# I am not sure the either time complexity since I have already forgotten the related knowledge.
# Actually, according to my test,
# set etf = 59140992 and e = 41154761,
# find_d() costs about 8.1 ~ 11.75 seconds (return 7~9 seconds if you use datetime module ),
# combine determine_d() and extend_gcd() cost about 3.13*10^(-5) ~ 3.49*10^(-4) second (return 0.0 second if you use datetime module ).
# Thus, the time cost of find_d() at least is about 2.32*10^4 times another two functions.
# You should get similar results by running "test1.py"
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
    
def choose_e(etf):
    e = randint(2, etf - 1)
    count = 0
    while(co_prime(etf, e) == False):
        e = randint(2, etf - 1)
        count += 1
        if count == etf:
            print("Error: choose_e() exceeds the loop limit.")
            return None
    
    return e
        
    
# Greatest common divisor
# Method: Euclidean algorithm
# see simple explanation in "Euclidean algorithm.gif" 
def gcd(a, b):
    if a == 0:
        return b
    elif b == 0:
        return a
    elif(a > b):
        return gcd(a%b, b)
    return gcd(a, b%a)

# Check if two integers are coprime
def co_prime(a, b):
    if gcd(a,b) == 1:
        return True
    return False
    
# Euler's totient function
def Euler_totient(p, q):
    return (p-1)*(q-1)
    
class Const:
  # @property is not in need.
  def PRIME_MAX(self):
    return 10000
    
  def FILENAME_PRIME(self):
    return "primes.txt"  
    
def pick_two(array):
    p1 = randint(0, len(array))
    p2 = randint(0, len(array))
    while (p1 == p2):
        p2 = randint(0, len(array))
    return array[p1], array[p2]    

def generate_primes():
    array = [2,3,5,7,11,13,17,19]
    for num in range(21, CONSTANTS.PRIME_MAX(), 2):
        if all(num%i != 0 for i in range(3, int(sqrt(num))+1, 2)):
            array.append(num)
    return array

# Note the path difference below if you want to change some files' location    
def write_to_file(array):
    with open("../input/"+CONSTANTS.FILENAME_PRIME(), "w") as file:
        file.write(", ".join([str(i) for i in array]))
        
def read_from_file():
    with open("./input/"+CONSTANTS.FILENAME_PRIME(), "r") as file:
        array = file.read()
    return array    
    
if __name__ == "__main__":
    main()        
        