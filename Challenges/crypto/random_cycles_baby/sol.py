#key = {'f': 21, 'l': 45, 'a': 4, 'g': 53, '{': 20, '4': 21, 'p': 48, 'r': 30, 'e': 40, 'n': 28, 't': 17, 'y': 54, '_': 41, '1': 3, 's': 20, 'c': 63, 'o': 42, '0': 36, 'w': 21, '3': 5, 'i': 13, 'u': 38, '7': 41, '5': 1, '}': 17}
#output = "f_py3ngye13l3iotcne4t4_uea4nrp_ssfe5aew4_s{4p1_0c___}574nttlrnr_1sl_s"
key = {'f': 18, 'l': 58, 'a': 22, 'g': 30, '{': 33, '4': 63, 'p': 68, 'r': 47, 'e': 6, 'n': 56, 't': 5, 'y': 40, '_': 17, '1': 30, 's': 53, 'c': 54, 'o': 63, '0': 67, 'w': 3, '3': 20, 'i': 26, 'u': 37, '6': 16, '5': 26, '9': 63, '8': 50, '}': 26}
output = "fsa3n_yt0yt_e1_tn_9_ctpf_1n54s1_psui8op{}g4s_rcr4l1n4e3wllrs16e_3ea_n"

def spin(w, k):
    k = k % len(w)
    return w[-k:] + w[:-k]

def encrypt_or_hash(flag, key):
    for i in range(1, len(flag)):
        flag = flag[:i] + spin(flag[i:], key[flag[i-1]])
    return flag

#output = encrypt_or_hash(flag, key)

def reverse_spin(w, k):
    k = k % len(w)
    return  w[k:] + w[:k]

def main():
    flag = output
    for i in reversed(range(1, len(flag))):
        print(flag)
        flag = flag[:i] + reverse_spin(flag[i:], key[flag[i-1]])
    
    print(flag)


if __name__ == "__main__": main()