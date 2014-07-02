import client
import threading
import time
import calendar
import curses

class ClientView(threading.Thread):
	def __init__(self, model):
		threading.Thread.__init__(self)
		self.model = model
		self.log = model.log
		self.logLock = model.logLock
		self.logIndex = 0
		#self.scr = curses.initscr()
		#curses.noecho()
		#curses.cbreak()
		#self.scr.keypad(1)
	def run(self):
		while True:
			with self.logLock:
				while self.logIndex < len(self.log):
					msg = self.log[self.logIndex]
					timeStruct = time.strptime(msg['time'])
					secs = calendar.timegm(timeStruct)
					localtime = time.localtime(secs)
					ltimeString = time.strftime('[%I:%M %p] ', localtime)
					if msg['type'] == 'notification' or msg['type'] == 'loginmsg':
						print ltimeString + msg['text']
						#self.scr.addstr(ltimeString + msg['text'])
					elif msg['type'] == 'message':
						print ltimeString + msg['username'] + ' -- ' + msg['text']
						#self.scr.addstr(ltimeString + msg['username'] + ' -- ' + msg['text'])
					self.logIndex += 1
					#self.scr.move(self.logIndex, 0)
			#self.scr.refresh()
				self.logLock.wait()
