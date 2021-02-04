import hashlib


class Hashing:
	def __init__(self, salt: str):
		self.salt = salt

	def hash(self, string):
		if not self.salt:
			return string

		hashed = hashlib.sha256(self.salt.encode() + string.encode())
		return hashed.hexdigest()

	def check_hash(self, string, md_hash):
		hashed = self.hash(string)
		return hashed == md_hash
