using System;
using System.Linq;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;

namespace MobileRC_POC
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        [DllImport("coredll.dll")]
        public static extern int BitBlt(IntPtr hdcDest, int nXDest, int nYDest, int nWidth, int nHeight, IntPtr hdcSrc, int nXSrc, int nYSrc, uint dwRop);

        [DllImport("coredll.dll", SetLastError = true)]
        public extern static IntPtr GetDC(IntPtr hwnd);

        const int SW_MINIMIZED = 6;
        const int SRCCOPY = 0x00CC0020;

        private TcpClient client;
        private NetworkStream stream;
        private int status = 0;

        private Bitmap Snapshot(Rectangle rect)
        {
            Bitmap bmp = new Bitmap(rect.Width, rect.Height);
            Graphics gxComp = Graphics.FromImage(bmp);
            // Blit the image data
            int ret = BitBlt(gxComp.GetHdc(), 0, 0, rect.Width, rect.Height, GetDC(IntPtr.Zero), 0, 0, SRCCOPY);
            return bmp;
        }

        private void menuItem1_Click(object sender, EventArgs e)
        {
            if (status == 0)
            {
                client = new TcpClient(textBox1.Text, 13000);
                stream = client.GetStream();
                status = 1;
                menuItem1.Text = "Disconnect";
            }
            else
            {
                client.Close();
                status = 0;
                menuItem1.Text = "Connect";
                stream.Close();
            }
        }

        private void menuItem2_Click(object sender, EventArgs e)
        {
            
            Rectangle bounds = Screen.PrimaryScreen.Bounds;
            Bitmap bmp = Snapshot(bounds);
            MemoryStream ms = new MemoryStream();
            bmp.Save(ms, System.Drawing.Imaging.ImageFormat.Jpeg);
            stream.Write(BitConverter.GetBytes(ms.Length), 0, 8);
            ms.WriteTo(stream);
            listBox1.Items.Add("done");
            ms.Close();
            
            bmp.Dispose();
        }
    }
}