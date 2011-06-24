#!/usr/bin/env python

from sqlalchemy import (Table, Column, Integer, String, Text, DateTime,
                        ForeignKey, Float, Time)

from config import metadata

class Character(object):
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return "<Character(%r)>" % (self.name)

characters_table = Table('characters', metadata,
    Column('guid', Integer, primary_key=True),
    Column('account', Integer, ForeignKey('account.id')),
    Column('name', String(12)),
    Column('race', Integer),
    Column('class', Integer),
    Column('gender', Integer),
    Column('level', Integer),
    Column('xp', Integer),
    Column('money', Integer),
    Column('position_x', Float),
    Column('position_y', Float),
    Column('position_z', Float),
    Column('map', Integer),
    Column('orientation', Float),
    Column('online', Integer),
    Column('totaltime', Integer),
    Column('leveltime', Integer),
    Column('logout_time', Integer),
    Column('is_logout_resting', Integer),
    Column('resettalents_cost', Integer),
    Column('resettalents_time', Integer),
    Column('extra_flags', Integer),
    Column('stable_slots', Integer),
    Column('at_login', Integer),
    Column('zone', Integer),
    Column('death_expire_time', Integer),
    Column('taxi_path', Text),
    Column('totalHonorPoints', Integer),
    Column('todayHonorPoints', Integer),
    Column('yesterdayHonorPoints', Integer),
    Column('totalKills', Integer),
    Column('todayKills', Integer),
    Column('yesterdayKills', Integer),
    Column('chosenTitle', Integer),
    Column('knownCurrencies', Integer),
    Column('watchedFaction', Integer),
    Column('drunk', Integer),
    Column('health', Integer),
    Column('power1', Integer),
    Column('power2', Integer),
    Column('power3', Integer),
    Column('power4', Integer),
    Column('power5', Integer),
    Column('power6', Integer),
    Column('power7', Integer),
    Column('latency', Integer),
    Column('speccount', Integer),
    Column('activespec', Integer),
    Column('exploredZones', Text),
    Column('equipmentCache', Text),
    Column('ammoId', Integer),
    Column('knownTitles', Text),
    Column('actionBars', Integer),
    Column('deleteInfos_Account', Integer),
    Column('deleteInfos_Name', String(12)),
    Column('deleteDate', Integer)
)
