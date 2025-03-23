from pwn import remote
import subprocess

r = remote('rabbit.challs.olicyber.it', 10501)

r.recvuntil(b'Execute: ')
command = r.recvline().strip().decode()
output = subprocess.check_output(command, shell=True).strip()
r.sendline(output)

r.interactive()

'''
flag{l1nux_15_4_.....}                          env
flag{....c0mpl3x_And_4m4.....}                  /entrypoint.sh
flag{......Z1ng_cr34Tur3}                       /var/log/flg
flag{l1nux_15_4_c0mpl3x_And_4m4Z1ng_cr34Tur3}
'''