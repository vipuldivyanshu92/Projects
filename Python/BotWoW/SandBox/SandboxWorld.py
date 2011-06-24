#!/usr/bin/python

from socket import *
import time
myHost = '127.0.0.1'
myPort = 8085

s = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
s.bind((myHost, myPort))            # bind it to the server port
s.listen(5)                         # allow 5 simultaneous
                                    # pending connections


while True:
    # wait for next client to connect
    connection, address = s.accept() # connection is a new socket
    connection.send('0006ec01bebaadde'.decode("hex"))
    data = connection.recv(2048)
    connection.send('eee2c74a0c00000000020000000001'.decode("hex"))
    data = connection.recv(2048)
    connection.send('30abc575016d0e000000000000417274687572000101000102070606016c03000001000000cd927d46cdfa7d46fed45441000000000000a00001000000000000000000000000000000000000000000000000000000a32600000400000000000000000000a4260000079d27000008000000000000000000000000000000000000000000000000000000000000000000000006060000152a4900000e000000000000000000000000000000'.decode("hex"))
    connection.close()              # close socket
