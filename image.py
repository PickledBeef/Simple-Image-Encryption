# Image encryption by RSA and something else
# This should be the first mask.

import cv2
import numpy as np
from os import path
from random import randint
from test3 import to_binary, to_decimal
from RSA import main as my_rsa
from RSA import encrypt, decrypt

# Load color images without considering alpha channel
# Make sure all input images are square

img = cv2.imread("content.png", 1)
mask = cv2.imread("mask.png", 1)

'''
cv2.imshow("Content", img)
cv2.imshow("Mask", mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
'''

# format mask
def format_mask(mask):
    for c in range(3):
        channel = mask[:, :, c]
        for q in range(len(channel)):
            for i in range(len(channel[q])):
                if channel[q][i] % 2 != 0:
                    channel[q][i] -= 1
    return None

mask_revised = "mask_revised_1.png"    

if not path.exists(mask_revised):
    format_mask(mask)  
    cv2.imwrite(mask_revised, mask)

#return the number of different pixel value at the same position
def image_diff(a, b):
    count = 0
    for c in range(3):
        channel_a = a[:, :, c]
        channel_b = b[:, :, c]
        for q in range(len(channel_a)):
            for i in range(len(channel_a[q])):
                if channel_a[q][i] == channel_b[q][i]:
                    count += 1
    return count

original = cv2.imread("mask.png", 1)
revised = cv2.imread(mask_revised, 1)
count = image_diff(original, revised)
print("Diff count: ", count)    

# First mask 
# In fact, most operations are not on images.
# This is fake image encryption. See this idea in "first mask.docx"
# "a – z" is assigned to "0 - 25" (which means 2 is c, 5 is f , etc.);
# "A - Z" is assigned to "26 - 51";
# ":" is 52; "/" is 52; "?" is 53; "." is 54; " " is 55

my_dict = {}

# Python: cv.Filter2D(src, dst, kernel)
# Parameters:	
# src – input image.
# dst – output image of the same size and the same number of channels as src.
# ddepth – desired depth of the destination image; if it is negative, it will be the same as src.depth().

def simple_gaussian(img):
    kernel = np.array([[1,2,1], [2,4,2], [1,2,1]])/16
    return cv2.filter2D(img, -1, kernel) 

def my_downsample(img):
    img = simple_gaussian(img)
    img_shape = img.shape
    ds = np.zeros(shape=((img_shape[0]-1)//3+1,(img_shape[1]-1)//3+1,3))
    for i in range(3):
        ds[:,:,i]=img[:,:,i][::3,::3]
    return ds   
 
content_ds = "content_ds.png"

if not path.exists(content_ds):
    content_smaller = my_downsample(img)
    cv2.imwrite(content_ds, content_smaller)

img = cv2.imread(content_ds, 1)   
    
# Second mask
def hide_pixels(img, mask):
    i_size = img.shape
    print(i_size)
    m_size = mask.shape
    w = m_size[0]
    h = m_size[1]
    loop = 0
    for i in range(3):
        a = img[:,:,i]
        b = mask[:,:,i]
        count1 = 0
        count2 = 0
        for o in range(i_size[0]):
            for p in range(i_size[1]):
                to2 = to_binary(a[o][p])
                for bit in to2:
                    b[count1][count2] += int(bit)
                    count2 += 1
                    loop += 1
                    if count2 == h:
                        count2 = 0
                        count1 += 1
    print("loop: ", loop)
    return None

hide_path = "mask_hide.png"
revised = cv2.imread(mask_revised, 1)
if not path.exists(hide_path):
    hide_pixels(img, revised)
    cv2.imwrite(hide_path, revised)

print("Diff for revised and hide: ", image_diff(cv2.imread(mask_revised, 1), cv2.imread(hide_path, 1)))

src = cv2.imread(hide_path, 1)
#img_shape = (167, 167, 3) # which should be from decryption. This tuple is just for test.

message = list(img.shape)
if not path.exists("original.txt"):
    with open("original.txt", 'w') as file:
        file.write(", ".join([str(i) for i in message]))
        
# Run RSA to generate public and private keys
keys = my_rsa()
public, private = [keys[0],keys[1]], [keys[0],keys[2]]
send = [encrypt(i, public[1], public[0]) for i in message]

if not path.exists("send.txt"):
    with open("send.txt", 'w') as file:
        file.write(", ".join([str(i) for i in send]))

extract = [decrypt(i, private[1], private[0]) for i in send]       
if not path.exists("extract.txt"):
    with open("extract.txt", 'w') as file:
        file.write(", ".join([str(i) for i in extract]))

img_shape = (167, 167, 3)        

def extract_pixels(mask, img_shape):
    w = img_shape[0]
    h = img_shape[1]
    print(img_shape)
    img = np.zeros(shape=(w,h,3))
    m_w = mask.shape[0]
    m_h = mask.shape[1]
    loop = 0
    for i in range(3):
        a = img[:,:,i]
        b = mask[:,:,i]
        count1 = 0
        count2 = 0
        bits = ""
        for o in range(w):
            for p in range(h):
                for _ in range(8):
                    loop += 1
                    if count2 == m_h:
                        count1 += 1
                        count2 = 0
                    bits += str(b[count1][count2]%2)
                    count2 += 1
                    
                value = to_decimal(bits)
                bits = ""
                a[o][p] = value
    print("loop: ", loop)
    return img
    
extract_path = "mask_extract.png"

if not path.exists(extract_path):
    img = extract_pixels(src, img_shape)
    cv2.imwrite(extract_path, img)    

