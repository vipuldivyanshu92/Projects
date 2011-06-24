import os
import sqlite3

DB_FILENAME = 'database.db3'

class DatabaseConnector:

    def __init__(self):
        self._con = None
        self._cur = None
        if not os.path.exists(DB_FILENAME):
            self._db_connect()
            self._create_tables()
        else:
            self._db_connect()

    def _db_connect(self):
        self._con = sqlite3.connect(DB_FILENAME)
        self._cur = self._con.cursor()

    def _create_tables(self):
        self._con.execute('CREATE TABLE messages(id INTEGER NOT NULL, message VARCHAR(100), PRIMARY KEY(id))')
        self._con.commit()

    def commit(self):
        self._con.commit()

    def cursor(self):
        return self._cur


db = DatabaseConnector()
