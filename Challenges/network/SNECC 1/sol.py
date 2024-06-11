#!/bin/python3
import pyshark
from pwn import *

cap = pyshark.FileCapture("traffic.pcap", display_filter="tcp")
numbers = dict()
flag = False
key = 0
for packet in cap:
    if 'data' in packet:
        try:
            num = int(bytes.fromhex(packet.data.data).decode('utf-8'))
        except:
            num = None
        if num and num > 5:
            if flag:
                flag = False
                numbers[key] = num
            else:
                flag = True
                key = num

r = remote("snecc.challs.olicyber.it", 12310)

num = int(r.recvline().decode().strip())
r.sendline(str(numbers[num]).encode())
r.interactive()