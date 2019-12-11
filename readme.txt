General idea: Hide secret ("content.png") in mask ("mask.png"). 
Alogrithms used: simple RSA, DWT-like

First of all:
A. In "clear_version" folder, this is a clear version which remove unnecessary code and has more readable ouput.
B. See my implementation of RSA algorithm in "./mylibs/RSA,py" (Math part)
C. This is a draft since I still have many idea to improve it. (select random start point when hide pixels, separatedly save info when hide pixels, fill image with meaningless info but image does not change, etc.)
D. All output will update if you run the program. You don't have to do any delete. Current existed output is a sample.


Then:
For inputs:
1. Name your secret image as "content.png", then put in "input" folder.
2. Name your mask image as "mask.png", then put in "input" folder.
3. "primes.txt" is a list of prime numbers. You can replace it with the same name.
4. See implementation of RSA algorithm in "input" folder.

For outputs: (You should get the following files in "output" folder after executing "image.py")
1. "content_ds.png" is compressed "content.png".
2. "mask_revised_1.png" is revised "mask.png", which is used for the follwing steps.
3. "mask_hide.png" is a combination of "content.png" and "mask_revised_1.png".
4. "mask_extract.png" consists of information that is extracted from "mask_hide.png".
5. "original.txt" contains the size/shape of "content.png". The size/shape is the key to extract the information from "mask_hide.png".
6. "send.txt" is encrypted "original.txt".
7. "extract.txt" is decrypted "send.txt".
8. "public.txt" contains a key for encryption.
9. "private.txt" contains a key for decryption.

