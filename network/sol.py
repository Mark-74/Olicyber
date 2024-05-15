from pyshark import *

capture = FileCapture("intercepted.pcap")

for packet in capture:
    print(packet)