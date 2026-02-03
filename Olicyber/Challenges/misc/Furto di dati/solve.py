import pyshark
import base64

# Read ARP packets with src IP 1.3.3.7
cap = pyshark.FileCapture("furto.pcapng", display_filter="arp && arp.src.proto_ipv4 == 1.3.3.7")

packets = [(int(pkt.frame_info.number), pkt.arp.src_hw_mac.replace(":", "")) for pkt in cap]
packets.sort()

# hex MACs -> ASCII (base64) -> decode
b64_data = bytes.fromhex("".join(mac for _, mac in packets)).decode()
png_data = base64.b64decode(b64_data)

with open("flag.png", "wb") as f:
    f.write(png_data)

print("Saved flag.png")
