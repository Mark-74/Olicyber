from Crypto.Util.number import getPrime, bytes_to_long
from secret import flag

p,q = getPrime(1024), getPrime(1024)
n = p*q
e = n-p-q+4 

# e = n - p - q + 4 = pq - p - q + 1 + 3 = p(q-1) - (q-1) + 3 = (p-1)(q-1) + 3
# ct = m^e mod n = (m ^ (phi(n) + 3)) % n 
# dato che x^(a+b) = x^a * x^b
# ct = (m ^ phi(n) * m^3) % n
# dato che m^phi(n) = 1
# ct = (1 * m^3) % n = m^3 % n

ct = pow(bytes_to_long(flag), e, n)

print("n =", n)
print("ct =", ct)
