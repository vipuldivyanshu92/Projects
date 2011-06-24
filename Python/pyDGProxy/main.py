#!/usr/bin/env python

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ServerFactory, ClientFactory
from twisted.internet.ssl import DefaultOpenSSLContextFactory, ClientContextFactory
from OpenSSL import SSL

# Defines
LISTEN_PORT = 443
PRIVATE_KEY_FILENAME = "server.pem"
CERTIFICATE_FILENAME = "server.pem"
CONNECTION_TIMEOUT = 20
MAX_NB_CONNECTIONS = 5

REMOTE_SERVER = "209.85.229.99"
REMOTE_PORT = 443

# Exceptions
class ProxyException(Exception):
    pass

class ProxyConnectException(Exception):
    pass

class ProxyLostConnectionException(Exception):
    pass
    
class SSLServerProxyProtocol(Protocol):
    def connectionMade(self):
        print "Received connection from %s:%d" % self.transport.getPeer()[1:]
        # Add one connection, and check if we still allow connections
        self.factory.nbConnections += 1
        if (self.factory.nbConnections > MAX_NB_CONNECTIONS):
            self.transport.loseConnection()
        
        # At this point create a connection to the server
        clientFactory = SSLClientProxyFactory(self)
        self.remote = reactor.connectSSL(REMOTE_SERVER, REMOTE_PORT, clientFactory, ClientContextFactory(), timeout=CONNECTION_TIMEOUT)
        
    def connectionLost(self, reason):
        self.remote.transport.loseConnection()
        self.factory.nbConnections -= 1
        
    def dataReceived(self, data):
        print "Data received on the listener [Length=%d]" % (len(data))
        print "Forwarding the data to the remote server"
        self.remote.transport.write(data)
        
# Incomming connections from the client to the proxy server.
class SSLServerProxyFactory(ServerFactory):
    protocol = SSLServerProxyProtocol
    
    def startFactory(self):
        self.nbConnections = 0        
    
class SSLClientProxyProtocol(Protocol):
    def __init__(self, parent):
        self.parent = parent
    
    def connectionMade(self):
        print "Connection to the client OK, parendID : %d" % (id(self.parent))
        
    def connectionLost(self, reason):
        pass
    
    def dataReceived(self, data):
        print "Data received from the remote server [Length=%d]" % (len(data))
        print "Forwarding the data to the client"
        print data

# Outgoing connections from the proxy to the remote server.
class SSLClientProxyFactory(ClientFactory):
    def __init__(self, parent):
        self.parent = parent
        
    def buildProtocol(self, addr):
        return SSLClientProxyProtocol(self.parent)

# Create the SSL Context, with server.pem as certificate, and TLS type auth
context = DefaultOpenSSLContextFactory(PRIVATE_KEY_FILENAME, CERTIFICATE_FILENAME, SSL.TLSv1_METHOD)

# Run the server and listen on port 443
reactor.listenSSL(LISTEN_PORT, SSLServerProxyFactory(), context)
reactor.run()