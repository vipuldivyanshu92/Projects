using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.IO;
using System.Drawing;
using System.Windows.Forms;

namespace RCServer
{
    class Server
    {
        private bool running;
        public PictureBox pb;

        private Int64 min(Int64 x, Int64 y)
        {
            return x > y ? y : x;
        }

        public void start()
        {
            TcpListener listener = new TcpListener(IPAddress.Any, 13000);
            listener.Start();
            running = true;

            TcpClient client = listener.AcceptTcpClient();
            NetworkStream stream = client.GetStream();

            while (running)
            {
                byte[] aSize = new byte[8];
                stream.Read(aSize, 0, 8);
                Int64 imgSize = BitConverter.ToInt64(aSize, 0);

                byte[] aImg = new byte[imgSize];
                MemoryStream ms = new MemoryStream(aImg);

                int read = 0;
                while (read != imgSize)
                {
                    read += stream.Read(aImg, read, (int)min(4096, imgSize - read));
                }

                Image img = Image.FromStream(ms);
                Image dup = (Image)img.Clone();

                Form1.SetControlPropertyThreadSafe(pb, "Image", dup);

                ms.Close();
            }
            stream.Close();
            client.Close();
        }

        public void stop()
        {
            running = false;
        }
    }
}
