import subprocess
import pyshark
import os

def send(message: str, dest: str):
    npath = os.path.join(os.getcwd(), 'win', 'src', 'nmap', 'nping.exe')
    command = [
        npath, '--icmp', '--data-string', message, '--count', '1', dest
    ] 
    subprocess.run(command)
    print("\n\n\n")

def cap_packet(interface):
    cap = pyshark.LiveCapture(interface=interface, bpf_filter='icmp')
    i = 0
    while(i != 1):
        cap.sniff(packet_count=1)
        cap
        for packet in cap.sniff_continuously(packet_count=5):
            print('Just arrived:', packet)