import cv2
import numpy as np
from os import path
from os import makedirs
from shutil import rmtree as delete
from mylibs.test3 import to_decimal
from mylibs.RSA import decrypt

def main():
    out = "./decrypt output/"
    if path.exists(out):
        delete(out)
    makedirs(out)

    with open("./encrypt output/encrypted message.txt", 'r') as file:
            encrypted_message = [int(i) for i in (file.read()).split(", ")]
    with open("./keys/private.txt", 'r') as file:
            private = [int(i) for i in (file.read()).split(", ")]
    decrypted_message = [decrypt(i, private[1], private[0]) for i in encrypted_message]       
    
    img_shape = decrypted_message
    save = out+ "decrypt.png"
    encrypted_mask = cv2.imread("./encrypt output/encrypt.png", 1)
    if not path.exists(save):
        img = extract_pixels(encrypted_mask, img_shape)
        cv2.imwrite(save, img)    

def extract_pixels(mask, img_shape):
    w = img_shape[0]
    h = img_shape[1]
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

    return img
    
if __name__ == "__main__":
    main()         