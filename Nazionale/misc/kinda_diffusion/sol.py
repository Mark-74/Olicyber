from PIL import Image, ImageDraw
import random

for i in range(256):
    random.seed(i)
    image = Image.open('output.bin')
    for x in range(image.width):
        for y in range(image.height):
            p = image.getpixel((x,y))
            old_p = [(c - random.randint(0, 255))%256 for c in p]
            image.putpixel((x,y), tuple(old_p))
    
    image.save(f'output_{i}.png')