import os

assert("FLAG" in os.environ)
FLAG = os.environ["FLAG"]
assert(FLAG.startswith("flag{"))
assert(FLAG.endswith("}"))

def gen_OTPs(key):
    for i in range(2, 10):
        yield i*key

key = int.from_bytes(os.urandom(len(FLAG)), 'big')
FLAG = int.from_bytes(FLAG.encode(), 'big')
bits = FLAG.bit_length()

for OTP in gen_OTPs(key):
    print((FLAG + OTP)%2**bits)
