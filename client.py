import socket
import sys
import argparse
import time
import threading

#deal with argvs
parse = argparse.ArgumentParser()
parse.add_argument('.py')
parse.add_argument('-n', default = 0)
parse.add_argument('-t', default = 1000)
parse.add_argument('ip', nargs = '+')
args = parse.parse_args(sys.argv)
timeout = float(args.t)
packageN = int(args.n)
hostPort = args.ip
lock = threading.Lock()
#create a socket


def multithread(hostPort):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as msg:
		print 'Fails to create socket. Error code: ' + str(msg[0]) + ' , Error msg : ' + str(msg[1])
		sys.exit()
	host_name = hostPort.split(':')[0]
	host_ip = socket.gethostbyname(host_name)
	port = int(hostPort.split(':')[1])
	seq = 0
	while True:
		if seq == packageN :break
		try:
			time.sleep(1)
			s.__init__()
			s.settimeout(timeout)
			s.connect((host_ip, port))
			s.settimeout(None)
			error = False
			while True:
				tick = 0
				try:
					s.sendall(str(seq))
					tick = time.time()
				except Exception as e:
					error = True
				if error : break
				try:
					seq_back = None
					rtt = None
					s.settimeout(timeout/1000 - (time.time() - tick))
					seq_back = s.recv(1024)
					rtt = time.time() - tick
					s.settimeout(None)
					lock.acquire()
					print "recv from " + host_ip + ':' + str(port) + ", seq = " + seq_back + ", RTT = " + str(round(rtt * 1000, 3)) + " msec"
					lock.release()
					seq = seq + 1
					if seq == packageN : break
				except socket.timeout:
					lock.acquire()
					print "timeout when connect to " + host_ip + ":" + str(port) + ", seq = " + str(seq)
					lock.release()
					error = True
					seq = seq + 1
					if seq == packageN : break
				if error : break
				time.sleep(1)
			if error : continue
			break
		except Exception as e:
			lock.acquire()
			print "timeout when connect to " + host_ip + ":" + str(port) + ", seq = " + str(seq)
			lock.release()
			time.sleep(1)
			seq = seq + 1
			if seq == packageN : break
			continue
	s.close()
	
for i in range(0,len(hostPort)):
	t = threading.Thread(target= multithread, args= (hostPort[i],))
	t.daemon = True
	t.start()

while threading.active_count() > 1:
	pass

