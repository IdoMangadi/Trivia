# Protocol Constants
#all set ready to work!

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR"
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occured
	"""
	if (data is None) | (cmd is None) | (len(cmd) > 16) | (len(data) > MAX_DATA_LENGTH):
		return None

	msg_len = len(data)
	formatted_number = "{:04d}".format(msg_len)
	while len(cmd) < 16:
		cmd += " "
	full_msg = cmd+ "|" +formatted_number+ "|" + data
	return full_msg


def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""
	lst = data.split("|")
	if len(lst) != 3:
		return None, None

	cmd = lst[0].strip()
	msg = lst[2].strip()
	sec_f = lst[1].strip()

	if not sec_f.isdigit():  # or int(sec_f) != len(msg):
		return None, None

	return cmd, msg

	
def split_data(msg, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
	# Implement code:
	result = msg.split("#")
	if result.len == expected_fields+1:
		return result
	return None


def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	Returns: string that looks like cell1#cell2#cell3
	"""
	# Implement code:
	result = ""
	while len(msg_fields) != 0:
		result += str(msg_fields.pop)
		if len(msg_fields) != 0:
			result += "#"
	return result

