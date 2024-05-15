from pwn import *
    
def Or(a: hex, b:hex) -> hex :
    a = int(a, 16)
    b = int(b, 16)
    
    result = a | b
    return hex(result)
        
def main():
    r = remote("segreto.challs.olicyber.it", 33000)
    
    for i in range(10):
        res = 0x0
        
        for j in range(10):
            r.recvuntil(">")
            r.sendline(str(j))
            if not res: res = hex(int(r.recvline(),16))
            else: res = Or(res, hex(int(r.recvline(),16)))
            
        r.sendline(b"g")
        r.recvuntil(b"?")
        r.sendline(str(res)[2:])
        
    r.interactive()
    
if __name__ == "__main__":
    main()