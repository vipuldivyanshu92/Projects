#ifndef PgSQLDATABASE_H_
#define PgSQLDATABASE_H_

#include "Database.h"
#include <libpq-fe.h>

class PgSQLDatabase : public Database {
public:
    PgSQLDatabase(std::size_t poolSize, const std::string& login,
            const std::string& host, const std::string& password,
            const std::string& database, uint32 port);

    void start();

    ~PgSQLDatabase();

    class PgSQLDatabaseConnection : public Database::DatabaseConnection {
public:
        friend class PgSQLQuery;
        PgSQLDatabaseConnection(Database* db, const std::string& connInfo);

        bool connected();

        bool disconnect();

        void shutdown();

        ~PgSQLDatabaseConnection();
private:

        bool dbInitialize();
        std::string m_connInfo;
        PGconn* m_pgsql;

    };

private:

    std::string m_login, m_host, m_password, m_database;
    const uint32 m_port;
    std::string m_connInfo;

    void dbInitialize();

};

#endif /*PgSQLDATABASE_H_*/
