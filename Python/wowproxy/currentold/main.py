import asyncore
from realmproxy import RealmServer

r = RealmServer(3724, '127.0.0.1', 37240)
asyncore.loop()
