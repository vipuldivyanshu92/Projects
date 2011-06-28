using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Security;
using System.Net.Sockets;
using System.Security.Cryptography.X509Certificates;
using System.Text;

namespace SslClient
{
    class Program
    {
        static bool CertificateValidationCallback(object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors sslPolicyErrors)
        {
            return true;
        }

        static void Main(string[] args)
        {
            TcpClient client = new TcpClient("64.7.194.113", 443); 

            SslStream sslStream = new SslStream(client.GetStream(), false, CertificateValidationCallback);

            sslStream.AuthenticateAsClient("remote");
        }
    }
}
