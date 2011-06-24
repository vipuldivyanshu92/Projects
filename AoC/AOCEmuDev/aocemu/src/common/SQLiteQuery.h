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
