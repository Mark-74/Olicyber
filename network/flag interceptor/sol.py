import pyshark
from collections import defaultdict

streams = defaultdict(str)

cap = pyshark.FileCapture("flag-interceptor.pcap", display_filter="tcp")

for packet in cap:
    if 'data' in packet:
        ip = packet.ip.src
        data = packet.data.data
        streams[ip] += bytes.fromhex(data).decode()[:-1]

for ip in streams:
    stream = streams[ip]
    
    if stream.startswith("flag{") and stream.endswith("}"):
        print(stream)