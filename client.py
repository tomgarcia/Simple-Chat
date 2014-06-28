import threading
import connection
import time
import calendar

class Client:
	def __init__(self, serverAddress, uname):
		self.serverAddress = serverAddress
		self.conn = connection.Connection()
		self.uname = uname
	def run(self):
		self.conn.connect(self.serverAddress)
		printThread = threading.Thread(target = self.printMsg)
		printThread.start()
		while True:
			msg = {'type': 'message',  'username': self.uname, 'text': raw_input(), 'time': time.asctime(time.gmtime())}
			self.conn.send(msg)
	def printMsg(self):
		while True:
			msgList = self.conn.recv()
			for msg in msgList:
				timeStruct = time.strptime(msg['time'])
				secs = calendar.timegm(timeStruct)
				localtime = time.localtime(secs)
				ltimeString = time.strftime('[%I:%M %p] ', localtime)
				print ltimeString + msg['username'] + ' -- ' + msg['text']

address = raw_input('Enter server address ')
port = int(raw_input('Enter port # '))
uname = raw_input('Enter username ')
client = Client((address, port), uname)
client.run()
