#!/usr/bin/env python

from sqlalchemy.orm import mapper, sessionmaker, relationship, backref

import auth
import characters

# Define the class/table mapping
mapper(auth.Realm, auth.realmlist_table, properties={
    'realm_characters': relationship(auth.RealmCharacter, backref='account'),
    'uptimes': relationship(auth.Uptime, backref='realm')
})
mapper(auth.AccountAccess, auth.account_access_table, properties={
    'realm': relationship(auth.Realm)
})
mapper(auth.Account, auth.account_table, properties={
    'account_access': relationship(auth.AccountAccess, backref='account', lazy='dynamic'),
    'account_banned': relationship(auth.AccountBanned, backref='account'),
    'characters': relationship(characters.Character)
})
mapper(auth.AccountBanned, auth.account_banned_table)
mapper(auth.RealmCharacter, auth.realmcharacters_table)
mapper(auth.Uptime, auth.uptime_table)
mapper(characters.Character, characters.characters_table)
