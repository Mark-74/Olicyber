from pwn import *

if args.REMOTE:
    r = remote('pwnable.kr', 9022)
else:
    r = process('./memcpy') # will work with any input if the cpu is 64 bits, so run this in the challenge container

'''
The problem is that these instructions need to be aligned to 16 bytes, but malloc in a 32 bits system aligns to 8 bytes, not 16.

"movdqa (%0), %%xmm0\n"
"movdqa 16(%0), %%xmm1\n"
"movdqa 32(%0), %%xmm2\n"
"movdqa 48(%0), %%xmm3\n"
"movntps %%xmm0, (%1)\n"
"movntps %%xmm1, 16(%1)\n"
"movntps %%xmm2, 32(%1)\n"
"movntps %%xmm3, 48(%1)\n"

To solve, we need to make the destination (malloc(size)) aligned to 16 bytes by sending the correct values, calculated with the help of gdb running inside the challenge container.
The Dockerfile in this folder is modified and makes you root, so you can test too.

'''

r.sendline(b'8')
r.sendline(b'16')
r.sendline(b'32')
r.sendline(b'72')   # 64 + 8
r.sendline(b'136')  # 128 + 8
r.sendline(b'264')  # 256 + 8
r.sendline(b'520')  # 512 + 8
r.sendline(b'1032') # 1024 + 8
r.sendline(b'2056') # 2048 + 8
r.sendline(b'4104') # 4096 + 8

r.interactive()
