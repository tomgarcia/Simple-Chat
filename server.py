import connection
import time
import calendar

class Server:
	def __init__(self, port):
		self.conn = connection.Connection()
		self.conn.bind(('', port))
		self.conn.listen(10)
		self.connList = []
		self.log = []
		self.users = {}
	def run(self):
		while True:
			self.connList.extend(self.conn.accept())
			msgList = []
			for conn in self.connList:
				msgs = conn.recv()
				if msgs is None:
					msgList.append({'type': 'loginmsg', 'username': conn.uname, 'text': conn.uname + ' left the chat', 'time': time.asctime(time.gmtime())}) 
					self.connList.remove(conn)
				else:
					for msg in msgs:
						if msg['type'] == 'login':
							conn.uname = msg['username']
							self.users[conn.uname] = conn
							msgList.append({'type': 'notification', 'user': conn.uname, 'text': 'Welcome to the chat, ' + conn.uname, 'time': time.asctime(time.gmtime())}) 
							msgList.append({'type': 'loginmsg', 'username': conn.uname, 'text': conn.uname + " joined the chat", 'time': time.asctime(time.gmtime()),}) 
						elif msg['type'] == 'message':
							if msg['text'] == 'log':
								print self.log
							msgList.append(msg)
			msgList.sort(key = lambda msg: calendar.timegm(time.strptime(msg['time'])))
			self.log.extend(msgList)
			for msg in msgList:
				if msg['type'] == 'notification':
					self.users[msg['user']].send(msg)
				elif msg['type'] == 'loginmsg' or msg['type'] == 'message':
					for conn in self.connList:
						if conn.uname != msg['username']:
							conn.send(msg)
port = int(raw_input('Enter port # '))
server = Server(port)
server.run()
