#include "PgSQLDatabase.h"
#include <boost/thread.hpp>
#include <boost/foreach.hpp>
#include <iostream>

PgSQLDatabase::PgSQLDatabase(std::size_t poolSize, const std::string& login,
        const std::string& host, const std::string& password,
        const std::string& database, uint32 port) :
Database(poolSize), m_login(login), m_host(host), m_password(password),
m_database(database), m_port(port)
{
    std::ostringstream os;
    os << "hostaddr = '" << m_host << "' port = '" << m_port << "' dbname = '";
    os << m_database << "' user = '" << m_login << "' password = '" << m_password;
    os << "' connect_timeout = '10'";
    
    m_connInfo = os.str();
}

void PgSQLDatabase::dbInitialize()
{
    for (uint32 i=0; i < m_poolConnSize; i++)
    {
        DatabaseConnection* dbc = new PgSQLDatabaseConnection(this,m_connInfo);
        m_dbConnQueue.push(dbc);
        m_dbConn.push_back(dbc);
        m_group.create_thread(boost::bind(&PgSQLDatabaseConnection::run, dbc));
    }
}

void PgSQLDatabase::start()
{
    m_runThread = new boost::thread(boost::bind(&PgSQLDatabase::run,this));
}

PgSQLDatabase::~PgSQLDatabase()
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
// PgSQLDatabaseConnection def
//////////////////////////////////////////////////////////////

PgSQLDatabase::PgSQLDatabaseConnection::PgSQLDatabaseConnection(
        Database* db, const std::string& connInfo) :
DatabaseConnection(db), m_connInfo(connInfo)
{

}

bool PgSQLDatabase::PgSQLDatabaseConnection::dbInitialize()
{

    m_pgsql = PQconnectdb(m_connInfo.c_str());
    if(!m_pgsql)
    {
        
        return false;
    }
    
    return connected();

}

bool PgSQLDatabase::PgSQLDatabaseConnection::connected()
{
    if(PQstatus(m_pgsql) != CONNECTION_OK)
    {
        std::cout << PQerrorMessage(m_pgsql);
        return false;
    }
    
    return true;
}

bool PgSQLDatabase::PgSQLDatabaseConnection::disconnect()
{
    PQfinish(m_pgsql);
    std::cout << "PgSQL conn closed" << std::endl;
    return true;
}

PgSQLDatabase::PgSQLDatabaseConnection::~PgSQLDatabaseConnection()
{

    disconnect();
}

void PgSQLDatabase::PgSQLDatabaseConnection::shutdown()
{
    m_shutdown=true;
    m_condition.notify_one();
}

