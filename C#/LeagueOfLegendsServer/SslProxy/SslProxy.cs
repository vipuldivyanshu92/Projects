using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Security.Cryptography.X509Certificates;

namespace SslProxy
{
    using System.Diagnostics;
    using System.Linq;

    class SslListener
    {
        public int Port { get; set; }

        public X509Certificate2 Certificate { get; set; }

        private static void Usage()
        {
            Console.Write("Usage: ");
            Console.WriteLine(Path.GetFileNameWithoutExtension(Environment.GetCommandLineArgs()[0])
                + " <listening_address> <listening_port> <remote_address> <port> [<certificate_name>]");
        }

        private static bool ValidateArgs(string[] args)
        {
            if (args.Length < 4)
                return false;

            try
            {
                Dns.GetHostAddresses(args[0]);
                int.Parse(args[1]);
                Dns.GetHostAddresses(args[2]);
                int.Parse(args[3]);
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }

        static void Main(string[] args)
        {
            // Create the Trace Listeners
            var fileName = string.Format("log-{0}.txt", DateTime.Now.ToString("yy-MM-dd-h-mm-ss"));
            FileStream log = new FileStream(fileName, FileMode.OpenOrCreate);
            Trace.Listeners.Add(new TextWriterTraceListener(log));
            Trace.AutoFlush = true;

            // Validate the arguments)
            if (!ValidateArgs(args))
            {
                Usage();
                return;
            }

            X509Certificate2Collection certificates = null;
            if (args.Length == 5)
            {
                // Open the Local Machine certificate store
                var store = new X509Store(StoreLocation.LocalMachine);
                store.Open(OpenFlags.ReadOnly);
                certificates = store.Certificates.Find(X509FindType.FindBySubjectName, args[4], true);

                // Check if any valid certificate has been found
                if (certificates.Count == 0) Console.WriteLine("Unable to load the certificate " + args[4]);
            }

            // Create the listener
            var listener = new TcpListener(Dns.GetHostAddresses(args[0]).First(), int.Parse(args[1]));
            listener.Start();

            // Informative message
            Console.Write("Listening on {0}:{1} and forwarding to {2}:{3}\n", args[0], args[1], args[2], args[3]);

            while (true)
            {
                // Accept the Tcp connection from the clients
                var client = listener.AcceptTcpClient();

                // The Handler should take care of the work from now
                int remotePort = int.Parse(args[3]);
                var remote = new TcpClient(args[2], remotePort);
                RawProxifier proxy;

                if (certificates == null) 
                    proxy = new RawProxifier(client.GetStream(), remote.GetStream());
                else
                    proxy = new SslProxifier(client.GetStream(), remote.GetStream(), certificates[0]);

                proxy.Execute();
            }
        }
    }
}
