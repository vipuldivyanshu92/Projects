"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from avalon.model.meta import metas, metaObj

from sqlalchemy import schema, types
from sqlalchemy.databases.mysql import MSBigInteger

def init_model(engine, name):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #

    metas[name] = metaObj()
    metas[name].Session.configure(bind=engine)
    metas[name].engine = engine

ip_banned_table = schema.Table('ip_banned', metas['realm'].metadata,
    schema.Column('ip', types.VARCHAR(), primary_key=True),
    schema.Column('bandate', MSBigInteger(), primary_key=True),
    schema.Column('unbandate', MSBigInteger()),
    schema.Column('bannedby', types.VARCHAR()),
    schema.Column('banreason', types.VARCHAR())
)

class IpBanned(object):
    pass

orm.mapper(IpBanned, ip_banned_table)
