from pwn import remote, process, args
from Crypto.Util.Padding import pad

if args.REMOTE:
    r = remote('spg.challs.olicyber.it', 38052)
else:
    r = process('./secure_passphrase_generator.py')

payload = b'a;x=aa;' + pad(b'username=a;index0=0;index1=1;index2=2;index3=3', 16)
r.sendline(b'1')
r.sendlineafter(b'Username? ', payload)

r.recvuntil(b'Nel caso la dimenticassi, puoi recuperarla con il seguente token: ')
resp = r.recvline().strip().decode()

payload = b'username=' + payload
resp = bytes.fromhex(resp)

iv, ciphertext = resp[:16], resp[16:]
ciphertext = ciphertext[:len(payload)]

r.sendline(b'1')
r.sendlineafter(b'Username? ', b'a')

r.sendline(b'2')
r.sendlineafter(b'Token? ', (iv + ciphertext).hex())

r.recvuntil(b'flag')
flag = 'flag' + r.recvline().strip().decode().replace('-', '')

print(f'Flag: {flag}')
