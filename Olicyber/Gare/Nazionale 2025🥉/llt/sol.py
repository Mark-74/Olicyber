#!/usr/bin/env python3
from scapy.all import rdpcap, IP, ICMP

PCAP_FILE = "llt.pcap"
SRC_IP    = "172.19.0.2"
DST_IP    = "172.67.157.96"

flag = []

def main():
    packets = rdpcap(PCAP_FILE)

    for pkt in packets:
        if IP in pkt and ICMP in pkt:
            ip  = pkt[IP]
            icm = pkt[ICMP]
            # 8 = request
            if icm.type == 8 and ip.src == SRC_IP and ip.dst == DST_IP:
                flag.append(ip.ttl)

if __name__ == "__main__":
    main()
    print("Flag:", "".join(map(chr, flag)))
