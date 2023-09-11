import socket
import chatlib
import select
import random
import json

# GLOBALS
users = {}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"
MAX_MSG_LENGTH = 1024


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
	to_send = chatlib.build_message(code, msg)
	conn.send(to_send.encode())
	print("[SERVER SENT:] ", to_send)	  # Debug print


def recv_message_and_parse(conn):
	full_msg = conn.recv(chatlib.MAX_MSG_LENGTH).decode()
	cmd, data = chatlib.parse_message(full_msg)
	print("[CLIENT SENT:] ", full_msg)  # Debug print
	return cmd, data


# Data Loaders #

def load_questions():
	"""
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: questions dictionary
	"""

	try:
		with open('questions.json', 'r', encoding='utf-8') as file:
			questions_data = json.load(file)
			return questions_data
	except FileNotFoundError:
		print(f"The file 'questions.json' was not found.")
		return {}


def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""

	data = {}
	with open('users.json', 'r', encoding='utf-8') as file:
		user_data = json.load(file)
		data.update(user_data)
	return data

# SOCKET CREATOR

def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""
	print("SETTING UP SERVER....")
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((SERVER_IP, SERVER_PORT))
	sock.listen()
	print("LISTENING FOR CLIENTS.")
	return sock
	

def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	to_send = chatlib.build_message("ERROR", error_msg)
	conn.send(to_send.encode())


##### MESSAGE HANDLING


def handle_getscore_message(conn, username):
	global users
	to_send = str(users[username]["score"])
	build_and_send_message(conn, "YOUR_SCORE", to_send)


def handle_highscore_message(conn):
	global users
	results = ""

	for i in range(5):
		max_score = 0
		max_name = ""
		for user in users:
			sub_dict = users[user]
			val = sub_dict["score"]
			if max_score <= val and user not in results:
				max_score = val
				max_name = user
		if max_name != "":
			results += max_name+":"+str(max_score)+"\n"

	build_and_send_message(conn, "ALL_SCORE", results)


def handle_logged_message(conn):
	global logged_users
	to_send = ""
	for logged_user in logged_users:
		to_send += logged_users[logged_user]+","
	build_and_send_message(conn, "LOGGED_ANSWER", to_send[:-1])

	
def handle_logout_message(conn):
	"""
	Closes the given socket (in laster chapters, also remove user from logged_users dictionary)
	Recieves: socket
	Returns: None
	"""
	global logged_users
	if str(conn.getpeername()) in logged_users:
		del logged_users[str(conn.getpeername())]
	conn.close()
	

def handle_login_message(conn, data):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Receives: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users
	global logged_users
	lst = data.split("#")
	user_name = lst[0]
	password = lst[1]

	if user_name in users:
		if password == users[user_name]["password"]:
			to_send = chatlib.build_message("LOGIN_OK", "")
			conn.send(to_send.encode())
			logged_users[str(conn.getpeername())] = user_name
			print("NEW USER ENTERED THE GAME: "+ user_name)
			print("NOW LOGGED IN: ", logged_users)
		else:
			send_error(conn, password + " is not a valid password")
	else:
		send_error(conn, user_name+" is not a valid user")


def handle_register_massage(conn, data):
	global users
	reg = data.split("#")

	if reg[0] in users:
		build_and_send_message(conn, "FAILED_REG", "username already exist")
		return

	tmp = {"password": reg[1], "score": 0, "questions_asked": []}
	users[reg[0]] = tmp
	with open('users.json', 'w', encoding='utf-8') as file:
		json.dump(users, file, indent=4)
	build_and_send_message(conn, "SEC_REG", "")


def handle_client_message(conn, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Receives: socket, message code and data
	Returns: None
	"""
	global logged_users	 # To be used later

	if str(conn.getpeername()) not in logged_users:
		if cmd == "LOGIN":
			print(str(conn.getpeername()) + "IS TRYING TO ENTER THE GAME.")
			handle_login_message(conn, data)
			return
		if cmd == "REGISTER":
			handle_register_massage(conn, data)
			return
	else:
		if cmd == "LOGOUT":
			handle_logout_message(conn)
			return
		if cmd == "MY_SCORE":
			handle_getscore_message(conn, logged_users[str(conn.getpeername())])
			return
		if cmd == "HIGHSCORE":
			handle_highscore_message(conn)
			return
		if cmd == "LOGGED":
			handle_logged_message(conn)
			return
		if cmd == "GET_QUESTION":
			handle_question_message(conn)
			return
		if cmd == "SEND_ANSWER":
			to_user_name = logged_users[str(conn.getpeername())]
			handle_answer_message(conn,to_user_name, data)
			return

	send_error(conn, "Unknown command, please try again.")


def create_random_question():
	global questions
	random_number = random.randint(0, len(questions)-1)
	res = str(random_number)+"#"
	sub_dict = questions[str(random_number)]
	tmp1 = sub_dict["question"]
	res = res+tmp1+"#"
	tmp2 = sub_dict["answers"]
	for ans in tmp2:
		res = res+ans+"#"
	return res[:-1]


def handle_question_message(conn):
	build_and_send_message(conn, "YOUR_QUESTION", create_random_question())


def handle_answer_message(conn, user_name, data):
	global users
	data2 = data.split("#")
	sub_dict = questions[data2[0]]
	correct_answer = sub_dict["correct"]

	if int(correct_answer) != int(data2[1]):
		build_and_send_message(conn, "WRONG_ANSWER", str(correct_answer))
	else:
		users[user_name]["score"] += 5
		with open('users.json', 'w', encoding='utf-8') as file:
			json.dump(users, file, indent=4)
		build_and_send_message(conn, "CORRECT_ANSWER", "")


def main():
	global users
	global questions
	users = load_user_database()
	questions = load_questions()

	print("WELCOME TO TRIVIA SERVER!")
	server_socket = setup_socket()
	client_sockets = []

	while True:
		ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, [], [])
		for current_socket in ready_to_read:
			# Handling a new client:
			if current_socket is server_socket:
				(client_socket, client_address) = current_socket.accept()
				client_sockets.append(client_socket)
				print("NEW CLIENT CONNECTED: IP: "+client_address[0]+" PORT: "+str(client_address[1]))
			else:
				try:
					cmd, data = recv_message_and_parse(current_socket)
					if data is None or cmd == "LOGOUT":
						client_sockets.remove(current_socket)
						handle_logout_message(current_socket)
					else:
						handle_client_message(current_socket, cmd, data)
				except socket.error as e:
					client_sockets.remove(current_socket)
					handle_logout_message(current_socket)
					current_socket.close()


if __name__ == '__main__':
	main()

	