import os
from PIL import Image, ImageDraw
import numpy as np
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def mix(col1, col2):
    """
    Custom mixing function: element-wise addition modulo 256.
    """
    return [(c1 + c2) % 256 for c1, c2 in zip(col1, col2)]

def mix_inverse(result, x):
    """
    Inverse of the mixing function: element-wise subtraction modulo 256.
    If result = mix(x, y), then y = mix_inverse(result, x).
    Ensures that inputs are treated as integers before subtraction.
    """
    return [(int(c_res) - int(c_x)) % 256 for c_res, c_x in zip(result, x)]

def get_non_white_pixel(image_path):
    """
    Extracts the first non-white, non-black pixel color from an image.
    This is used to retrieve the g, A, and B values from the generated images.
    Ensures that the returned color components are standard Python integers.
    """
    with Image.open(image_path).convert('RGBA') as im:
        n = np.array(im)
        # Iterate through unique colors to find the one that's not pure white or pure black.
        unique_colors = [tuple(c) for c in np.unique(n.reshape(-1, n.shape[2]), axis=0)]
        for color in unique_colors:
            if color != (255, 255, 255, 255) and color != (0, 0, 0, 255):
                # Convert each component to a standard Python int
                return [int(c) for c in color]
    return None

def main():
    print("Starting flag recovery process...")

    # --- Step 1 & 2: Extract g, A, and B from the images ---
    print("Extracting g, A, and B values from images...")
    g_val = get_non_white_pixel('g.png')
    A_val = get_non_white_pixel('A.png')
    B_val = get_non_white_pixel('B.png')

    if not all([g_val, A_val, B_val]):
        print("Error: Could not extract all required pixel values. Ensure images are present and valid.")
        return

    print(f"  Extracted g: {g_val}")
    print(f"  Extracted A: {A_val}")
    print(f"  Extracted B: {B_val}")

    # --- Step 3: Recover 'a' and 'b' ---
    print("\nRecovering 'a' and 'b' values...")
    a_val = mix_inverse(A_val, g_val)
    b_val = mix_inverse(B_val, g_val)

    print(f"  Recovered a: {a_val}")
    print(f"  Recovered b: {b_val}")

    # --- Step 4: Calculate the shared secret (shared_A or shared_B) ---
    print("\nCalculating the shared secret...")
    shared_A = mix(B_val, a_val)
    shared_B = mix(A_val, b_val)

    print(f"  Calculated shared_A: {shared_A}")
    print(f"  Calculated shared_B: {shared_B}")

    if shared_A == shared_B:
        print("  Shared secrets match!")
    else:
        print("  Warning: Shared secrets do NOT match! There might be an issue with recovery.")
        return

    # --- Step 5: Derive the AES key ---
    print("\nDeriving the AES key...")
    # The shared secret is a list of integers, convert to bytes before hashing
    aes_key = sha256(bytes(shared_A)).digest()
    print(f"  AES Key (hex): {aes_key.hex()}")

    # --- Step 6: Decrypt the ciphertext ---
    print("\nDecrypting the flag...")
    ciphertext_hex = "999ea64e865f9bb2665c56ca54dac94c2f4968370b87d87c6bec5b8c1bba2bc4580ab1744944984f661f33776b31f49ba1ecc06db0adb892509a91018ff15503bdff31561607393cc0c8aff602da6168eb925df54fb16d75acd3550abec0781e"
    ciphertext_bytes = bytes.fromhex(ciphertext_hex)

    iv = ciphertext_bytes[:16]
    encrypted_flag = ciphertext_bytes[16:]

    try:
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_flag = unpad(cipher.decrypt(encrypted_flag), 16)
        print(f"\nSuccessfully decrypted flag: {decrypted_flag.decode()}")
    except ValueError as e:
        print(f"Decryption failed: {e}. This might indicate an incorrect key or IV.")
    except Exception as e:
        print(f"An unexpected error occurred during decryption: {e}")

if __name__ == "__main__":
    main()
