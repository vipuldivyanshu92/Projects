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

#ifndef MYSQLQUERY_H_
#define MYSQLQUERY_H_

#include "Query.h"
#include "Common.h"
#include "MysqlDatabase.h"
#include <map>
#include <string>

class MysqlQuery : public Query {

public:
    /**
     * Query with a callback
     * 
     */
    MysqlQuery(boost::function<void ()> f, CallbackType type, QueryType t);

    MysqlQuery(CallbackType type, QueryType t);
    
    /**
     * Query without callback
     */
    MysqlQuery(QueryType t);

    bool execute();

    bool fetchRow();

    bool storeResult();
    
    std::string error();

    
    uint32 getUint32();
    uint64 getUint64();
    const char* getString();
    
    uint32 getUint32(uint32 idx);
    uint64 getUint64(uint32 idx);
    const char* getString(uint32 idx);

private:
    MYSQL_RES* m_res;
    MYSQL_ROW m_row;

};

#endif /*MYSQLQUERY_H_*/
