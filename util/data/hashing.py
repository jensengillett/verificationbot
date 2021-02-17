import hashlib


class Hashing:
	def __init__(self, salt: str):
		"""Test

		Args:
			salt (str): A string of text that is added to a hash to prevent a hash from being recreated. This should be kept private!
		"""

		self.salt = salt

	def hash(self, string: str):
		"""Converts a string to a hash

		Args:
			string (str): String to convert

		Returns:
			str: Hashed string
		"""

		if not self.salt:
			return string

		hashed = hashlib.md5(self.salt.encode() + string.encode())
		return hashed.hexdigest()

	def check_hash(self, string: str, md_hash: str):
		"""Checks if a string matches a MD5 hash

		Args:
			string (str): String to hash and compare
			md_hash (str): Hash to compare

		Returns:
			bool: Returns true if hashes match.
		"""

		hashed = self.hash(string)
		return hashed == md_hash
