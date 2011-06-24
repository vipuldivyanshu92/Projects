#!/usr/bin/env python

from sqlalchemy import (create_engine, MetaData, Table, Column, Integer, String,
    Text, DateTime, ForeignKey, Float, Time)

from config import metadata

class Realm(object):
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return "<Realm(%r)>" % (self.name)

class AccountAccess(object):    
    def __init__(self, gmlevel, RealmID):
        self.gmlevel = gmlevel
        self.RealmID = RealmID
    
    def __repr__(self):
        return "<AccountAccess(%r, %r)>" % (self.gmlevel, self.RealmID)

class Account(object):    
    def __init__(self, username):
        self.username = username
        
    def __repr__(self):
        return "<Account(%r)>" % (self.username)

class AccountBanned(object):
    def __init__(self, id, bandate):
        self.id = id
        self.bandate = bandate
        
    def __repr__(self):
        return "<AccountBanned(%r, %r)>" % (self.id, self.bandate)

class RealmCharacter(object):
    def __init__(self, realmid, acctid):
        self.realmid = realmid
        self.acctid = acctid
        
    def __repr__(self):
        return "<RealmCharacter(%r, %r)>" % (self.realmid, self.acctid)

class Uptime(object):
    def __init__(self, realmid, starttime):
        self.realmid = realmid
        self.starttime = starttime
        
    def __repr__(self):
        return "<Uptime(%r, %r)>" % (self.realmid, self.starttime)

realmlist_table = Table('realmlist', metadata,    
    Column('id', Integer, primary_key=True),
    Column('name', String(32)),
    Column('address', String(32)),
    Column('port', Integer),
    Column('icon', Integer),
    Column('color', Integer),
    Column('timezone', Integer),
    Column('allowedSecurityLevel', Integer),
    Column('population', Float),
    Column('gamebuild', Integer)
)

account_access_table = Table('account_access', metadata,
    Column('id', Integer, ForeignKey('account.id'), primary_key=True),
    Column('gmlevel', Integer),
    Column('RealmID', Integer, ForeignKey('realmlist.id'), primary_key=True)
)

account_table = Table('account', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(32)),
    Column('sha_pass_hash', String(40)),
    Column('email', Text),
    Column('joindate', DateTime),
    Column('last_ip', String(30)),
    Column('failed_logins', Integer),
    Column('locked', Integer),
    Column('last_login', DateTime),
    Column('online', Integer),
    Column('expansion', Integer),
    Column('mutetime', Integer),
    Column('locale', Integer),
    Column('recruiter', Integer),
    Column('premium', Integer),
    Column('premium_die', DateTime),
)

account_banned_table = Table('account_banned', metadata,
    Column('id', Integer, ForeignKey('account.id'), primary_key=True),
    Column('bandate', DateTime, primary_key=True),
    Column('unbandate', DateTime),
    Column('bannedby', String(50)),
    Column('banreason', String(255)),
    Column('active', Integer)
)

realmcharacters_table = Table('realmcharacters', metadata,
    Column('realmid', ForeignKey('realmlist.id'), primary_key=True),
    Column('acctid', ForeignKey('account.id'), primary_key=True),
    Column('numchars', Integer)
)

uptime_table = Table('uptime', metadata,
    Column('realmid', Integer, ForeignKey('realmlist.id'), primary_key=True),
    Column('starttime', DateTime, primary_key=True),
    Column('startstring', String(64)),
    Column('uptime', Integer),
    Column('maxplayers', Integer),
    Column('revision', String(255))
)
