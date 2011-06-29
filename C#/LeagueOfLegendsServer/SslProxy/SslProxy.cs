using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Security.Cryptography.X509Certificates;

namespace SslProxy
{
    using System.Linq;

    class SslListener
    {
        public int Port { get; set; }

        public X509Certificate2 Certificate { get; set; }

        private static void Usage()
        {
            Console.Write("Usage: ");
            Console.WriteLine(Path.GetFileNameWithoutExtension(Environment.GetCommandLineArgs()[0])
                + " <listening_address> <remote_address> <port> [<certificate_name>]");
        }

        private static bool ValidateArgs(string[] args)
        {
            if (args.Length < 3)
                return false;

            try
            {
                Dns.GetHostAddresses(args[0]);
                Dns.GetHostAddresses(args[1]);
                int.Parse(args[2]);
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }

        static void Main(string[] args)
        {
            if (!ValidateArgs(args))
            {
                Usage();
                return;
            }

            X509Certificate2Collection certificates = null;
            if (args.Length == 4)
            {
                // Open the Local Machine certificate store
                var store = new X509Store(StoreLocation.LocalMachine);
                store.Open(OpenFlags.ReadOnly);
                certificates = store.Certificates.Find(X509FindType.FindBySubjectName, args[3], true);

                // Check if any valid certificate has been found
                if (certificates.Count == 0) Console.WriteLine("Unable to load the certificate " + args[3]);
            }

            // Create the listener
            var listener = new TcpListener(Dns.GetHostAddresses(args[0]).First(), int.Parse(args[2]));
            listener.Start();

            // Informative message
            Console.Write("Listening on {0}:{2} and forwarding to {1}:{2}\n", args[0], args[1], args[2]);

            while (true)
            {
                // Accept the Tcp connection from the clients
                var client = listener.AcceptTcpClient();

                // The Handler should take care of the work from now
                int port = int.Parse(args[2]);
                var remote = new TcpClient(args[1], port);
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
