from win.client import send
import subprocess

subprocess.Popen(
    ["cmd", "/c", "start", "cmd", "/k", f"python3 receiver.py"],
    shell = True
)

i = 0
while (i != 1):
    msg = input("Message: ")
    dest = input("Destination: ")
    send(msg, dest)
