import threading
import connection
import time

class Client(threading.Thread):
	def __init__(self, serverAddress, uname):
		threading.Thread.__init__(self)
		self.serverAddress = serverAddress
		self.conn = connection.Connection()
		self.uname = uname
		self.log = []
		self.logLock = threading.Condition(threading.Lock())
	def run(self):
		self.conn.connect(self.serverAddress)
		self.conn.send({'type': 'login', 'username': self.uname, 'time': time.asctime(time.gmtime())})
		while True:
			msg = self.conn.recv()
			if msg is not None:
				with self.logLock:
					self.log.append(msg)
					self.logLock.notify()

