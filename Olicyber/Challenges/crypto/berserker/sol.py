from pwn import remote, args, process, log, xor
from Crypto.Util.Padding import pad
from tqdm import trange

FOUND_CHARS = 5
FLAG = 'flag{'

for i in range(27):
    if args.REMOTE:
        r = remote('berserker.challs.olicyber.it', 10507)
    else:
        r = process('python3 challenge.py', shell=True)

    # user={name};flag={flag}
    second_block = b'a'*16

    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'?', b'a'*11 + second_block + b'a'*(42 - FOUND_CHARS - 1))

    r.recvuntil(b': ')

    cookie = r.recvline().strip().decode()
    cookie = [cookie[i:i+32] for i in range(0, len(cookie), 32)]
    iv = cookie[-1]

    for j in trange(256):
        #             IV                 cookie[0]                 plain of cookie[1]
        payload = xor(bytes.fromhex(iv), bytes.fromhex(cookie[0]), second_block).hex()

        r.sendlineafter(b'> ', b'2')
        r.sendlineafter(b': ', payload.encode() + (b'a'*(42 - FOUND_CHARS - 1) + b';flag=' + FLAG.encode() + bytes([j])).hex().encode())

        x = r.recvuntil(b': ')

        res = r.recvline().strip().decode()
        res = [res[i:i+32] for i in range(0, len(res), 32)]

        iv = res[-1]

        if res[0] == cookie[1] and res[1] == cookie[2] and res[2] == cookie[3] and res[3] == cookie[4]:
            FOUND_CHARS += 1
            FLAG += chr(j)
            log.success(f'FLAG: {FLAG}')
            break

    r.close()

print(FLAG)