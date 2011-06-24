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

#ifndef SQLiteQUERY_H_
#define SQLiteQUERY_H_

#include "Query.h"
#include "Common.h"
#include "SQLiteDatabase.h"
#include <map>
#include <string>

class SQLiteQuery : public Query {

public:
    /**
     * Query with a callback
     * 
     */
    SQLiteQuery(boost::function<void ()> f, CallbackType type, QueryType t);

    SQLiteQuery(CallbackType type, QueryType t);
    
    /**
     * Query without callback
     */
    SQLiteQuery(QueryType t);

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

    sqlite3_stmt *m_res;
    int m_cacheRc;
    bool m_row;
};

#endif /*SQLiteQUERY_H_*/
