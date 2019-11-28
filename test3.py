def to_binary(decimal):
    return f"{decimal:08b}"
    #return bin(decimal)[2:]

def to_decimal(binary):    
    return int(binary, 2)

# PowerMod
# Video: https://www.youtube.com/watch?v=EHUgNLN8F1Y
# Online: https://www.mtholyoke.edu/courses/quenell/s2003/ma139/js/powermod.html
def quick_mod(num, ed, n):
    r = 1
    while (ed > 0):
        if (ed & 1):
            r = (r * num) % n
        num = (num * num) % n
        ed >>= 1

    return r
