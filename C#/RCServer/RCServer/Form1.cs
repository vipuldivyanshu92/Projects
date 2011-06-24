using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Threading;
using System.Reflection;


namespace RCServer
{
    public partial class Form1 : Form
    {
        private Server server = new Server();
        Thread t;

        public Form1()
        {
            InitializeComponent();
        }

        private delegate void SetControlPropertyThreadSafeDelegate(Control control, string propertyName, object propertyValue);

        public static void SetControlPropertyThreadSafe(Control control, string propertyName, object propertyValue)
        {
            if (control.InvokeRequired)
            {
                control.Invoke(new SetControlPropertyThreadSafeDelegate(SetControlPropertyThreadSafe), new object[] { control, propertyName, propertyValue });
            }
            else
            {
                control.GetType().InvokeMember(propertyName, BindingFlags.SetProperty, null, control, new object[] { propertyValue });
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            server.pb = pictureBox1;
            t = new Thread(new ThreadStart(server.start));
            t.Start();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            t.Abort();
        }
    }
}
