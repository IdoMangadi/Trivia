import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5678
MAX_MSG_LEN = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))

while True:
    to_send = input("Enter your message: ")
    sock.send(to_send.encode())
    re = sock.recv(MAX_MSG_LEN).decode()
    if re == "Bye!":
        break
    print("Server says: " + re)

sock.close()
