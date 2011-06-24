#ifndef PgSQLQUERY_H_
#define PgSQLQUERY_H_

#include "Query.h"
#include "Common.h"
#include "PgSQLDatabase.h"
#include <string>
#include <libpq-fe.h>

class PgSQLQuery : public Query {

public:
    /**
     * Query with a callback
     * 
     */
    PgSQLQuery(boost::function<void ()> f, CallbackType type, QueryType t);

    PgSQLQuery(CallbackType type, QueryType t);
    
    /**
     * Query without callback
     */
    PgSQLQuery(QueryType t);

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
    PGresult* m_res;
    uint32  m_row;
    int m_rowIdx;

};

#endif /*PgSQLQUERY_H_*/
