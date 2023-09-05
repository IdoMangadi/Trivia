import socket
from datetime import datetime

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5678

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))

while True:
    data = sock.recv(4096).decode()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Friend: " + data + "  ("+current_time+")")
    if data == "Bye":
        sock.send("Bye you to!".encode())
        break
    to_send = input("You:")
    sock.send(to_send.encode())
    now = datetime.now()
    print("  (" + now.strftime("%H:%M:%S") + ")")
    if to_send == "Bye":
        break

sock.close()