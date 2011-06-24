#!/usr/bin/python

from socket import *
myHost = '127.0.0.1'
myPort = 3724

s = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
s.bind((myHost, myPort))            # bind it to the server port
s.listen(5)                         # allow 5 simultaneous
                                    # pending connections


while True:
    # wait for next client to connect
    connection, address = s.accept() # connection is a new socket
    print "Connection established"
    data = connection.recv(1024)
    connection.send('0000002156910f822daca52a522b19c17a395e7882138fda79d52e2279944e7169d35b010720b79b3e2a87823cab8f5ebfbf8eb10108535006298b5badbd5b53e1895e644b8935c6bb55652e2e18f2824c4836b883aa008bc33924e7cf44ee262e5f924823f2f52af78434388d10dff948d3b6ba81d200'.decode("hex"))
    data = connection.recv(1024)
    print data.encode('hex')
    connection.send('0100c5a33daa48c7e303a2fe357e20459be55db3c5ed000000000000'.decode("hex"))
    data = connection.recv(1024)
    connection.send('102c000000000001000000004176616c6f6e0039312e3132312e31312e3231373a38303835008fc2f53e01012c1000'.decode("hex"))
    connection.close()              # close socket
