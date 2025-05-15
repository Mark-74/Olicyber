from Crypto.Util.number import bytes_to_long

the_username = bytes.fromhex('E5FD8D2CD9026BC6E6CE892DC44239D6F0CE8B7BCC14050000000000000000008391EC4BA2715AA2170000000000000000000000000000000000000000000000')
the_password = bytes.fromhex('5DFEE6A141574D6C47C7B19F8628536E16CBDF6E515D99000000000000000000E6957A3D20F81C3B17000000')

maximum = bytes_to_long(the_username[0x28:0x2c:][::-1])

username = [0 for i in range(maximum)]
password = [0 for i in range(maximum)]

for i in reversed(range(maximum)):
    username[i] = the_username[i] ^ the_username[i % 8 + 32]
    password[i] = (the_password[i] - the_password[i % 8 + 32]) & 0xff
    
print("username: ", ''.join([chr(i) for i in username]))
print("password: ", ''.join([chr(i) for i in password]))

print("flag:", ''.join([chr(i) for i in username] + [chr(i) for i in password]))
    
