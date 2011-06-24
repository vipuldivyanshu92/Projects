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
