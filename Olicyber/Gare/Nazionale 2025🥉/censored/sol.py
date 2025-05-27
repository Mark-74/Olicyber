from PIL import Image
import string

def count_black_pixels_in_row(image_path, row):
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    if row < 0 or row >= height:
        raise ValueError("Row index out of bounds.")
    pixels = img.load()
    blocks = []
    count = 0
    flag = False
    for x in range(width):
        if pixels[x, row] == (0, 0, 0):
            flag = True
            count += 1
        else:
            if flag:
                blocks.append(count)
                count = 0
                flag = False
    return blocks

if __name__ == "__main__":
    results = []
    for i in range(0,800, 100):
        result = count_black_pixels_in_row('image.png', i)
        if len(result) > 0 and result[-1] != result:
            results.append(result)

    print("Results:", results)
    alphabet = string.ascii_lowercase + '_{}'

    decoded_alphabet = {}
    decoded_message = []
    counter = 0
    for i in results:
        for j in i:
            if decoded_alphabet.get(j) is None:
                decoded_alphabet[j] = alphabet[counter]
                counter += 1
    
    for i in results:
        for j in i:
            decoded_message.append(decoded_alphabet[j])
    
    print("Decoded message:", ''.join(decoded_message))
