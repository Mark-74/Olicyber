from pwn import *
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad
import os
import time

# --- Configuration ---
HOST = 'partymode.challs.olicyber.it'
PORT = 38063
REMOTE_TIMEOUT = 300 # seconds, matching the CTF timeout

# --- Helper Functions for Blowfish Operations ---
def blowfish_cfb_encrypt(key_bytes, iv_bytes, plaintext_bytes):
    cipher = Blowfish.new(key_bytes, Blowfish.MODE_CFB, iv_bytes)
    return cipher.encrypt(plaintext_bytes)

def blowfish_cbc_encrypt(key_bytes, iv_bytes, plaintext_bytes):
    cipher = Blowfish.new(key_bytes, Blowfish.MODE_CBC, iv_bytes)
    return cipher.encrypt(plaintext_bytes)

def blowfish_cbc_decrypt(key_bytes, iv_bytes, ciphertext_bytes):
    cipher = Blowfish.new(key_bytes, Blowfish.MODE_CBC, iv_bytes)
    return cipher.decrypt(ciphertext_bytes)

def blowfish_ofb_encrypt(key_bytes, iv_bytes, plaintext_bytes):
    cipher = Blowfish.new(int.to_bytes(key_bytes, 4, 'big'), Blowfish.MODE_OFB, iv_bytes)
    return cipher.encrypt(plaintext_bytes)

def solve():
    """
    Main function to solve the CTF challenge.
    """
    overall_start_time = time.time() # Start overall timer

    r = remote(HOST, PORT)
    log.info(f"Connected to {HOST}:{PORT}")

    P_MSG_INTERNAL_FOR_K3_BRUTEFORCE = b'\x00'*16
    P_MSG_INTERNAL_FOR_K1K2_MITM = b'\x00'*16
    PAYLOAD_MESSAGE_PART = b'\x00'*16 # This is the part of the input to D command after IVs

    # Changed from 256 to 255 queries
    log.info("Collecting 255 (X_i, Y_i) pairs...")
    query_collection_start_time = time.time() # Start timer for query collection
    queries = []
    for i in range(255): # Collect 255 queries
        X_i = i.to_bytes(8, 'big') # Our chosen IV_C
        payload_bytes = b'\x00'*8 + b'\x00'*8 + X_i + PAYLOAD_MESSAGE_PART

        # The server sends a '>' prompt for each of these queries.
        r.sendlineafter(b"> ", b"D" + payload_bytes.hex().encode())
        response_hex = r.recvline().strip().decode()
        Y_i = bytes.fromhex(response_hex)
        queries.append((X_i, Y_i))

    X_0, Y_0 = queries[0]
    query_collection_end_time = time.time() # End timer for query collection
    log.info(f"Query collection complete in {query_collection_end_time - query_collection_start_time:.2f} seconds.")

    # --- NO MORE SERVER INTERACTION UNTIL FINAL KEY SUBMISSION ---
    # All brute-forcing and MITM calculations are done locally now.

    log.info("Brute-forcing K3 (2^20 combinations) and verifying K_const...")
    k3_bruteforce_start_time = time.time() # Start timer for K3 brute-force
    found_k3 = None
    found_k_const = None

    for k3_candidate in range(2**20):
        # In the original script, Blowfish.new was instantiated with int.to_bytes(k3_candidate, 4, 'big') directly within the loop.
        # Here we moved it inside blowfish_ofb_encrypt, which handles the conversion.
        e_k3_x0 = blowfish_ofb_encrypt(k3_candidate, X_0, P_MSG_INTERNAL_FOR_K3_BRUTEFORCE)

        k_const_candidate = bytes([a ^ b for a, b in zip(Y_0, e_k3_x0)])

        is_k3_found = True
        # Iterate over the remaining 254 queries for verification
        for i in range(1, 255): # Iterate from 1 to 254 (inclusive)
            X_i, Y_i = queries[i]
            e_k3_xi = blowfish_ofb_encrypt(k3_candidate, X_i, P_MSG_INTERNAL_FOR_K3_BRUTEFORCE)

            if bytes([a ^ b for a, b in zip(Y_i, k_const_candidate)]) != e_k3_xi:
                is_k3_found = False
                break

        if is_k3_found:
            found_k3 = k3_candidate
            found_k_const = k_const_candidate
            log.success(f"Found K3: {hex(found_k3)}")
            break

    k3_bruteforce_end_time = time.time() # End timer for K3 brute-force
    log.info(f"K3 brute-force complete in {k3_bruteforce_end_time - k3_bruteforce_start_time:.2f} seconds.")

    if found_k3 is None:
        log.error("Failed to find K3 and K_const. Exiting.")
        r.close()
        return

    log.info("Brute-forcing K1 and K2 using Meet-in-the-Middle...")
    k1k2_mitm_start_time = time.time() # Start timer for K1/K2 MITM

    P_FIXED_IV = b'\x00'*8
    target_val = found_k_const

    log.info("Building map for E_K1(P_FIXED_IV)...")
    map_k1_to_intermediate = {}
    for k1_candidate in range(2**20):
        bf1_k1 = Blowfish.new(int.to_bytes(k1_candidate, 4, 'big'), Blowfish.MODE_CFB, P_FIXED_IV)
        intermediate1 = bf1_k1.encrypt(P_MSG_INTERNAL_FOR_K1K2_MITM)
        map_k1_to_intermediate[intermediate1] = k1_candidate

    log.info("Iterating for K2 and checking against K1 map...")
    found_k1 = None
    found_k2 = None
    for k2_candidate in range(2**20):
        bf2_k2_decryptor = Blowfish.new(int.to_bytes(k2_candidate, 4, 'big'), Blowfish.MODE_CBC, P_FIXED_IV)
        decrypted_intermediate = bf2_k2_decryptor.decrypt(target_val)

        if decrypted_intermediate in map_k1_to_intermediate:
            found_k1 = map_k1_to_intermediate[decrypted_intermediate]
            found_k2 = k2_candidate
            log.success(f"Found K1: {hex(found_k1)}")
            log.success(f"Found K2: {hex(found_k2)}")
            break

    k1k2_mitm_end_time = time.time() # End timer for K1/K2 MITM
    log.info(f"K1/K2 Meet-in-the-Middle complete in {k1k2_mitm_end_time - k1k2_mitm_start_time:.2f} seconds.")

    if found_k1 is None or found_k2 is None:
        log.error("Failed to find K1 or K2. Exiting.")
        r.close()
        return

    log.info("Combining keys and sending 'G' command...")
    final_key = found_k1 | (found_k2 << 20) | (found_k3 << 40)
    log.success(f"Final calculated key: {hex(final_key)}")

    key_hex_str = f'{final_key:015x}' # Ensure 15 hex digits, padded with leading zeros

    # --- Final 'G' command submission ---
    # After 255 queries, the server is waiting directly for the 'G' command.
    # It does NOT send another prompt. We just send the key.
    r.sendline(b"G" + key_hex_str.encode())

    flag_response = r.recvline().strip().decode()
    log.success(f"Server response: {flag_response}")

    r.close()
    overall_end_time = time.time() # End overall timer
    log.info(f"Connection closed. Overall script execution time: {overall_end_time - overall_start_time:.2f} seconds.")

if __name__ == '__main__':
    solve()
