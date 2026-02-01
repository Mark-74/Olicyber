from math import gcd, lcm
from Crypto.Util.number import isPrime
from pwn import remote

r = remote("nt-master.challs.olicyber.it", 11001)

'''
I'll give you a positive integer N, can you give me two positive integers a,b such that a>b and gcd(a,b)+lcm(a,b)=N?
You must send the values of a and b separated by a space.
You have 1 second for each of the 10 tests.
'''

for t in range(10):
    r.recvuntil(b'N = ')
    N = int(r.recvline().strip())
    a, b = N-1, 1
    
    r.sendline(f"{a} {b}".encode())

print(r.recvall(timeout=1).decode())
