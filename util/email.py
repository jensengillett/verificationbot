import re


def is_valid_email(email: str):

	# This is not a miracle-expression, but it should work for most cases.
	# 	RFC822 Compliant Regex is *much* longer (http://www.ex-parrot.com/~pdw/Mail-RFC822-Address.html).
	# 	Similar expressions are also long. This is (probably) the next best thing.
	# ---
	# Explanation:
	# 	\b (beginning boundary)
	# 	Local part: Matched if it contains a word-character or a %, +, or - and is between 1 and 64 chars.
	# 	@ (at-symbol in email)
	# 	Domain name: Matched if it contains a word-character or - and is between 1 and 255 chars.
	# 	. (period in domain)
	# 	Domain ending: Matched if alpha-character and is at least 2 characters long.
	# 	\b (ending boundary)
	regex = r"\b[\w.%+-]{1,64}@[\w.-]{1,255}\.[a-zA-Z-]{2,}\b"

	if(re.search(regex, email)):
		return True

	return False
