import threading
import socket

# Wrapper class for sockets, that improves functionality. 
# It sends dictionaries instead of strings.
class Connection:
	def __init__(self, sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
		self.sock = sock
	def connect(self, address):
		self.sock.connect(address)
	# msg is a dictionary, not a string
	def send(self, msg):
		msgString = 'type=' + msg['type']
		for key in msg.keys():
			if key != 'type':
				msgString += '\1B' + key + '=' + msg[key]
		self.sock.send(msgString)
	# Returns a message dictionary
	def recv(self):
		msgString = self.sock.recv(2048)
		if msgString == '':
			self.sock.close()
			return None
		else:
			msg = {}
			parsedMsg = msgString.split('\1B')
			for pair in parsedMsg:
				key = pair.split('=')[0]
				value = pair.split('=')[1]
				msg[key] = value
			return msg
	def bind(self, address):
		self.sock.bind(address)
	def listen(self, num):
		self.sock.listen(num)
	def accept(self):
		return self.sock.accept()
	def close(self):
		self.sock.close()

