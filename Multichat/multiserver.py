import socket
import select

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5678
MAX_MSG_LEN = 1024


def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())


def main():
    print("Setting up server..")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen()
    print("Listening for clients")
    client_sockets = []

    while True:
        ready_to_read, ready_to_write, in_error = select.select([sock]+client_sockets,[],[])
        for current_socket in ready_to_read:
            if current_socket is sock:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined: ")
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)
            else:
                print("New message from client!")
                data = current_socket.recv(MAX_MSG_LEN).decode()
                if data == "":
                    current_socket.send("Bye!".encode())
                    print("Connection closed")
                    client_sockets.remove(current_socket)
                    current_socket.close()
                    print_client_sockets(client_sockets)
                else:
                    print(data)
                    current_socket.send(data.encode())



if __name__ == '__main__':
    main()