#ifndef SQLiteDATABASE_H_
#define SQLiteDATABASE_H_

#include "Database.h"
#include <sqlite3.h>

class SQLiteDatabase : public Database {
public:
    SQLiteDatabase(std::size_t poolSize, const std::string& database);

    void start();

    ~SQLiteDatabase();

    class SQLiteDatabaseConnection : public Database::DatabaseConnection {
public:
        friend class SQLiteQuery;
        SQLiteDatabaseConnection(Database* db, const std::string& database);

        bool connected();

        bool disconnect();

        void shutdown();

        ~SQLiteDatabaseConnection();
private:

        bool dbInitialize();
        sqlite3* m_sqlite;
        std::string m_database;
        
    };

private:

    std::string m_database;
    void dbInitialize();

};

#endif /*SQLiteDATABASE_H_*/
