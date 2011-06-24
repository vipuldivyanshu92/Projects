using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace AE1_WPF
{
    /// <summary>
    /// Interaction logic for LinkUI.xaml
    /// </summary>
    public partial class LinkUI : UserControl
    {
        private NodeUI endPoint1;
        private NodeUI endPoint2;
        private int cost;

        public LinkUI(NodeUI ep1, NodeUI ep2, int c)
        {
            endPoint1 = ep1;
            endPoint2 = ep2;

            InitializeComponent();

            Cost = c;
            updateLink();
        }

        public int Cost
        {
            get { return cost; }
            set
            {
                cost = value;
                label.Text = value.ToString();
            }
        }

        public NodeUI EndPoint1
        {
            get { return endPoint1; }
            set { endPoint1 = value; }
        }

        public NodeUI EndPoint2
        {
            get { return endPoint2; }
            set { endPoint2 = value; }
        }

        public void updateLink()
        {
            line.X1 = endPoint1.Anchor.X;
            line.Y1 = endPoint1.Anchor.Y;
            line.X2 = endPoint2.Anchor.X;
            line.Y2 = endPoint2.Anchor.Y;

            Canvas.SetTop(label, line.Y1 + (line.Y2 - line.Y1) / 2);
            Canvas.SetLeft(label, line.X1 + (line.X2 - line.X1) / 2);
        }

        public override string ToString()
        {
            return EndPoint1.ToString() + "," + EndPoint2.ToString();
        }
    }
}
