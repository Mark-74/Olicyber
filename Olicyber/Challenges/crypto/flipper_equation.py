import requests
from pwn import xor
import base64

URL = "http://flipper-equation.challs.olicyber.it/"

token = base64.b64decode(requests.get(URL + 'save_session').json().get("token"))
blocks = [token[i:i+16] for i in range(0, len(token), 16)]

second_plain        = b";pts=00000000000"
second_objective    = b";pts=10000000000"

new_block_1 = xor(blocks[0], second_plain, second_objective)
blocks[0] = new_block_1

print("token: " + base64.b64encode(b"".join(blocks)).decode())