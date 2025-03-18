import os
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Directories
encrypted_dir = 'encrypted_files'
decrypted_dir = 'decrypted_files'
os.makedirs(decrypted_dir, exist_ok=True)

all_files = [f for f in os.listdir(encrypted_dir) if f.endswith('.enc')]

# Determine the original filenames
base_names = set()
for filename in all_files:
    try:
        base, _ = filename.rsplit('_', 1)  # splits into "original_filename" and "XX.enc"
        base_names.add(base)
    except ValueError:
        # Skip if don't match
        continue

# For each unique file, search for sequential chunks until one is missing.
for base in base_names:
    key = sha256(base.encode()).digest()
    iv = b'\x00' * 16
    chunk_index = 0
    output_file_path = os.path.join(decrypted_dir, base)
    
    # Open (or create) the output file for writing the decrypted content.
    with open(output_file_path, 'wb') as outfile:
        while True:
            # Construct the expected chunk filename (e.g. myfile_00.enc, myfile_01.enc, etc.)
            chunk_filename = f"{base}_{chunk_index:02}.enc"
            chunk_filepath = os.path.join(encrypted_dir, chunk_filename)
            
            # If the chunk does not exist, stop processing this file.
            if not os.path.exists(chunk_filepath):
                break
            
            # Read the encrypted chunk.
            with open(chunk_filepath, 'rb') as chunk_file:
                encrypted_chunk = chunk_file.read()
            
            # Initialize the cipher with the derived key and fixed IV.
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            
            # Decrypt and remove the padding.
            try:
                decrypted_chunk = unpad(cipher.decrypt(encrypted_chunk), AES.block_size)
            except ValueError as e:
                print(f"Error decrypting {chunk_filename}: {e}")
                break
            
            # Write the decrypted chunk to the output file.
            outfile.write(decrypted_chunk)
            chunk_index += 1
            
    print(f"Decrypted file saved as: {output_file_path}")

print("Decryption complete.")
