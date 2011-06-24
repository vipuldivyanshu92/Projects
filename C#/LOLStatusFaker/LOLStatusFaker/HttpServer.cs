using System;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

namespace LOLStatusFaker
{
    public class HttpHandler
    {
        private readonly TcpClient client;

        public HttpHandler(TcpClient client)
        {
            this.client = client;
        }

        public void ServiceClient()
        {
            try
            {
                const string response = @"refreshContent({""status"":false,""serverStatus"":1,""news"":[{""title"":""League Judgement: Yorick, the Gravedigger"",""url"":""http:\\/\\/eu.leagueoflegends.com\\/node\\/4015"",""date"":""06.22.2011""},{""title"":""Skin Sale: 50% Off Bird of Prey Anivia, Cowgirl Miss Fortune, and Dragon Slayer Jarvan"",""url"":""http:\\/\\/eu.leagueoflegends.com\\/node\\/3999"",""date"":""06.22.2011""},{""title"":""New Yorick Skins and Bundles in the Upcoming Patch"",""url"":""http:\\/\\/eu.leagueoflegends.com\\/node\\/3989"",""date"":""06.22.2011""},{""title"":""Champion Sale: 50% Off Pantheon, Kennen, and Anivia "",""url"":""http:\\/\\/eu.leagueoflegends.com\\/node\\/3984"",""date"":""06.22.2011""},{""title"":""League of Legends Season One Champions Have Been Crowned!"",""url"":""http:\\/\\/eu.leagueoflegends.com\\/node\\/3954"",""date"":""06.22.2011""}],""community"":[{""title"":""Yorick, the Gravedigger"",""url"":""http:\\/\\/eu.leagueoflegends.com\\/news\\/new-yorick-skins-and-bundles-upcoming-patch""},{""title"":""Visit the Season One Championship page!"",""url"":""http:\\/\\/s1.leagueoflegends.com""},{""title"":""Summoner Name Change"",""url"":""http:\\/\\/eu.leagueoflegends.com\\/news\\/summoner-name-changes-available-tomorrow""},{""title"":""Multiple Mastery Pages"",""url"":""http:\\/\\/eu.leagueoflegends.com\\/news\\/multiple-mastery-pages-are-way""},{""title"":""The Tribunal"",""url"":""http:\\/\\/eu.leagueoflegends.com\\/news\\/tribunal-now-limited-release""}]});";

                while (client.Connected)
                {
                    var asciiReader = new StreamReader(client.GetStream(), Encoding.ASCII);
                    var asciiWriter = new StreamWriter(client.GetStream(), Encoding.ASCII);
                    var utf8Writer = new StreamWriter(client.GetStream(), Encoding.UTF8);

                    // Read the HTTP header
                    while (asciiReader.ReadLine() != string.Empty)
                    {
                    }

                    // Write the response
                    asciiWriter.WriteLine("HTTP/1.1 200 OK");
                    asciiWriter.WriteLine("Content-Length: 1340");
                    asciiWriter.WriteLine("Connection: close");
                    asciiWriter.WriteLine("Content-Type: text/javascript; charset=UTF-8");
                    asciiWriter.WriteLine();
                    asciiWriter.Flush();

                    asciiWriter.WriteLine();
                    utf8Writer.Write(response);
                    utf8Writer.Flush();
                }
            }
            catch (Exception ex)
            {
                Trace.WriteLine(ex.Message);
            }
        }
    }

    public class HttpListener
    {
        public int Port { get; private set; }

        public bool Running { get; set; }

        public HttpListener(int port)
        {
            Port = port;
        }

        public void Run()
        {
            var listener = new TcpListener(IPAddress.Any, Port);

            Running = true;

            listener.Start();

            while (Running)
            {
                var tcpClient = listener.AcceptTcpClient();

                var handler = new HttpHandler(tcpClient);
                new Thread(handler.ServiceClient).Start();
            }
        }
    }
}
