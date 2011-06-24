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
