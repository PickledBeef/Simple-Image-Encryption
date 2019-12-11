import cv2
import numpy as np
from os import path
from os import makedirs
from shutil import rmtree as delete
from random import randint
from mylibs.test3 import to_binary
from mylibs.RSA import main as my_rsa
from mylibs.RSA import encrypt

def main():  
    # Load color images without considering alpha channel
    # Make sure all input images are square. (Actually, it should work for rectangle.)
    original_content = "./input/content.png"
    original_mask    = "./input/mask.png"
    img  = cv2.imread(original_content, 1)
    mask = cv2.imread(original_mask, 1)
    
    out = "./encrypt output/"
    if path.exists(out):
        delete(out)
    makedirs(out)

    format_mask(mask) # each pixel value of mask will be even after this step 
    img = my_downsample(img) # downsample img 
    
    save = out+"encrypt.png"
    if not path.exists(save):
        hide_pixels(img, mask)
        cv2.imwrite(save, mask)

    message = list(img.shape)
    if not path.exists(out+"original message.txt"):
        with open(out+"original message.txt", 'w') as file:
            file.write(", ".join([str(i) for i in message]))
            
    # Run RSA to generate public and private keys
    keys = my_rsa()
    public, private = [keys[0],keys[1]], [keys[0],keys[2]]
    
    encrypted_message = [encrypt(i, public[1], public[0]) for i in message]
    if not path.exists(out+"encrypted message.txt"):
        with open(out+"encrypted message.txt", 'w') as file:
            file.write(", ".join([str(i) for i in encrypted_message]))
            
# format mask
def format_mask(mask):
    for c in range(3):
        channel = mask[:, :, c]
        for q in range(len(channel)):
            for i in range(len(channel[q])):
                if channel[q][i] % 2 != 0:
                    channel[q][i] -= 1
    return None

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

def hide_pixels(img, mask):
    i_size = img.shape
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
                to2 = to_binary(int(a[o][p]))
                for bit in to2:
                    b[count1][count2] += int(bit)
                    count2 += 1
                    loop += 1
                    if count2 == h:
                        count2 = 0
                        count1 += 1

    return None      
   
if __name__ == "__main__":
    main() 