"""
This file is for converting the existing used_emails
data to a set of hashed used_emails. This file can be
removed once data hashing transfer is completed.
"""

import sys
import hashlib

hash_key = "hashkey"  # Set this to your key you wish to hash the data with
file_to_hash = "hashme.txt"  # File to hash
file_dest = "hashed.txt"  # Complete, hashed file destination


class Hashing:
	def __init__(self, salt: str):
		self.salt = salt

	def hash(self, string):
		if not self.salt:
			return string

		hashed = hashlib.md5(self.salt.encode() + string.encode())
		return hashed.hexdigest()

	def check_hash(self, string, md_hash):
		hashed = self.hash(string)
		return hashed == md_hash


hashing = Hashing(hash_key)

with open(file_to_hash, "r") as file:
	with open(file_dest, "w") as file_h:
		for line in file:
			line = line.strip('\n')
			hashed_line = hashing.hash(line)
			file_h.write(f"{hashed_line}\n")
			print(f"Wrote {line} as {hashed_line}")

print("\nChecking to make sure everything was hashed correctly...")
with open(file_to_hash, "r") as file:
	for i, line in enumerate(file):
		with open(file_dest, "r") as file_h:
			h_lines = file_h.readlines()
			checked = hashing.check_hash(line.strip('\n'), h_lines[i].strip('\n'))
			print(f"{'Match ' if checked else 'No Match '}\t", line.strip('\n'), h_lines[i].strip('\n'))
