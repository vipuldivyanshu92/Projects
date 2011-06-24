using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Sockets;
using System.Collections;
using System.Threading;

namespace AoC_Update_Server
{
    public abstract class CSHTTPServer
    {
        private int portNum = 8080;
        private TcpListener listener;
        System.Threading.Thread Thread;

        public Hashtable respStatus;

        public string Name = "AoCUpdateServer/1.0.*";

        public bool IsAlive
        {
            get
            {
                return this.Thread.IsAlive;
            }
        }

        public CSHTTPServer()
        {
            //
            respStatusInit();
        }

        public CSHTTPServer(int thePort)
        {
            portNum = thePort;
            respStatusInit();
        }

        private void respStatusInit()
        {
            respStatus = new Hashtable();

            respStatus.Add(200, "200 Ok");
            respStatus.Add(201, "201 Created");
            respStatus.Add(202, "202 Accepted");
            respStatus.Add(204, "204 No Content");

            respStatus.Add(301, "301 Moved Permanently");
            respStatus.Add(302, "302 Redirection");
            respStatus.Add(304, "304 Not Modified");

            respStatus.Add(400, "400 Bad Request");
            respStatus.Add(401, "401 Unauthorized");
            respStatus.Add(403, "403 Forbidden");
            respStatus.Add(404, "404 Not Found");

            respStatus.Add(500, "500 Internal Server Error");
            respStatus.Add(501, "501 Not Implemented");
            respStatus.Add(502, "502 Bad Gateway");
            respStatus.Add(503, "503 Service Unavailable");
        }

        private void Listen()
        {
            bool done = false;

            listener = new TcpListener(portNum);

            listener.Start();

            WriteLog("Listening On: " + portNum.ToString());

            while (!done)
            {
                WriteLog("Waiting for connection...");
                CsHTTPRequest newRequest = new CsHTTPRequest(listener.AcceptTcpClient(), this);
                Thread Thread = new Thread(new ThreadStart(newRequest.Process));
                Thread.Name = "HTTP Request";
                Thread.Start();
            }

        }

        public void WriteLog(string EventMessage)
        {
            Console.WriteLine(EventMessage);
        }

        public void Start()
        {
            // CSHTTPServer HTTPServer = new CSHTTPServer(portNum);
            this.Thread = new Thread(new ThreadStart(this.Listen));
            this.Thread.Start();
        }

        public void Stop()
        {
            listener.Stop();
            this.Thread.Abort();
        }

        public void Suspend()
        {
            this.Thread.Suspend();
        }

        public void Resume()
        {
            this.Thread.Resume();
        }

        public abstract void OnResponse(ref HTTPRequestStruct rq, ref HTTPResponseStruct rp);
    }
}
