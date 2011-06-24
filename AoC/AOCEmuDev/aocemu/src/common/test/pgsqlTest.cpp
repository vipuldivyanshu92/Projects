#include "../PgSQLDatabase.h"
#include "../PgSQLQuery.h"
#include <boost/thread.hpp>
#include <iostream>

void dummyFunction(Query* q)
{
    std::cout << "worker thread callback" << std::endl;
    
    while(q->fetchRow())
    {
        std::cout << q->getUint32() << ":";
        std::cout << q->getString() << ":";
        std::cout << q->getString() << std::endl;
    }
    


}

void secondDummyFunction(Query* q)
{
    std::cout << "main thread callback" << std::endl;
}

int main()
{
    PgSQLDatabase* db = new PgSQLDatabase(10,"albator","127.0.0.1","albator","aocemu",5432);
    
    db->start();

    PgSQLQuery* q = new PgSQLQuery(Query::WORKER_THREAD,Query::HAS_RESULT);
    q->setQueryText("SELECT * FROM auth");
    q->setCallbackFunction(boost::bind(&dummyFunction, q));

    PgSQLQuery* q2 = new PgSQLQuery(boost::bind(&dummyFunction, q2),Query::WORKER_THREAD,Query::HAS_RESULT);
    q2->setQueryText("SELECT * FROM auth");
    q2->setCallbackFunction(boost::bind(&dummyFunction, q2));

    PgSQLQuery* q3 = new PgSQLQuery(boost::bind(&secondDummyFunction, q3),Query::MAIN_THREAD,Query::HAS_RESULT);
    q3->setQueryText("SELECT * FROM auth");
    q3->setCallbackFunction(boost::bind(&dummyFunction, q3));
    PgSQLQuery* q4 = new PgSQLQuery(boost::bind(&secondDummyFunction, q4),Query::MAIN_THREAD,Query::HAS_RESULT);
    q4->setQueryText("SELECT * FROM auth");
    q4->setCallbackFunction(boost::bind(&dummyFunction, q4));
    PgSQLQuery* q5 = new PgSQLQuery(boost::bind(&secondDummyFunction, q5),Query::MAIN_THREAD,Query::HAS_RESULT);
    q5->setQueryText("SELECT * FROM auth");
    q5->setCallbackFunction(boost::bind(&dummyFunction, q5));
    PgSQLQuery* q6 = new PgSQLQuery(boost::bind(&dummyFunction, q6),Query::WORKER_THREAD,Query::HAS_RESULT);
    q6->setQueryText("SELECT * FROM auth");
    q6->setCallbackFunction(boost::bind(&dummyFunction, q6));
    PgSQLQuery* q7 = new PgSQLQuery(boost::bind(&dummyFunction, q7),Query::WORKER_THREAD,Query::HAS_RESULT);
    q7->setQueryText("SELECT * FROM auth");
    q7->setCallbackFunction(boost::bind(&dummyFunction, q7));
    PgSQLQuery* q8 = new PgSQLQuery(boost::bind(&dummyFunction, q8),Query::WORKER_THREAD,Query::HAS_RESULT);
    q8->setQueryText("SELECT * FROM auth");
    q8->setCallbackFunction(boost::bind(&dummyFunction, q8));

    db->enqueueQuery(q);
    db->enqueueQuery(q2);
    db->enqueueQuery(q3);
    db->enqueueQuery(q4);
    db->enqueueQuery(q5);
    db->enqueueQuery(q6);
    db->enqueueQuery(q7);
    db->enqueueQuery(q8);
    
    std::cout << "available connection : " << db->availableDBConnection() << std::endl;
    db->runFinishedQueryCallback();
    boost::xtime sleepA;
    boost::xtime_get(&sleepA, boost::TIME_UTC);
    sleepA.sec += 1;
    
    boost::thread::sleep(sleepA);
    
    
    db->runFinishedQueryCallback();
    std::cout << "available connection : " << db->availableDBConnection() << std::endl;
    
    db->shutdown();
    delete db;
    
    return 0;
}
