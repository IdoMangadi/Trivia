import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    to_send = chatlib.build_message(code, data)
    conn.send(to_send.encode())
    print("data sent: "+to_send)


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    full_msg = conn.recv(chatlib.MAX_MSG_LENGTH).decode()
    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data



def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    return sock


def error_and_exit(error_msg):
    print(error_msg)
    exit()


def login(conn):
    while True:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")

        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], username+"#"+password)
        cmd, data = recv_message_and_parse(conn)
        if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print(cmd)
            return
        else:
            print(chatlib.PROTOCOL_SERVER["login_failed_msg"])


def logout(conn):
    build_and_send_message(conn, "LOGOUT")


def main():
    sock = connect()
    login(sock)
    while True:
        print("What would you like to do now?")
        print("1 - Show your score")
        print("2 - Show scores table")
        print("3 - Play a question")
        print("4 - See hou logged in")
        print("5 - Quit")

        ans = input("Your answer:")

        if ans == "1":
            get_score(sock)
        if ans == "2":
            get_highscore(sock)
        if ans == "3":
            play_question(sock)
        if ans == "4":
            get_logged_users(sock)
        if ans == "5":
            break

    logout(sock)
    sock.close()


if __name__ == '__main__':
    main()


def build_send_recv_parse(conn, cmd, data):
    build_and_send_message(conn, cmd, data)
    cmd2, data2 = recv_message_and_parse(conn)
    return cmd2, data2


def get_score(conn):
    cmd, data = build_send_recv_parse(conn, "MY_SCORE")
    if cmd != "YOUR_SCORE":
        print("ERROR")
    else:
        print (data)


def get_highscore(conn):
    cmd, data = build_send_recv_parse(conn, "HIGHSCORE")
    if cmd != "ALL_SCORE":
        print("ERROR")
    else:
        print (data)


def play_question(conn):
    cmd, q_data = build_send_recv_parse(conn, "GET_QUESTION")
    q_lst = chatlib.split_data(q_data)
    print("Question number: "+q_lst[0]+": "+ q_lst[1]+"\n1. "+q_lst[2]+"\n2. "+q_lst[3]+"\n3. "+q_lst[4]+"\n4. "+q_lst[5])
    cmd2, data2 = build_send_recv_parse(conn, "SEND_ANSWER", q_lst[0]+"#"+input("Your answer: "))
    if cmd2 == "CORRECT_ANSWER":
        print("You are right!")
    else:
        print("You are wrong, the right answer is: "+ q_lst[data2+1])


def get_logged_users(conn):
    cmd, data = build_send_recv_parse(conn, "LOGGED")
    print("The logged in users now are: "+data)



