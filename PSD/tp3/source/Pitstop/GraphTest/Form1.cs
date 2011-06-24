using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace GraphTest
{
    public partial class Form1 : Form
    {       
        private IGraph gra1, gra2, gra3, gra4;
        private IGraphDriver graph1 = new userGraphDriver();
        private IGraphDriver graph2 = new userGraphDriver();
        private IGraphDriver graph3 = new userGraphDriver();
        private IGraphDriver graph4 = new userGraphDriver();
     
        public int curSpeed = 0, curSpeed1 = 0, curSpeed2 = 0;
        public Form1()
        {
            InitializeComponent();
            
        }
        public void drawAxis()
        {
          
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            
        }

        private void button1_Click(object sender, EventArgs e)
        {
            
            if (gra1 == null)
            {
                gra1 = new CHistGraph(groupBox1, 260, 0);
                gra2 = new CSpeedGraph(groupBox2,260,-1);
               
                gra2.Driver = graph2;
                gra1.Driver = graph1;

                gra1.TitleX = "Velocity (kph)";
                gra1.TitleY = "Time (t)";

                gra2.GraphEnabled = true;
                gra1.GraphEnabled = true;

                gra3 = new CHistGraph(groupBox3, 260, 0);
                gra4 = new CSpeedGraph(groupBox4, 260, -1);

                gra4.Driver = graph4;
                gra3.Driver = graph3;

                gra3.TitleX = "Velocity (kph)";
                gra3.TitleY = "Time (t)";

                gra4.GraphEnabled = true;
                gra3.GraphEnabled = true;

                timer1.Enabled = true;
                timer2.Enabled = true;
                button1.Text = "&Stop Demo";
             
              }
            else if (timer1.Enabled == true)
            {
                timer1.Enabled = false;
                button1.Text = "&Start Demo";
            }
            else
            {
                timer1.Enabled = true;
                button1.Text = "&Stop Demo";
            }
            
            
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            Random r = new Random(DateTime.Now.Millisecond);
            int offset = r.Next(-30,30);
            if (curSpeed + offset >= 260)
            {
                curSpeed -= offset;
            }
            else if (curSpeed + offset <= 0)
            {
                curSpeed -= offset;
            }
            else
            {
                curSpeed += offset;
            }

            graph1.setNextValue(curSpeed);
            graph2.setNextValue(curSpeed);
            label1.Text = curSpeed.ToString() + " km/h";

        }

        private void timer2_Tick(object sender, EventArgs e)
        {
            Random r = new Random(DateTime.Now.Millisecond);
            int offset = r.Next(-30, 30);
            if (curSpeed1 + offset >= 260)
            {
                curSpeed1 -= offset;
            }
            else if (curSpeed1 + offset <= 0)
            {
                curSpeed1 -= offset;
            }
            else
            {
                curSpeed1 += offset;
            }

            graph3.setNextValue(curSpeed1);
            graph4.setNextValue(curSpeed1);
            label2.Text = curSpeed1.ToString() + " km/h";

           // this.Text = "UGRacer PitStop :: Graph Demo (" + curSpeed.ToString() + " km/h)";
        }

        
    }
}
