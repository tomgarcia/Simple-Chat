import connection

class Server:
	def __init__(self, port):
		self.conn = connection.Connection()
		self.conn.bind(('', port))
		self.conn.listen(10)
		self.connList = []
	def run(self):
		while True:
			self.connList.extend(self.conn.accept())
			msgList = []
			for conn in self.connList:
				msgs = conn.recv()
				if msgs is None:
					self.connList.remove(conn)
				else:
					msgList.extend(msgs)
			for msg in msgList:
				for conn in self.connList:
					conn.send(msg)

port = int(raw_input('Enter port # '))
server = Server(port)
server.run()
