def is_valid_email(email: str):
	try:
		dm = email.split('@')[1]  # split the string based on the @ symbol
	except AttributeError:
		return False

	if not dm:
		return False

	if len(email.split('@')[0]) > 64 or len(email.split('@')[1]) > 255:  # valid emails have 64char max before @, 255 max after
		return False

	if set('+').intersection(email):  # to prevent people from making extra email addresses
		return False

	return True
