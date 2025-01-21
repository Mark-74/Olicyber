from pwn import *

r = remote('pwnable.kr', 9022)

# segmentation fault cause: heap is not aligned to 16 bytes if the architecture is x86 (32 bit)
# we allineate the heap to 16 bytes by removing 8 bytes from the allocated chunk because malloc adds 8 bytes to the size of the chunk and so it wouldn't be aligned to 16 bytes

print(r.recvuntil(b':D\n'))
for i in range(1, 11):
    print(r.recvuntil(b':'))
    r.sendline(f'{(1<<(3+i))-8}'.encode())

r.recvuntil(b'flag : ')
print('flag' + r.recvline().decode())