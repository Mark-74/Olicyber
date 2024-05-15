from Crypto.Util.number import long_to_bytes

Public_key = long_to_bytes(964964529)
secret = 170
result = ""

for i in Public_key:
    result += str(i ^ secret)

print(result)