"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

class metaObj(object):
    def __init__(self):
        self.engine = None
        self.Session = scoped_session(sessionmaker())
        self.metadata = MetaData()

metas = {
    'realm'      : metaObj(),
    'characters' : metaObj()
}
