/*
Faolan Project, a free Age of Conan server emulator made for educational purpose
Copyright (C) 2008 Project Faolan team

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/

#include "SQLiteDatabase.h"
#include <boost/thread.hpp>
#include <boost/foreach.hpp>

SQLiteDatabase::SQLiteDatabase(std::size_t poolSize, const std::string& database) :
    Database(poolSize), m_database(database)
{

}

void SQLiteDatabase::dbInitialize()
{
    for (uint32 i=0; i < m_poolConnSize; i++)
    {
        DatabaseConnection* dbc = new SQLiteDatabaseConnection(this,m_database);
        m_dbConnQueue.push(dbc);
        m_dbConn.push_back(dbc);
        m_group.create_thread(boost::bind(&SQLiteDatabaseConnection::run, dbc));
    }
}

void SQLiteDatabase::start()
{
    m_runThread = new boost::thread(boost::bind(&SQLiteDatabase::run,this));
}

SQLiteDatabase::~SQLiteDatabase()
{
    BOOST_FOREACH(DatabaseConnection* dbc, m_dbConn)
    {
        if (dbc)
        {
            delete dbc;
        }
    }

    if (m_runThread)
    {
        delete m_runThread;
    }
}

/////////////////////////////////////////////////////////////:
// SQLiteDatabaseConnection def
//////////////////////////////////////////////////////////////

SQLiteDatabase::SQLiteDatabaseConnection::SQLiteDatabaseConnection(
        Database* db, const std::string& database) :
    DatabaseConnection(db), m_database(database)
{

}

bool SQLiteDatabase::SQLiteDatabaseConnection::dbInitialize()
{

    int res = sqlite3_open(m_database.c_str(), &m_sqlite);
    if(res)
    {
        return false;
    }
    
    return connected();

}

bool SQLiteDatabase::SQLiteDatabaseConnection::connected()
{
    return true; // only for inheritance purpose
}

bool SQLiteDatabase::SQLiteDatabaseConnection::disconnect()
{
    sqlite3_close(m_sqlite);
    std::cout << "SQLite conn closed" << std::endl;
    return true;
}

SQLiteDatabase::SQLiteDatabaseConnection::~SQLiteDatabaseConnection()
{

    disconnect();
}

void SQLiteDatabase::SQLiteDatabaseConnection::shutdown()
{
    m_shutdown=true;
    m_condition.notify_one();
}

