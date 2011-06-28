using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Net;
using System.Net.Sockets;
using System.Security.Cryptography.X509Certificates;
using System.Threading;

namespace SSLServer
{
    class SslListener
    {
        public int Port { get; private set; }

        public X509Certificate2 Certificate { get; set; }

        private List<Thread> handlers;

        public SslListener(int port, string certificateName)
        {
            Port = port;
            handlers = new List<Thread>();

            // Open the Local Machine certificate store
            var store = new X509Store(StoreLocation.LocalMachine);
            store.Open(OpenFlags.ReadOnly);
            var certificates = store.Certificates.Find(X509FindType.FindBySubjectName, certificateName, true);

            //
            if (certificates.Count == 0)
                throw new ArgumentException("Unable to find certificate :" + certificateName);

            Certificate = certificates[0];
        }

        public void Start()
        {
            // Create the listener
            var listener = new TcpListener(IPAddress.Any, Port);

            listener.Start();

            try
            {
                while (true)
                {
                    // Accept the Tcp connection from the clients
                    var client = listener.AcceptTcpClient();

                    Trace.TraceInformation("Connection from {0}", client.Client.RemoteEndPoint);

                    // The Handler should take care of the work from now
                    var handler = new SslHandler(client, Certificate);
                    var thread = new Thread(handler.Handle);
                    handlers.Add(thread);
                    thread.Start();
                }
            }
            catch (ThreadAbortException tae)
            {
                handlers.ForEach(x => x.Abort());
            }
        }
    }
}
