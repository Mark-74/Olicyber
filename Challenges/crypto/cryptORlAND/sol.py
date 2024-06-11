from pwn import *

def main():
    r = connect("cryptorland.challs.olicyber.it", 10801)

    ciphertexts = []
    for i in range(10):
        ciphertexts.append(bin(int(r.recvline().decode()))[2:])
        
    print(ciphertexts)
    print(r.recvuntil(b"? "))
    
    result = ""
    temp = ""
    
    for i in range(len(ciphertexts)):
        while len(ciphertexts[i]) < 96:
            ciphertexts[i] = "0" + ciphertexts[i]
    
    for j in range(len(ciphertexts[0])):
        for i in ciphertexts:
            temp += i[j]
        result += findBit(temp)
        temp = ""
        
    print(int(result,2))
    r.sendline(str(int(result,2)))
    r.interactive()
    
    

def findBit(bits): #bits  must be a string
    one_count = 0
    zero_count = 0
    
    for i in bits:
        if i == "1": one_count += 1
        else: zero_count += 1

    if one_count > zero_count:return "1"
    else: return "0"

if __name__ == "__main__":
    main()
