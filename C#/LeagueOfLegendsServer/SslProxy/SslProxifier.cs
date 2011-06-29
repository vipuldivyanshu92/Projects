using System;
using System.IO;
using System.Net.Security;
using System.Net.Sockets;
using System.Security.Authentication;
using System.Security.Cryptography.X509Certificates;
using System.Threading;

namespace SslProxy
{
    public class SslProxifier : RawProxifier
    {
        public X509Certificate Certificate { get; set; }

        // Dummy certification callback
        private static bool CertificateValidationCallback(object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors sslPolicyErrors)
        {
            return true;
        }

        // 
        public SslProxifier(Stream local, Stream remote, X509Certificate certificate)
        {
            LocalStream = new SslStream(local);
            RemoteStream = new SslStream(remote, false, CertificateValidationCallback);
            Certificate = certificate;
        }

        //
        public override bool Init()
        {
            try
            {
                // Create the local SSL authentication
                ((SslStream)LocalStream).AuthenticateAsServer(Certificate, false, SslProtocols.Default, true);

                // Create the remote SSL authentication
                ((SslStream)RemoteStream).AuthenticateAsClient("Remote");

                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }
    }
}