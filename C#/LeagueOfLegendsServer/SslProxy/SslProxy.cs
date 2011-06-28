using System;
using System.IO;
using System.Net;
using System.Net.Security;
using System.Net.Sockets;
using System.Security.Authentication;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading;

namespace SslProxy
{
    class SslListener
    {
        public int Port { get; private set; }

        public X509Certificate2 Certificate { get; set; }

        public SslListener(int port, string certificateName)
        {
            Port = port;

            // Open the Local Machine certificate store
            var store = new X509Store(StoreLocation.LocalMachine);
            store.Open(OpenFlags.ReadOnly);
            var certificates = store.Certificates.Find(X509FindType.FindBySubjectName, certificateName, true);

            //
            if (certificates.Count == 0)
                throw new ArgumentException("Unable to find certificate :" + certificateName);

            Certificate = certificates[0];
        }

        public class Proxify
        {
            private readonly SslStream localSsl;
            private readonly SslStream remoteSsl;
            private readonly X509Certificate certificate;

            static bool CertificateValidationCallback(object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors sslPolicyErrors)
            {
                return true;
            }

            public Proxify(TcpClient local, string remoteAddress, X509Certificate certificate)
            {
                this.certificate = certificate;

                var remote = new TcpClient(remoteAddress, 443);

                localSsl = new SslStream(local.GetStream());
                remoteSsl = new SslStream(remote.GetStream(), false, CertificateValidationCallback);
            }

            public void Execute()
            {
                // Do both sides authentication

                if (Authenticate())
                {
                    var localToRemote = new ProxyPipe(localSsl, remoteSsl, true);
                    var localToRemoteThread = new Thread(localToRemote.Transfer);
                    localToRemoteThread.Start();

                    var remoteToLocal = new ProxyPipe(remoteSsl, localSsl, true);
                    var remoteToLocalThread = new Thread(remoteToLocal.Transfer);
                    remoteToLocalThread.Start();
                }
            }

            private class ProxyPipe
            {
                private readonly Stream src;
                private readonly Stream dst;
                private readonly bool verbose;

                public ProxyPipe(Stream src, Stream dst, bool verbose)
                {
                    this.src = src;
                    this.dst = dst;
                    this.verbose = verbose;
                }

                public void Transfer()
                {
                    var buffer = new byte[2048];

                    try
                    {
                        int len;
                        while ((len = src.Read(buffer, 0, buffer.Length)) > 0)
                        {
                            if (verbose)
                            {
                                var content = Encoding.ASCII.GetString(buffer, 0, len);
                                Console.WriteLine(content);
                            }
                            dst.Write(buffer, 0, len);
                        }
                    } 
                    catch (Exception ex)
                    {
                        Console.WriteLine(ex.Message);
                    }
                }
            }

            private bool Authenticate()
            {
                try
                {
                    // Create the local SSL authentication
                    localSsl.AuthenticateAsServer(certificate, false, SslProtocols.Default, true);

                    // Create the remote SSL authentication
                    remoteSsl.AuthenticateAsClient("Remote");

                    return true;
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                    return false;
                }
            }
        }

        static void Main(string[] args)
        {
            // Open the Local Machine certificate store
            var store = new X509Store(StoreLocation.LocalMachine);
            store.Open(OpenFlags.ReadOnly);
            var certificates = store.Certificates.Find(X509FindType.FindBySubjectName, "localhost", true);

            //
            if (certificates.Count == 0)
                throw new ArgumentException("Unable to find certificate");

            // Create the listener
            var listener = new TcpListener(IPAddress.Any, 443);
            listener.Start();

            while (true)
            {
                // Accept the Tcp connection from the clients
                var client = listener.AcceptTcpClient();

                // The Handler should take care of the work from now
                var proxy = new Proxify(client, "64.7.194.113", certificates[0]);
                proxy.Execute();
            }
            
        }
    }
}
