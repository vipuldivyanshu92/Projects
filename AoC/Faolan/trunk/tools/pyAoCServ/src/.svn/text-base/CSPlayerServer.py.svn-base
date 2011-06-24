from common import framework
from csplayer import onAuthenticate
import asyncore
import MySQLdb

class CSPlayerServer(framework.server):
    def __init__(self):
        framework.server.__init__(self, 7002, 20, framework.GlobalHandler, False)
    
        self.db = MySQLdb.connection(
            host   = "127.0.0.1",
            user   = "root",
            passwd = "",
            db     = "aoc",
        )
    
        self.packetMgr = {
            "CSPlayerAgent" : {
                0 : onAuthenticate.onAuthenticate,
            }
        }
        
serv = CSPlayerServer()
asyncore.loop()