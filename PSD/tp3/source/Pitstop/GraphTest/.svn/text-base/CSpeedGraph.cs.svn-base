using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Diagnostics;

namespace GraphTest
{
    public partial class CSpeedGraph : UserControl, IGraph
    {
        private Point _origin;
        private Point _curPt;
        private double dpkm;
        // Private class variables
        private string _xTitle = "t";
        private string _yTitle = "y";
        private IGraphDriver _driver;
        private int _delay = 100;
        private bool _enabled = false;
        private float _maxY,  _minY;

        // Public Properties
        public IGraphDriver Driver
        {
            get { return _driver; }
            set { _driver = value; }
        }
        public bool GraphEnabled
        {
            get { return _enabled; }
            set { _enabled = value; timer1.Enabled = value; }
        }
        public int RefreshRate
        {
            get { return _delay; }
            set
            {
                _delay = value;
                timer1.Interval = _delay;
            }
        }
        public string TitleX
        {
            get { return _xTitle; }
            set { _xTitle = value; }
        }
        public string TitleY
        {
            get { return _yTitle; }
            set { _yTitle = value; }
        }
        public int MaximumY
        {
            get { return (int)_maxY; }
            set { 
                _maxY = value;
                dpkm = 180 / _maxY;
            }
        }
        public int MinimumY
        {
            get { return (int)_minY; }
            set { _minY = value; }
        }      // Not needed in this implementation
        public CSpeedGraph(System.Windows.Forms.Control Parent, int max, int min)
        {
            InitializeComponent();
            this.Parent = Parent;
            this.Dock = DockStyle.Fill;
            Debug.WriteLine("W: " + this.Width + " H: " + this.Height );
            this.Visible = true;
            
            MinimumY = min;
            MaximumY = max;
            
        }

        public void DrawAxis()
        {
            Bitmap b = new Bitmap(this.Width, this.Height);
            _origin = new Point(this.Width / 2, this.Width / 2);
            Graphics _gra = Graphics.FromImage(b);

            _gra.DrawArc(Pens.Black, new Rectangle(12, 12, this.Width-24, this.Height), 180, 180);

            for (int i = (int) (0-(0.5*_maxY)); i <= (int) ((0.5*_maxY)); i += 10)
            {
                
                double angle = dpkm * (i) * (Math.PI / 180);
                double radius = (this.Width / 2) - 12;
                int xEnd = (int) (radius*Math.Sin(angle));
                int yEnd = (int) (radius*Math.Cos(angle));
                int xStart = (int) ((radius-5) * Math.Sin(angle));
                int yStart = (int) ((radius-5) * Math.Cos(angle));
                Point outer = new Point((int) _origin.X - xEnd, (int) _origin.Y - yEnd);
                Point inner = new Point((int) _origin.X - xStart, (int) _origin.Y - yStart);
                _gra.DrawLine(Pens.Black, outer, inner);

            }
            if (_curPt == null) { _curPt = new Point(25, this.Width / 2); }
            //_curPt = new Point(25, _origin.Y);
            _gra.DrawLine(Pens.Red, _origin, _curPt);
            pictureBox1.Image = b;
            
        }
        public void AddValue(int yValue)
        {
            
            double angle = ((90-(dpkm * (yValue))) * (Math.PI / 180));
            double radius = 0.75*((this.Width / 2)-12);
            Point outer = new Point((int)((this.Width / 2) - (radius * Math.Sin(angle))), (int)((this.Width / 2) - radius * Math.Cos(angle)));
            _curPt = outer;
            DrawAxis();
          
        }
        private void timer1_Tick(object sender, EventArgs e)
        {
            if (_driver.hasNextValue())
            {
                AddValue(_driver.getNextValue());
            }

        }

    }
}