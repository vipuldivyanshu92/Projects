using System;
using System.IO;
using System.Net;
using System.Net.Security;
using System.Net.Sockets;
using System.Security.Authentication;
using System.Security.Cryptography.X509Certificates;
using System.Text;

namespace ConsoleApplication1
{
    class Program
    {
        static void Main(string[] args)
        {
            var store = new X509Store(StoreLocation.LocalMachine);
            store.Open(OpenFlags.ReadOnly);
            var certificates = store.Certificates.Find(X509FindType.FindBySubjectName, "localhost", true);

            Console.WriteLine("Number of valid certificate found: " + certificates.Count);

            if (certificates.Count == 0)
            {
                Console.WriteLine("Unable to retrieve a valid certificate, existing ...");
                return;
            }

            var cert = certificates[0];

            var listener = new TcpListener(IPAddress.Any, 443);

            listener.Start();

            while (true)
            {
                // Accept the Tcp connection from the client
                Console.WriteLine("Waiting for client to connect ...");

                var client = listener.AcceptTcpClient();

                Console.WriteLine("Accepted connection from : " + client.Client.LocalEndPoint);

                // Establish an SSL connection
                try
                {
                    using (var sslStream = new SslStream(client.GetStream()))
                    {

                        sslStream.AuthenticateAsServer(cert, false, SslProtocols.Default, true);
                        // Receive the request
                        var buffer = new byte[2048];
                        var read = sslStream.Read(buffer, 0, buffer.Length);
                        var decoder = Encoding.ASCII.GetDecoder();
                        var chars = new char[read];
                        decoder.GetChars(buffer, 0, read, chars, 0);

                        Console.WriteLine("Read : " + read);
                        Console.WriteLine(chars);

                        // Send the response
                        Console.WriteLine("Sending the response");
                        sslStream.Write(Encoding.ASCII.GetBytes("HTTP/1.1 200 OK\r\n"));
                        sslStream.Write(Encoding.ASCII.GetBytes("Content-Length: 5\r\n"));
                        sslStream.Write(Encoding.ASCII.GetBytes("Connection: close\r\n"));
                        sslStream.Write(Encoding.ASCII.GetBytes("\r\n"));
                        sslStream.Write(Encoding.ASCII.GetBytes("Hello"));
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Authentification failed : " + ex.Message);
                }
            }

            Console.ReadKey();
        }
    }
}
