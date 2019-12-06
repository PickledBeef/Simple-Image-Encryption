
The program is about the encryption and decryption of image. We hide the image A into another image B, then we got image B_1, which looks the same to image B but hiding image A in it. Next step, we extract information(image A) from image B_1 and release it as a new image A_1.
In our example, image A is 'content.png', image B is 'mask.png', image A_1 is 'mask_extract.png' and image B_1 is 'mask_hide.png'.

0. Make sure python3 is installed.

1. Run encrypt.py to encrypt the image in input file with the public key. The encrypted image is in output file. 
    python3 encrypt.py
2. Run decrypt.py to decrypt the image with the private key. The decrypted image is in output file.
    python3 decrypt.py
3. Look at four images in input file and output file. In input file, there are 'content.png' and 'mask.png'. In output file, there are 'mask_extract.png' and 'mask_hide.png'.

4. 'content.png' and 'mask_extract.png' is the same. 'mask_hide.png' should look the same to 'mask.png'
