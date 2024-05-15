#!/usr/bin/python3
from PIL import Image

def main():
    image = Image.open("bits.bmp")
    #print(image.mode) --> L --> 1 byte per pixel
    
    res = ""
    
    for pixel in list(image.getdata()):
        res += "0" if not pixel else "1"
    
    print(res)
    
    #usando poi il risultato su cyberchef è possibile scaricare l'output nel fromato corretto (zip) ed al suo interno si può trovare la flag

if __name__ == "__main__":
    main()