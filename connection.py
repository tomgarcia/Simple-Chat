import threading
import socket

# Wrapper class for sockets, that improves functionality. 
# It sends dictionaries instead of strings, and handles all of the needed threads by itself.
class Connection:
	def __init__(self, sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
		self.sock = sock
		self.inbox = []
		self.inLock = threading.Lock()
		self.outbox = []
		self.outLock = threading.Lock()
		self.acceptList = []
		self.acceptLock = threading.Lock()
		self.sender = _Sender(self.sock, self.outbox, self.outLock)
		self.reciever = _Reciever(self.sock, self.inbox, self.inLock)
		self.acceptor = _Acceptor(self.sock, self.acceptList, self.acceptLock)
	def connect(self, address):
		self.sock.connect(address)
		self.sender.start()
		self.reciever.start()
	# msg is a dictionary, not a string
	def send(self, msg):
		with self.outLock:
			self.outbox.append(msg)
	# Returns a list containing all the messages (dictionaries) that have been sent
	# since the last call to recv(). Returns None if the connection is dead.
	# Unlike socket.recv(), this method is non-blocking. 
	def recv(self):
		with self.inLock:
			msgList = self.inbox
			with self.reciever.closeLock:
				if self.reciever.isClosed:
					self.reciever.msgList = None
				else:
					self.reciever.msgList = []
			self.inbox = self.reciever.msgList
		return msgList
	def bind(self, address):
		self.sock.bind(address)
	def listen(self, num):
		self.sock.listen(num)
		self.acceptor.start()
	# Returns a list of all Connections that have connected since the
	# last call to accept(). Unlike socket.accept(), this is non-
	# blocking.
	def accept(self):
		with self.acceptLock:
			alist = self.acceptList
			self.acceptList = []
			self.acceptor.connList = self.acceptList
		for conn in alist:
			conn.sender.start()
			conn.reciever.start()
		return alist
	def close(self):
		self.sock.close()

# Helper class for sending messages. Do not use directly: use
# Connection instead.
class _Sender(threading.Thread):
	def __init__(self, sock, msgList = [], msgLock = threading.Lock()):
		threading.Thread.__init__(self)
		self.sock = sock
		self.msgList = msgList
		self.msgLock = msgLock
	def run(self):
		while True:
			with self.msgLock:
				if len(self.msgList) > 0:
					msg = self.msgList.pop(0)
				else:
					continue
			msgString = 'type=' + msg['type']
			for key in msg.keys():
				if key != 'type':
					msgString += '\1B' + key + '=' + msg[key]
			try:
				self.sock.send(msgString)
			except:
				self.sock.close()
				return

# Helper class for recieving messages. Do not use directly: use
# Connection instead.
class _Reciever(threading.Thread):
	def __init__(self, sock, msgList = [], msgLock = threading.Lock()):
		threading.Thread.__init__(self)
		self.sock = sock
		self.isClosed = False
		self.closeLock = threading.Lock()
		self.msgList = msgList
		self.msgLock = msgLock
	def run(self):
		while True:
			msgString = self.sock.recv(2048)
			if msgString == '':
				self.sock.close()
				with self.closeLock:
					self.isClosed = True
				return
			else:
				msg = {}
				parsedMsg = msgString.split('\1B')
				for pair in parsedMsg:
					key = pair.split('=')[0]
					value = pair.split('=')[1]
					msg[key] = value
				with self.msgLock:
					self.msgList.append(msg)

# Helper class for accepting connections. Do not use directly: use
# Connection instead.  
class _Acceptor(threading.Thread):
	def __init__(self, sock, connList = [], connLock = threading.Lock()):
		threading.Thread.__init__(self)
		self.sock = sock
		self.connList = connList
		self.connLock = connLock
	def run(self):
		while True:
			(sock, address) = self.sock.accept()
			conn = Connection(sock)
			with self.connLock:
				self.connList.append(conn)
