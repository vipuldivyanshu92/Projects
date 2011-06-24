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
