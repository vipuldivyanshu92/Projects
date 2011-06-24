from common import framework
from dimension.game import onAuthenticate2, onPing, onUpdateGameServerStats
import asyncore
import MySQLdb

class TerritoryManagerServer(framework.server):
    def __init__(self):
        framework.server.__init__(self, 7040, 20, framework.GlobalHandler, True)

        self.db = MySQLdb.connection(
            host   = "127.0.0.1",
            user   = "root",
            passwd = "",
            db     = "aoc",
        )

        self.packetMgr = {
            "GameAgent" : {
                1 : onPing.onPing,
                3 : onAuthenticate2.onAuthenticate2,
                5 : onUpdateGameServerStats.onUpdateGameServerStats,
            },
            "GameCharAgent" : {
            }
        }
        
serv = TerritoryManagerServer()
asyncore.loop()