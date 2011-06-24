using System;
using System.Collections.Generic;
using System.ComponentModel;
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
using System.Collections.ObjectModel;

namespace AE1_WPF
{
    /// <summary>
    /// Interaction logic for NodeUI.xaml
    /// </summary>
    public partial class NodeUI : UserControl
    {
        private bool selected;
        private RoutingTable routingTable = new RoutingTable();
        private List<LinkUI> links = new List<LinkUI>();

        public RoutingTable RoutingTable
        {
            get { return routingTable; }
        }

        public void addLink(LinkUI l)
        {
            links.Add(l);
        }

        public List<NodeUI> getNeighbours()
        {
            List<NodeUI> neighbours = new List<NodeUI>();
            foreach (LinkUI l in links)
                neighbours.Add(l.EndPoint1 == this ? l.EndPoint2 : l.EndPoint1);

            return neighbours;
        }

        public void propagateRoutingTable()
        {
            foreach (NodeUI n in getNeighbours())
            {
                n.routingTable.update(this, routingTable);
            }
        }

        public string Label
        {
            get { return label.Text; }
            set { label.Text = value; }
        }

        public bool Selected
        {
            get { return selected; }
            set
            {
                selected = value;
                if (selected)
                    ellipse.Stroke = Brushes.Red;
                else
                    ellipse.Stroke = Brushes.Black;
            }
        }

        public Point Anchor
        {
            get
            {
                return
                    this.TransformToAncestor((Visual)this.Parent).Transform(
                        ellipse.TransformToAncestor(this).Transform(
                            new Point(ellipse.Width / 2, ellipse.Height / 2))
                    );
            }
        }

        public NodeUI()
        {
            InitializeComponent();

            this.routingTable.addRoutingEntry(this, 0, null);
        }

        public override string ToString()
        {
            return label.Text;
        }
    }
}
