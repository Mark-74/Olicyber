#!/usr/bin/env python3

# by extracting the adventure binary with a PyInstaller archive extractor we can get the source, in particular there is a file called adventure.pyc that has the main logic which is reported here.

def xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def givePiece(player, piece):
    key = b'cp\xc8\xec\xb0\xcc\x8e\x13\xa7\xcb0b\xd5\xf6sz\x13\x0eK\xed\xd52\x14\xe8e\x05\xb8\x93\x03\xf7QB\xfb\xde\xc9\xc4\x12\xeb'
    enc = b'\x13\x04\xa5\x97\xc7\xa4\xbeL\xc1\xfa^\x06\xa6\xa9G%ub\x7f\x8a\x8aT%\x86\x01v\xe7\xa7\\\xc0#q\xcf\xad\xbc\xb6!\x96'
    if piece == 1:
        player.inventory["First piece"] = [
         1, "legendary artifact", xor(key, enc).decode()[:13]]
    elif piece == 2:
        player.inventory["Second piece"] = [
         1, "legendary artifact", xor(key, enc).decode()[13:]]


key = b'cp\xc8\xec\xb0\xcc\x8e\x13\xa7\xcb0b\xd5\xf6sz\x13\x0eK\xed\xd52\x14\xe8e\x05\xb8\x93\x03\xf7QB\xfb\xde\xc9\xc4\x12\xeb'
enc = b'\x13\x04\xa5\x97\xc7\xa4\xbeL\xc1\xfa^\x06\xa6\xa9G%ub\x7f\x8a\x8aT%\x86\x01v\xe7\xa7\\\xc0#q\xcf\xad\xbc\xb6!\x96'
print(xor(key, enc).decode()[:13] +  xor(key, enc).decode()[13:])
