import socket
import chatlib

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5678

# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    to_send = chatlib.build_message(code, data)
    conn.send(to_send.encode())


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
            return 1
        else:
            print(chatlib.PROTOCOL_SERVER["login_failed_msg"] + ": " + data)
        if input("1. Try again\n2. Back\nYour answer: ") == "2":
            return 0


def build_send_recv_parse(conn, cmd, data):
    build_and_send_message(conn, cmd, data)
    cmd2, data2 = recv_message_and_parse(conn)
    return cmd2, data2


def get_score(conn):
    cmd, data = build_send_recv_parse(conn, "MY_SCORE", "")
    if str(cmd) != "YOUR_SCORE":
        print("\nERROR")
    else:
        print("\nYOUR SCORE: "+ data)


def get_highscore(conn):
    cmd, data = build_send_recv_parse(conn, "HIGHSCORE", "")
    if str(cmd) != "ALL_SCORE":
        print("\nERROR")
    else:
        print("\nSCORES TABLE:\n"+ data)


def play_question(conn):
    cmd, q_data = build_send_recv_parse(conn, "GET_QUESTION", "")
    q_lst = q_data.split("#")
    print("\nQuestion number: "+q_lst[0]+": "+ q_lst[1]+"\n1. "+q_lst[2]+"\n2. "+q_lst[3]+"\n3. "+q_lst[4]+"\n4. "+q_lst[5])
    cmd2, data2 = build_send_recv_parse(conn, "SEND_ANSWER", q_lst[0]+"#"+input("Your answer: "))
    print("check"+str(cmd2))
    if str(cmd2) == "CORRECT_ANSWER":
        print("You are right!")
    else:
        print("You are wrong, the right answer is: "+ q_lst[int(data2)+1])


def get_logged_users(conn):
    cmd, data = build_send_recv_parse(conn, "LOGGED", "")
    print("\nThe logged in users now are: "+str(data))


def logout(conn):
    build_and_send_message(conn, "LOGOUT", "")


def register(conn):
    reg_user = input("Enter your new username: ")
    reg_pass = input("Enter you new password: ")
    build_and_send_message(conn, "REGISTER", reg_user+"#"+reg_pass)
    cmd, data = recv_message_and_parse(conn)
    if cmd == "SEC_REG":
        print("Successfully registered: "+reg_user)
    else:
        print("Registration failed because: "+data)


def main():
    print("Hi welcome to TRIVIA game !")
    first_input = input("1. Login\n2. Register\n3. Exit\nYour Answer:")
    while first_input == "1" or first_input == "2":
        sock = connect()
        if first_input == "1":
            login_check = login(sock)
            if login_check == 1:
                while True:
                    print("\nWhat would you like to do now?")
                    print("1 - Show my score")
                    print("2 - Show scores table")
                    print("3 - Play a question")
                    print("4 - See hou logged in")
                    print("5 - Logout")

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
        if first_input == "2":
            register(sock)
        sock.close()
        first_input = input("What would you like to do now?\n1. Login\n2. Register\n3. Exit\nYour Answer:")

    print("Bye Bye... :)")


if __name__ == '__main__':
    main()




