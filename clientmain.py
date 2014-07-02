import client
import clientview
import time

address = raw_input('Enter server address ')
port = int(raw_input('Enter port # '))
uname = raw_input('Enter username ')
model = client.Client((address, port), uname)
view = clientview.ClientView(model)
model.start()
view.start()

while True:
	#textbox = view.textbox
	#msg = {'type': 'message',  'username': model.uname, 'text': textbox.edit(), 'time': time.asctime(time.gmtime())}
	msg = {'type': 'message',  'username': model.uname, 'text': raw_input(),  'time': time.asctime(time.gmtime())}
	view.textwin.clear()
	view.scr.refresh()
	model.conn.send(msg)
