using System;
using System.Management;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace DnsPoisoning
{
    public class UdpListener
    {
        private Socket socket;
        private int port;

        public UdpListener(int port)
        {
            this.port = port;
            socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        }

        public void Execute()
        {
            socket.Bind(new IPEndPoint(IPAddress.Any, port));
            var buffer = new byte[2048];

            while (true)
            {
                socket.Receive(buffer);

                Console.WriteLine("Received something");
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            var mc = new ManagementClass("Win32_NetworkAdapterConfiguration");
            var moc = mc.GetInstances();

            // Start the local DNS Server
            var listener = new UdpListener(54);
            var listeningThread = new Thread(listener.Execute);
            listeningThread.Start();

            // Modify the local config to use local DNS server
            foreach (ManagementObject mo in moc)
            {
                if ((bool)mo["ipEnabled"])
                {
                    Console.WriteLine(mo["Caption"]);

                    ManagementBaseObject newDNS = mo.GetMethodParameters("SetDNSServerSearchOrder");

                    newDNS["DNSServerSearchOrder"] = new[] { "127.0.0.1:54" };
                    mo.InvokeMethod("SetDNSServerSearchOrder", newDNS, null);
                }
            }

            // try to do a DNS resolve
            string str;
            while ((str = Console.ReadLine()) != String.Empty)
            {
                var addresses = Dns.GetHostAddresses(str);

                foreach (var ipAddress in addresses)
                {
                    Console.WriteLine(ipAddress);
                }
            }
            
            listeningThread.Abort();
        }
    }
}
