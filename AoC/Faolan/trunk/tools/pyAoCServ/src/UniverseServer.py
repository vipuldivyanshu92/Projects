from common import framework
from universe import onInitiateAuthentification, onAnswerChallenge
import asyncore
import MySQLdb

class UniverseServer(framework.server):
    def __init__(self):
        framework.server.__init__(self, 7000, 20, framework.GlobalHandler, False)
        
        self.db = MySQLdb.connection(
            host   = "127.0.0.1",
            user   = "root",
            passwd = "",
            db     = "aoc",
        )
    
        self.packetMgr = {
            "UniverseAgent" : {
                0 : onInitiateAuthentification.onInitiateAuthentification,
                1 : onAnswerChallenge.onAnswerChallenge,
            }
        }
        
serv = UniverseServer()
asyncore.loop()