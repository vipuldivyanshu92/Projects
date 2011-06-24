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

#ifndef MYSQLDATABASE_H_
#define MYSQLDATABASE_H_

#include "Database.h"
#include "Common.h"
#include "Singleton.h"

#if PLATFORM == PLATFORM_WIN32
#	include <winsock2.h>
#endif
#include <mysql.h>

class MysqlDatabase : public Database {
public:
    
	static MysqlDatabase* createInstance(std::size_t poolSize, const std::string& login,
            const std::string& host, const std::string& password,
            const std::string& database, uint32 port);

	static MysqlDatabase* instance();

	static void destroy();
    
    bool start();
    

    
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

		std::string error();
private:

        bool dbInitialize();
        MYSQL m_mysql;

        std::string m_login, m_host, m_password, m_database;
        const uint32 m_port;
    };

private:

	MysqlDatabase(std::size_t poolSize, const std::string& login,
            const std::string& host, const std::string& password,
            const std::string& database, uint32 port);

	~MysqlDatabase();

    std::string m_login, m_host, m_password, m_database;
    const uint32 m_port;
    bool dbInitialize();

	static MysqlDatabase* m_db;

};

#endif /*MYSQLDATABASE_H_*/
