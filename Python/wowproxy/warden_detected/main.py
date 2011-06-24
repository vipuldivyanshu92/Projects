import sys
import asyncore
from realm_proxy import RealmServer
from world_proxy import WorldServer
from database import db
from sqlite3 import OperationalError

args = sys.argv[1:]
if len(args) == 0:
    rserver = RealmServer()
    wserver = WorldServer()
    asyncore.loop()
elif args[0] == '-sql':
    cursor = db.cursor()
    while True:
        sql = raw_input('> ')
        try:
            t = cursor.execute(sql).fetchall()
            db.commit()
            for r in t:
                print r
        except OperationalError as e:
            print('SQL ERROR : %s' % e)
