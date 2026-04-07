#!/bin/python

def perfect(s):
	s = s.replace("à", "&agrave")
	s = s.replace("è", "&egrave")
	s = s.replace("é", "&eacute")
	s = s.replace("ì", "&igrave")
	s = s.replace("ò", "&ograve")
	s = s.replace("ù", "&ugrave")
	s = s.replace("&lt;", "<")
	s = s.replace("&gt;", ">")
	s = s.replace("[b]", "<strong>")
	s = s.replace("[/b]", "</strong>")
	s = s.replace("&quot;", "\"")
	s = s.replace("&ldquo;", "\"")
	s = s.replace("&rdquo;", "\"")
	s = s.replace("\'", "'")
	s = s.replace("\\\\", "\\")
	return s

def encrypt(s, key):
	# Setup
	final = ''
	s = perfect(s)
	key = [ int(x) for x in key ]
	key_length = len(key)
	key_index = -1

	for i in range(len(s)):
		element = s[i]
		result = element
		# Char to code
		if ord(element) >= ord('a') and ord(element) <= ord('z'):
			var = ord(element) - ord('a') + 1
		elif ord(element) >= ord('A') and ord(element) <= ord('Z'):
			var = ord(element) - ord('A') + 101
		else:
			var = -100

		# Encrypt
		key_index += 1
		key_index %= key_length
		if var != 0: var += key[key_index]
		if var > 100:
			if var > 126: var -= 26
		else:
			if var > 26: var -= 26
		
		# Code to char
		if var >= 1 and var <= 26:
			result = chr(ord('a') + var -1)
		elif var >= 101 and var <= 126:
			result = chr(ord('A') + var - 101)
		final += result
	return final

def decrypt(s, key):
	# Setup
	final = ''
	s = perfect(s)
	key = [ int(x) for x in key ]
	key_length = len(key)
	key_index = -1

	for i in range(len(s)):
		element = s[i]
		result = element
		# Char to code
		if ord(element) >= ord('a') and ord(element) <= ord('z'):
			var = ord(element) - ord('a') + 1
		elif ord(element) >= ord('A') and ord(element) <= ord('Z'):
			var = ord(element) - ord('A') + 101
		else:
			var = -100

		# Encrypt
		key_index += 1
		key_index %= key_length
		if var != 0: var -= key[key_index]
		if var > 100:
			if var < 101: var += 26
		else:
			if var < 1: var += 26
		
		# Code to char
		if var >= 1 and var <= 26:
			result = chr(ord('a') + var -1)
		elif var >= 101 and var <= 126:
			result = chr(ord('A') + var - 101)
		final += result
	return final

print(encrypt('testo di prova 1234', '693141335382539823945172975697'))
print(decrypt(encrypt('testo di prova 1234', '693141335382539823945172975697'), '693141335382539823945172975697'))
