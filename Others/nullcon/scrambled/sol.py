import random

def reverse_encoding(scrambled_result, key, seed):
    chunk_size = 4
    num_chunks = len(scrambled_result) // chunk_size

    # Step 1: Split scrambled result into chunks of size 4
    scrambled_chunks = [scrambled_result[i:i+chunk_size] for i in range(0, len(scrambled_result), chunk_size)]

    # Step 2: Recreate shuffle order using the same seed
    random.seed(seed)
    shuffled_indices = list(range(num_chunks))
    random.shuffle(shuffled_indices)

    # Step 3: Restore the original chunk order correctly
    original_chunks = [None] * num_chunks
    for correct_idx, shuffled_idx in enumerate(shuffled_indices):
        original_chunks[shuffled_idx] = scrambled_chunks[correct_idx]  # <-- Fix

    # Flatten to recover XORed bytes
    original_xor_result = [item for chunk in original_chunks for item in chunk]

    # Step 5: Undo XOR
    original_flag = "".join(chr(byte ^ key) for byte in original_xor_result)

    return original_flag

scrambled_result_hex = '1e78197567121966196e757e1f69781e1e1f7e736d6d1f75196e75191b646e196f6465510b0b0b57'  
scrambled_result = [int(scrambled_result_hex[i:i+2], 16) for i in range(0, len(scrambled_result_hex), 2)]

for seed in range(11):  # Brute-force all possible seeds
    for key in range(256):  # Brute-force the XOR key
        flag = reverse_encoding(scrambled_result, key, seed)
        if flag.startswith("ENO{"):
            print(f"✅ Found: Seed={seed}, Key={key}")
            print(f"Recovered Flag: {flag}")
            exit()
            
