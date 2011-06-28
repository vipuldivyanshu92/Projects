using System;
using System.Diagnostics;
using System.Threading;

namespace SSLServer
{
    public class SslServer
    {
        static void Main(string[] args)
        {
            // Init the Trace
            Trace.Listeners.Add(new TextWriterTraceListener(Console.Out));
            Trace.AutoFlush = true;

            // Start the server
            var server = new SslListener(443, "localhost");
            var serverThread = new Thread(server.Start);
            serverThread.Start();

            Console.WriteLine("Listening on port 443");

            Console.ReadKey();

            Console.WriteLine("Stopping threads");
            serverThread.Abort();
            serverThread.Join();
        }
    }
}
