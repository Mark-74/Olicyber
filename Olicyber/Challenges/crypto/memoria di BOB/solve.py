from pwn import remote, process, args
from base64 import b64decode
from string import printable
from Crypto.Util.Padding import pad

printable = printable.replace('\n', '')
if args.REMOTE:
    r = remote('bob.challs.olicyber.it', 10602)
else:
    r = process('./source.py')

plaintext = b'Cosa ne pensi? Bob: Ok. Allora mi puoi dare la flag? Alice: Nah, ma ti pare? Sono studiata io... Bob: Ma seriamente, ti immagini se qualcuno riuscisse ad ottenere i nostri messaggi?'
pre_padding = b'\x00'*11

while True:
    found = False
    
    if (len(plaintext) + 1) % 16 == 6:
        for c in printable:
            for d in printable:
                try:
                    payload = pad(c.encode() + d.encode() + plaintext, 16)
                    r.sendlineafter(b'Bob: ', pre_padding + payload + b' '*(2 + len(plaintext)))
                    r.recvuntil(b'messaggio!\n')
                    ciphertext = b64decode(r.recvline().strip())
                except EOFError:
                    r.close()
                    r = remote('bob.challs.olicyber.it', 10602)
                    payload = pad(c.encode() + d.encode() + plaintext, 16)
                    r.sendlineafter(b'Bob: ', pre_padding + payload + b' '*(2 + len(plaintext)))
                    r.recvuntil(b'messaggio!\n')
                    ciphertext = b64decode(r.recvline().strip())

                if len(plaintext) % 16 == 15:
                    guessing = ciphertext[-16*(len(plaintext)//16+2):-16*(len(plaintext)//16+1)]
                else:
                    guessing = ciphertext[-16*(len(plaintext)//16+1):-16*(len(plaintext)//16)]
                block = ciphertext[16:32]

                print(block.hex(), guessing.hex(), c + d)
                
                if block == guessing:
                    plaintext = c.encode() + d.encode() + plaintext
                    print(plaintext)
                    found = True
                    r.sendlineafter(b'Riprova pure premendo 1\n', b'1')
                    break
                
                r.sendlineafter(b'Riprova pure premendo 1\n', b'1')
            
            if found:
                break
            
    else:
        for c in printable:
            try:
                payload = pad(c.encode() + plaintext, 16)
                r.sendlineafter(b'Bob: ', pre_padding + payload + b' '*(1 + len(plaintext)))
                r.recvuntil(b'messaggio!\n')
                ciphertext = b64decode(r.recvline().strip())
            except EOFError:
                r.close()
                r = remote('bob.challs.olicyber.it', 10602)
                payload = pad(c.encode() + plaintext, 16)
                r.sendlineafter(b'Bob: ', pre_padding + payload + b' '*(1 + len(plaintext)))
                r.recvuntil(b'messaggio!\n')
                ciphertext = b64decode(r.recvline().strip())

            if len(plaintext) % 16 == 15:
                guessing = ciphertext[-16*(len(plaintext)//16+2):-16*(len(plaintext)//16+1)]
            else:
                guessing = ciphertext[-16*(len(plaintext)//16+1):-16*(len(plaintext)//16)]
            block = ciphertext[16:32]

            print([ciphertext[i*16:(i+1)*16].hex() for i in range(len(ciphertext)//16)])
            print(block.hex(), guessing.hex(), c, (-16*(len(plaintext)//15+1), (-16*(len(plaintext)//15))))

            if block == guessing:
                plaintext = c.encode() + plaintext
                print(plaintext)
                found = True
                r.sendlineafter(b'Riprova pure premendo 1\n', b'1')
                break
            
            r.sendlineafter(b'Riprova pure premendo 1\n', b'1')
            
    if not found:
        break

r.close()

print(f'Final plaintext: {plaintext}')
