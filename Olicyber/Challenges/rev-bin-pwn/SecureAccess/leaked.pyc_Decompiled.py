# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: leaked.py
# Bytecode version: 3.8.0rc1+ (3413)
# Source timestamp: 2023-10-26 17:39:19 UTC (1698341959)

import hashlib
import json
import base64

def generate_token(nonce: str):
    username = 'user001'
    secret = hashlib.sha256(username.encode() + nonce.encode()).hexdigest()
    bundle = {'user': username, 'secret': secret}
    return base64.b64encode(json.dumps(bundle).encode())


# My solution

nonce = '37A2C4D2-AF65-4584-BF09-135972310A1B' # different, get it from stage2
print(generate_token(nonce).decode())
