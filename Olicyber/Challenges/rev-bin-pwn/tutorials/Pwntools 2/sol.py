from pwn import *

r = remote('software-18.challs.olicyber.it', 13001)

r.recvuntil(b'iniziare ...')
r.sendline()

for i in range(100):

    try:
        r.recvuntil(b'restituiscimi ')
    except:
        log.critical('Too slow')
        exit()
    
    res = r.recvline().strip().decode().split(' ')
    hex_number, mode, bit = res[0], res[1], res[-1]

    #r.recvuntil(b'Result : ')
    print(i+1, hex_number, mode, bit)

    if mode == 'packed':
        if bit == '32-bit':
            r.send(p32(int(hex_number, 16), endianness="little"))
        elif bit == '64-bit':
            r.send(p64(int(hex_number, 16), endianness="little"))

r.interactive()
    
