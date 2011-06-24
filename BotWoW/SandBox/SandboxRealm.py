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
    data = connection.recv(1024)
    connection.send('000000e3b5af11e6e87e7650a55fd62670a503d837812b08bc3bcae6c6cc1caafb413e010720b79b3e2a87823cab8f5ebfbf8eb10108535006298b5badbd5b53e1895e644b89fff3f2bd90c855d04a74109a138568df4c076354ca9f526eee0386ae9063dfcc97eab5ca00023dd512c0f85f679763ea00'.decode("hex"))
    data = connection.recv(1024)
    connection.send('0100c5a33daa48c7e303a2fe357e20459be55db3c5ed000000000000'.decode("hex"))
    data = connection.recv(1024)
    connection.send('102c000000000001000000004176616c6f6e0039312e3132312e31312e3231373a38303835008fc2f53e01012c1000'.decode("hex"))
    connection.close()              # close socket
