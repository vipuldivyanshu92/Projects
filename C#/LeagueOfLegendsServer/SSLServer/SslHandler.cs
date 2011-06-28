using System;
using System.Diagnostics;
using System.Net.Security;
using System.Net.Sockets;
using System.Security.Authentication;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading;

namespace SSLServer
{
    class SslHandler
    {
        private readonly TcpClient client;

        private readonly X509Certificate2 certificate;

        public SslHandler(TcpClient client, X509Certificate2 certificate)
        {
            this.client = client;
            this.certificate = certificate;
        }

        public void Handle()
        {
            // Establish an SSL connection
            try
            {
                using (var sslStream = new SslStream(client.GetStream()))
                {

                    sslStream.AuthenticateAsServer(certificate, false, SslProtocols.Default, true);

                    var buffer = new byte[2048];
                    var decoder = Encoding.ASCII.GetDecoder();
                    var chars = new char[buffer.Length];
                    while (true)
                    {
                        // Receive the request
                        var read = sslStream.Read(buffer, 0, buffer.Length);
                        decoder.GetChars(buffer, 0, read, chars, 0);
                        var str = new String(chars);

                        Trace.Write(str.Trim('\0'));

                        // Send the response
                        sslStream.Write(Encoding.ASCII.GetBytes("HTTP/1.1 200 OK\r\n"));
                        sslStream.Write(Encoding.ASCII.GetBytes("Content-Length: 5\r\n"));
                        sslStream.Write(Encoding.ASCII.GetBytes("Connection: close\r\n"));
                        sslStream.Write(Encoding.ASCII.GetBytes("\r\n"));
                        sslStream.Write(Encoding.ASCII.GetBytes("Hello"));
                    }
                }
            }
            catch(ThreadAbortException tae)
            {
                Trace.TraceInformation("Exiting Handler thread: " + Thread.CurrentThread);
            }
            catch (Exception ex)
            {
            }
        }
    }
}
