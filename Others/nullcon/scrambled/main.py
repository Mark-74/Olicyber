import random

def encode_flag(flag, key):
    xor_result = [ord(c) ^ key for c in flag]

    chunk_size = 4
    chunks = [xor_result[i:i+chunk_size] for i in range(0, len(xor_result), chunk_size)]
    seed = random.randint(0, 10)
    random.seed(seed)
    random.shuffle(chunks)
    
    scrambled_result = [item for chunk in chunks for item in chunk]
    return scrambled_result, chunks

def main():
    flag = "REDACTED"
    key = REDACTED

    scrambled_result, _ = encode_flag(flag, key)
    print("result:", "".join([format(i, '02x') for i in scrambled_result]))


if __name__ == "__main__":
    main()