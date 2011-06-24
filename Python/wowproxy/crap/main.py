from proxy import RealmServer
from SKserver import SKServer
import asyncore

SKserv = SKServer()
rserv = RealmServer(3724, '127.0.0.1', 37240)
wserv = RealmServer(8085, '127.0.0.1', 8086)

asyncore.loop()
