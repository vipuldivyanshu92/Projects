#include "MysqlDatabase.h"
#include <boost/thread.hpp>
#include <boost/foreach.hpp>

MysqlDatabase::MysqlDatabase(std::size_t poolSize, const std::string& login,
        const std::string& host, const std::string& password,
        const std::string& database, uint32 port) :
    Database(poolSize), m_login(login), m_host(host), m_password(password),
            m_database(database), m_port(port)
{

}

void MysqlDatabase::dbInitialize()
{
    for (uint32 i=0; i < m_poolConnSize; i++)
    {
        DatabaseConnection* dbc = new MysqlDatabaseConnection(this,m_login,m_host,m_password,m_database,m_port);
        m_dbConnQueue.push(dbc);
        m_dbConn.push_back(dbc);
        m_group.create_thread(boost::bind(&MysqlDatabaseConnection::run, dbc));
    }
}

void MysqlDatabase::start()
{
    m_runThread = new boost::thread(boost::bind(&MysqlDatabase::run,this));
}

MysqlDatabase::~MysqlDatabase()
{
    BOOST_FOREACH(DatabaseConnection* dbc, m_dbConn)
    {
        if(dbc)
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
// MysqlDatabaseConnection def
//////////////////////////////////////////////////////////////

MysqlDatabase::MysqlDatabaseConnection::MysqlDatabaseConnection(Database* db,
        const std::string& login, const std::string& host,
        const std::string& password, const std::string& database, uint32 port) :
    DatabaseConnection(db), m_login(login), m_host(host), m_password(password),
            m_database(database), m_port(port)
{

}

bool MysqlDatabase::MysqlDatabaseConnection::dbInitialize()
{

    mysql_init(&m_mysql);
    //mysql_option(&m_mysql, MYSQL_SET_CHARSET_NAME, "utf8");

    if (!mysql_real_connect(&m_mysql, m_host.c_str(), m_login.c_str(),
            m_password.c_str(), m_database.c_str(), m_port, NULL, 0))
    {

        return false;
    }

    return connected();

}

bool MysqlDatabase::MysqlDatabaseConnection::connected()
{
    return mysql_ping(&m_mysql) ? false : true;
}

bool MysqlDatabase::MysqlDatabaseConnection::disconnect()
{
    mysql_close(&m_mysql);
    std::cout << "mysql conn closed" << std::endl;
    return true;
}

MysqlDatabase::MysqlDatabaseConnection::~MysqlDatabaseConnection()
{

    disconnect();
}

void MysqlDatabase::MysqlDatabaseConnection::shutdown()
{
    m_shutdown=true;
    m_condition.notify_one();
}

