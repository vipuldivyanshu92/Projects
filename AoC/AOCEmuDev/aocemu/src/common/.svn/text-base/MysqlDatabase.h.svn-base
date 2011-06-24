#ifndef MYSQLDATABASE_H_
#define MYSQLDATABASE_H_

#include "Database.h"
#include <mysql.h>

class MysqlDatabase : public Database {
public:
    MysqlDatabase(std::size_t poolSize, const std::string& login,
            const std::string& host, const std::string& password,
            const std::string& database, uint32 port);

    
    void start();
    
    ~MysqlDatabase();
    
    class MysqlDatabaseConnection : public Database::DatabaseConnection {
public:
        friend class MysqlQuery;
        MysqlDatabaseConnection(Database* db, const std::string& login,
                const std::string& host, const std::string& password,
                const std::string& database, uint32 port);

        bool connected();

        bool disconnect();
        
        void shutdown();

        ~MysqlDatabaseConnection();
private:

        bool dbInitialize();
        MYSQL m_mysql;

        std::string m_login, m_host, m_password, m_database;
        const uint32 m_port;
    };

private:

    std::string m_login, m_host, m_password, m_database;
    const uint32 m_port;
    void dbInitialize();

};

#endif /*MYSQLDATABASE_H_*/
