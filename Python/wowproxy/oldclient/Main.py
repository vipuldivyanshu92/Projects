import AsyncRealm
import AsyncWorld
import asyncore

RealmSession = AsyncRealm.RealmHandler(
        '80.239.178.110',
        'ADRAEND',
        'N3YL9RL5',
    )

asyncore.loop()


WorldSession = AsyncWorld.WorldHandler(
        RealmSession.realms.get('Scarshield Legion', '')["address"],
        #"127.0.0.1:8085",
        'ADRAEND',
        RealmSession.SRP_SK,
        'ADRAEND'
    )

asyncore.loop()
