import socket
import threading
import connection
import server

class Acceptor(threading.Thread):
	def __init__(self, port):
		threading.Thread.__init__(self)
		self.conn = connection.Connection()
		self.conn.bind(('', port))
		self.conn.listen(10)
		self.serverList = []
	def run(self):
		while True:
			(sock, address) = self.conn.accept()
			conn = connection.Connection(sock)
			serverRunner = server.Server(conn)
			for s in self.serverList:
				with serverRunner.connLock:
					serverRunner.connList.append(s.client)
				with s.connLock:
					s.connList.append(serverRunner.client)
			self.serverList.append(serverRunner)
			serverRunner.start()

port = int(raw_input('Enter port # '))
a = Acceptor(port)
a.run()
