#!/usr/bin/env python

from config import metadata, realm
import map
import characters
import auth

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

auth_engine = create_engine('mysql+mysqldb://mangos:ZklndmYG3jTG@www.avalonserver.org/tc2_auth?charset=utf8&use_unicode=0', pool_recycle=3600)
#auth_engine.echo = True
characters_engine = create_engine('mysql+mysqldb://mangos:ZklndmYG3jTG@www.avalonserver.org/tc2_characters?charset=utf8&use_unicode=0', pool_recycle=3600)

Session = sessionmaker()
session = Session()

association = {
    'auth_engine': (auth.Realm, auth.Account, auth.AccountAccess,
                    auth.AccountBanned, auth.RealmCharacter, auth.Uptime),
    'characters_engine': (characters.Character, )
}

for o in association['auth_engine']:
    session.bind_mapper(o, auth_engine)
    
for o in association['characters_engine']:
    session.bind_mapper(o, characters_engine)

account = session.query(auth.Account).filter_by(username='EOWAMIR').one()
access = account.account_access.filter(auth.Realm.name == realm).one()

print(account.id)
print(access)