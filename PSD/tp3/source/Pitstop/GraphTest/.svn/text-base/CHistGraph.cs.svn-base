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
    public partial class CHistGraph : UserControl, IGraph
    {
        // Publicly Exposed Properties

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
            set {
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
            set { _maxY = value; }
        }
        public int MinimumY
        {
            get { return (int) _minY; }
            set { _minY = value; }
        }
        
        // Private class variables
        private string _xTitle = "t";
        private string _yTitle = "y";
        private IGraphDriver _driver;
        private int _delay = 100;
        private bool _enabled;
        private float _maxY, _minY, _yScale;
        private PointF _origin = new PointF();
        private List<PointF> _buffer = new List<PointF>();
        private List<PointF> _nbuffer = new List<PointF>();

        // Public Methods
        public CHistGraph(System.Windows.Forms.Control Parent, int Max, int Min)
        {
            InitializeComponent();
            this.Parent = Parent;
            this.Visible = true;
            this.Dock = DockStyle.Fill;
            MaximumY = Max;
            MinimumY = Min;
            
        }

        // Private Methods
        private void GraphingControl_Load(object sender, EventArgs e)
        {
           
        }
        private void Redraw()
        {
            
           Bitmap b = new Bitmap(this.Width, this.Height);
           Graphics g = Graphics.FromImage(b);

            
            if (_buffer.Count > 1)
            {
                PointF[] points = _buffer.ToArray<PointF>();
                g.DrawCurve(Pens.Blue, points);
            }
            this.DrawAxis(g);
            pictureBox1.Image = null;
            pictureBox1.Image = b;
        }
        private void AddValue(int yValue)
        {
            PointF np = new PointF();
            if (_buffer.Count < this.Width - 24)
            {
                np.Y = _origin.Y - (_yScale * yValue);
                np.X = 12 + _buffer.Count;
                _buffer.Add(np);
            }
            else
            {
                _buffer.RemoveAt(0);
                _nbuffer.Clear();
                for (int i = 0; i < _buffer.Count; i++)
                {
                    PointF b = _buffer[i];
                    b.X -= 1;
                    _nbuffer.Add(b);
                }
                _buffer = new List<PointF>(_nbuffer);
            }
            Redraw();
        }
        private void DrawAxis(Graphics _gra)
        {
            // Calculate Scales
            _yScale = (this.Height - 24) / ((_maxY - _minY));
            _origin.X = 12;
            _origin.Y = (_minY < 0) ? this.Height - 12 - (_yScale * (-1 * _minY)) : this.Height - 12;

            // DRAW Y AXIS
            _gra.DrawLine(Pens.Black, _origin, new Point((int)_origin.X, (int)12));
            _gra.DrawLine(Pens.Black, _origin, new Point((int)_origin.X, (int)this.Height - 12));
            // DRAW X axis
            _gra.DrawLine(Pens.Black, _origin, new Point(12, (int)_origin.Y));
            _gra.DrawLine(Pens.Black, _origin, new Point((int)this.Width - 12, (int)_origin.Y));
            // LABEL Axii
            _gra.DrawString(_yTitle, new Font("Microsoft Sans Serif", (float)8.5, FontStyle.Italic), Brushes.Black, new Point((int)_origin.X - 12, 0));
            _gra.DrawString(_xTitle, new Font("Microsoft Sans Serif", (float)8.5, FontStyle.Italic), Brushes.Black, new Point((int)(this.Width / 2), (int)(_origin.Y - 2)));

            _gra.DrawString(_maxY.ToString(), new Font("Microsoft Sans Serif", (float) 8.5), Brushes.Black, new Point((int)_origin.X + 2, 12));
            _gra.DrawString(_minY.ToString(), new Font("Microsoft Sans Serif", (float)8.5), Brushes.Black, new Point((int)_origin.X, (int)_origin.Y));
            
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
