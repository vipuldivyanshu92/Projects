#include "../MysqlDatabase.h"
#include "../MysqlQuery.h"
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
    MysqlDatabase* db = new MysqlDatabase(10,"albator","localhost","albator","aocemu",3306);
    
    db->start();

    MysqlQuery* q = new MysqlQuery(Query::WORKER_THREAD,Query::HAS_RESULT);
    q->setQueryText("SELECT * FROM auth");
    q->setCallbackFunction(boost::bind(&dummyFunction, q));

    MysqlQuery* q2 = new MysqlQuery(boost::bind(&dummyFunction, q2),Query::WORKER_THREAD,Query::HAS_RESULT);
    q2->setQueryText("SELECT * FROM auth");
    q2->setCallbackFunction(boost::bind(&dummyFunction, q2));

    MysqlQuery* q3 = new MysqlQuery(boost::bind(&secondDummyFunction, q3),Query::MAIN_THREAD,Query::HAS_RESULT);
    q3->setQueryText("SELECT * FROM auth");
    q3->setCallbackFunction(boost::bind(&dummyFunction, q3));
    MysqlQuery* q4 = new MysqlQuery(boost::bind(&secondDummyFunction, q4),Query::MAIN_THREAD,Query::HAS_RESULT);
    q4->setQueryText("SELECT * FROM auth");
    q4->setCallbackFunction(boost::bind(&dummyFunction, q4));
    MysqlQuery* q5 = new MysqlQuery(boost::bind(&secondDummyFunction, q5),Query::MAIN_THREAD,Query::HAS_RESULT);
    q5->setQueryText("SELECT * FROM auth");
    q5->setCallbackFunction(boost::bind(&dummyFunction, q5));
    MysqlQuery* q6 = new MysqlQuery(boost::bind(&dummyFunction, q6),Query::WORKER_THREAD,Query::HAS_RESULT);
    q6->setQueryText("SELECT * FROM auth");
    q6->setCallbackFunction(boost::bind(&dummyFunction, q6));
    MysqlQuery* q7 = new MysqlQuery(boost::bind(&dummyFunction, q7),Query::WORKER_THREAD,Query::HAS_RESULT);
    q7->setQueryText("SELECT * FROM auth");
    q7->setCallbackFunction(boost::bind(&dummyFunction, q7));
    MysqlQuery* q8 = new MysqlQuery(boost::bind(&dummyFunction, q8),Query::WORKER_THREAD,Query::HAS_RESULT);
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
