import socket
import sys
import time
import threading

localhost = ''
port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#socket bind
try:
	s.bind((localhost, port))
except socket.error as msg:
	print "Bind failed. Error code : " + str(msg[0]) + " Message : " + str(msg[1])
	sys.exit()

#socket listen
s.listen(10)
#accept a socket
lock = threading.Lock()

def clientthread(conn, addr):	
	while True:
		seq = conn.recv(1024)
		if not seq: break
		lock.acquire()
		print "recv from " + addr[0] + ':' + str(addr[1]) + ", seq = " + seq
		lock.release()
		conn.sendall(seq)
	conn.close()

while 1:
	conn, addr = s.accept()
	t = threading.Thread(target = clientthread, args = (conn, addr))
	t.start()
s.close()