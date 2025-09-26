import subprocess
import pyshark
import re
import binascii
import socket
import os

def send(message: str, dest: str):
    npath = os.path.join(os.getcwd(), 'win', 'src', 'nmap', 'nping.exe')
    command = [
        npath, '--icmp', '--data-string', message, '--count', '1', dest
    ] 
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("\n\n\n")

def cap_packet(interface: str):
    cap = pyshark.LiveCapture(interface=interface, bpf_filter='icmp')
    local_ip = socket.gethostbyname(socket.gethostname())
    for pkt in cap.sniff_continuously(packet_count=0):
        payload = None
        if 'IP' in pkt and pkt['IP'].src != local_ip:
            if 'DATA' in pkt:
                data_layer = pkt['DATA']
                if hasattr(data_layer, 'data'):
                    payload = data_layer.data
                elif hasattr(data_layer, 'payload'):
                    payload = data_layer.payload
                else:
                    payload = str(data_layer)
            elif 'ICMP' in pkt:
                icmp_layer = pkt['ICMP']
                for fname in ('data', 'payload', 'rest_of_header'):
                    val = getattr(icmp_layer, fname, None)
                    if val:
                        payload = val
                        break
            print('\n\n\n--- Received ---')
            if payload:
                hexstr = re.sub(r'[^0-9A-Fa-f]', '', str(payload))
                if len(hexstr) >= 2:
                    raw = binascii.unhexlify(hexstr[: (len(hexstr)//2)*2 ])
                    print('Decoded (utf-8):', raw.decode('utf-8', errors='replace'))
