import connection
import time
import calendar
import threading

class Server(threading.Thread):
	def __init__(self, conn, acceptor):
		threading.Thread.__init__(self)
		self.client = conn
		self.acceptor = acceptor
		self.uname = ''
		self.connList = []
		self.connLock = threading.Lock()
	def run(self):
		socketClosed = False
		while True:
			msg = self.client.recv()
			if msg is None:
				with self.acceptor.serverListLock:
					self.acceptor.serverList.remove(self)
					for s in self.acceptor.serverList:
						with s.connLock:
							s.connList.remove(self.client)
				msg = {'type': 'loginmsg', 'username': uname, 'text': uname + ' left the chat', 'time': time.asctime(time.gmtime())} 
				socketClosed = True
			if msg['type'] == 'login':
				uname = msg['username']
				self.client.send({'type': 'notification', 'user': uname, 'text': 'Welcome to the chat, ' + uname, 'time': time.asctime(time.gmtime())}) 
				msg = {'type': 'loginmsg', 'username': uname, 'text': uname + " joined the chat", 'time': time.asctime(time.gmtime())}
		#	msgList.sort(key = lambda msg: calendar.timegm(time.strptime(msg['time'])))
			if msg['type'] == 'notification':
				pass#self.users[msg['user']].send(msg)
			elif msg['type'] == 'loginmsg' or msg['type'] == 'message':
				with self.connLock:
					for conn in self.connList:
						conn.send(msg)
			if socketClosed:
				return
