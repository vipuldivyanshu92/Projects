#include "Query.h"

Query::Query(boost::function<void ()> f, CallbackType type, QueryType t) :
    m_callback(f), m_callbackType(type), m_queryType(t), m_dbc(NULL),m_idx(0)
{

}

Query::Query(QueryType t) :
    m_callbackType(Query::NO_CALLBACK), m_queryType(t), m_dbc(NULL),m_idx(0)
{

}

Query::Query(CallbackType type, QueryType t) :
    m_callbackType(type), m_queryType(t), m_dbc(NULL),m_idx(0)
{

}

void Query::setDatabaseConnection(Database::DatabaseConnection* dbc)
{
    m_dbc=dbc;
}

void Query::setQueryText(const char* queryTxt, ...)
{
    va_list Params;
    va_start(Params, queryTxt);
    vsprintf(m_queryTxt, queryTxt, Params);
    va_end(Params);

}

void Query::releaseDBConnection()
{
    if (m_dbc)
    {
        Database* db = m_dbc->m_db;
        db->releaseDBConnection(m_dbc);
    }
}

void Query::setCallbackFunction(boost::function<void ()> f)
{
    m_callback=f;
}

void Query::setCallbackType(CallbackType type)
{
    m_callbackType=type;
}


