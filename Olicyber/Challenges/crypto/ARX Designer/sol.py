def prng(n, seed, iterations):
  numbers = []
  for _ in range(iterations):
    seed = (seed ** 2) % n
    numbers.append(seed)
  return numbers

def decrypt(key, encrypted):
  decrypted = b''
  for i in range(len(encrypted) // 32):
    decrypted += decrypt_block(key, encrypted[32*i:32*i+32])
  
  return decrypted
    
def decrypt_block(key, block):
  assert len(key) == 32
  assert len(block) == 32
  k2, k1 = key[:16], key[16:32]
  b1, b2 = block[:16], block[16:]
  for r in range(10):
    b1 = xor(b1, k1)
    b1 = back_ror(b1, 31)
    b2 = xor(b2, k2)
    b2 = sub(b2, b1)
    '''
    b2 = add(b1, b2)
    b2 = xor(b2, k2)
    b1 = ror(b1, 31)
    b1 = xor(b1, k1)
    '''
        
  return b1 + b2

def xor(a, b):
    return bytes([x^y for x,y in zip(a,b)])

def back_ror(x, n):
  return int.to_bytes(((int.from_bytes(x, 'big') & ((1<<128-n)-1)) << n) | (int.from_bytes(x, 'big') >> (128-n)), 16, 'big')
   
def sub(a, b):
  return int.to_bytes((int.from_bytes(a, 'big') - int.from_bytes(b, 'big')) & ((1<<128)-1),16, 'big')

def main():
    n = 28087460813174486059034414551240249788023923756050759856308458322681826441049323969972913966894664237696959566808290405727732350393345948504891177099061573610135163058514828369697643042666005384521714256517991315882984306833419862539867692692716617074207808746659453884745255262698130584357835902471931699817647567728572688737596486809390298684489842424609146835280833441401592250553573771844222020121038815882223862298294665424093073182955018154044019485219838690648719703150807518955331895641688078886409605207252562543480484708396495057837290115243183136250323437141077720724973892227190571167633700090224634792701
    enc = bytes.fromhex("f12d1653bd9d4c3196860b77ffbe1862c67aca872cf2f793b97678f2478c6b7a9859372ac514d815a28a2657060b64777a272ef12c2c670f908266e4df0e8243")

    for seed in range(1000000):
    # integer between 0 and 999999, I hope it is enough

        key = int.to_bytes(prng(n, seed, 10)[-1], 2048//8, 'big')[16:16+32]
        res = decrypt(key, enc)
        
        if b'flag' in res:
          print(res)
          break
        
if __name__ == "__main__":
    main()