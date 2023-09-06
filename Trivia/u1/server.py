import socket
import chatlib

# GLOBALS
users = {}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
	to_send = chatlib.build_message(code, msg)
	conn.send(to_send.encode())
	print("[SERVER] ", to_send)	  # Debug print

def recv_message_and_parse(conn):
	full_msg = conn.recv(chatlib.MAX_MSG_LENGTH).decode()
	cmd, data = chatlib.parse_message(full_msg)
	print("[CLIENT] ", full_msg)  # Debug print
	return cmd, data


# Data Loaders #

def load_questions():
	"""
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: questions dictionary
	"""
	questions = {
				2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
				4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3} 
				}
	
	return questions

def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""
	users = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]}
			}
	return users

	
# SOCKET CREATOR

def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""
	print("Setting up server..")
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((SERVER_IP, SERVER_PORT))
	sock.listen()
	print("Listening for clients")
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
	# Implement this in later chapters

	
def handle_logout_message(conn):
	"""
	Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
	Recieves: socket
	Returns: None
	"""
	conn.close()
	global logged_users
	



def handle_login_message(conn, data):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  # This is needed to access the same users dictionary from all functions
	global logged_users	 # To be used later
	lst = data.split("#")
	user_name = lst[0]
	password = lst[1]

	if user_name in users:
		if password == users[user_name]:
			to_send = chatlib.build_message("LOGIN_OK", "")
			conn.send(to_send.encode())
		else:
			send_error(conn, user_name + " is not a valid password")
	else:
		send_error(conn, user_name+" is not a valid user")


def handle_client_message(conn, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
	global logged_users	 # To be used later
	
	# Implement code ...
	


def main():
	# Initializes global users and questions dicionaries using load functions, will be used later
	global users
	global questions
	
	print("Welcome to Trivia Server!")
	
	# Implement code ...



if __name__ == '__main__':
	main()

	