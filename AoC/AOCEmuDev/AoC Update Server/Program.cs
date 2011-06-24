using System;
using System.Collections.Generic;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.IO;

namespace AoC_Update_Server
{
    class Program
    {
        private static WebServer m_Server;

        static void Main(string[] args)
        {
            m_Server = new WebServer(80, Environment.CurrentDirectory + "\\Root");
            m_Server.Start();
        }
    }
}
