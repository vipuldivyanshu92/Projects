using System;
using System.Text;
using System.Net;
using System.Net.Sockets;

namespace RemoteServer
{
    class Program
    {
        static void Main(string[] args)
        {
            UdpClient client = new UdpClient();

            byte[] dgram = ASCIIEncoding.ASCII.GetBytes(System.Environment.MachineName);
            client.Send(dgram, dgram.Length, new IPEndPoint(IPAddress.Broadcast, 28960));
        }
    }
}
