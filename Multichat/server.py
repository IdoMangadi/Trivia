import socket
from datetime import datetime

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5678

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SERVER_IP, SERVER_PORT))
sock.listen()
conn, addr = sock.accept()
print("Connected to"+ addr[0])
conn.send("Hi, we can start talk now".encode())

while True:
    data = conn.recv(4096).decode()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Friend: " + data + "  (" + current_time + ")")
    if data == "Bye":
        conn.send("Bye you to!".encode())
        break
    to_send = input("You:")
    conn.send(to_send.encode())
    now = datetime.now()
    print("  (" + now.strftime("%H:%M:%S") + ")")
    if to_send == "Bye":
        break

conn.close()



