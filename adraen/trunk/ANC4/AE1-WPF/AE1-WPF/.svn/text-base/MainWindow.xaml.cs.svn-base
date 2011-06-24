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
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        Dictionary<String, NodeUI> nodes = new Dictionary<string, NodeUI>();
        Dictionary<NodeUI, List<LinkUI>> links = new Dictionary<NodeUI, List<LinkUI>>();
        List<NodeUI> selectedNodes = new List<NodeUI>();

        public MainWindow()
        {
            InitializeComponent();
        }

        // Remove the highlight on the selected nodes, and empty the list
        private void clearSelectedNodes()
        {
            foreach (NodeUI n in selectedNodes)
                n.Selected = false;
            selectedNodes.Clear();
        }

        // Triggered when a node is clicked, highlight the node and capture the mouse
        private void node_MouseLeftButtonDown(object sender, MouseEventArgs e)
        {
            NodeUI node = (NodeUI)sender;

            //
            dataGrid1.ItemsSource = node.RoutingTable.displayRoutingTable();

            //
            if (!selectedNodes.Contains(node))
            {
                node.CaptureMouse();
                Mouse.OverrideCursor = System.Windows.Input.Cursors.Cross;
                ForceCursor = true;
                selectedNodes.Add(node);
                node.Selected = true;
            }
        }

        // Triggered when the mouse is moved and the node is selected, used to update the GUI
        private void node_MouseMove(object sender, MouseEventArgs e)
        {
            NodeUI node = (NodeUI)sender;
            if (Mouse.LeftButton == MouseButtonState.Pressed && node.Selected)
            {
                Point pos = e.GetPosition(canvas1);
                Canvas.SetLeft(node, pos.X - node.RenderSize.Width / 2);
                Canvas.SetTop(node, pos.Y - node.RenderSize.Height / 2);

                if (links.ContainsKey(node))
                    foreach (LinkUI l in links[node])
                        l.updateLink();
            }
        }

        // Triggered when the mouse is released, release the mouse capture restore default cursor
        private void node_MouseLeftButtonUp(object sender, MouseEventArgs e)
        {
            ((NodeUI)sender).ReleaseMouseCapture();
            Mouse.OverrideCursor = null;
            ForceCursor = false;
        }

        // 
        private void Button_Click(object sender, RoutedEventArgs e)
        {
            //
            if (!(String.IsNullOrWhiteSpace(textBox1.Text) || nodes.ContainsKey(textBox1.Text)))
            {
                NodeUI nui = new NodeUI();
                Canvas.SetLeft(nui, 50);
                Canvas.SetTop(nui, 50);

                nui.Label = textBox1.Text;

                nui.MouseLeftButtonDown += new MouseButtonEventHandler(node_MouseLeftButtonDown);
                nui.MouseLeftButtonUp += new MouseButtonEventHandler(node_MouseLeftButtonUp);
                nui.MouseMove += new MouseEventHandler(node_MouseMove);

                nodes.Add(nui.Label, nui);
                canvas1.Children.Add(nui);
                textBox1.Text = String.Empty;
            }
            else
                listBox1.Items.Add("The node name specified is incorrect.");
        }

        private void canvas1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.LeftShift || e.Key == Key.RightShift)
            {
                listBox1.Items.Add("shift pressed");
            }
        }

        private void Button_Click_1(object sender, RoutedEventArgs e)
        {
            if (selectedNodes.Count == 2)
            {
                NodeUI n1 = selectedNodes[0];
                NodeUI n2 = selectedNodes[1];
                int distance = int.Parse(textBox2.Text);
                LinkUI link = new LinkUI(n1, n2, distance);
                Canvas.SetZIndex(link, -1);

                if (!links.ContainsKey(n1))
                    links.Add(n1, new List<LinkUI>());

                if (!links.ContainsKey(n2))
                    links.Add(n2, new List<LinkUI>());

                n1.RoutingTable.addRoutingEntry(n2, distance, link);
                n2.RoutingTable.addRoutingEntry(n1, distance, link);
                n1.addLink(link);
                n2.addLink(link);

                links[n1].Add(link);
                links[n2].Add(link);
                canvas1.Children.Add(link);
            }
            else
                listBox1.Items.Add("Two nodes need to be selected");
        }

        private void canvas1_PreviewMouseDown(object sender, MouseButtonEventArgs e)
        {
            if (!(Keyboard.IsKeyDown(Key.LeftShift) || Keyboard.IsKeyDown(Key.RightShift)))
                clearSelectedNodes();
        }

        private void Button_Click_2(object sender, RoutedEventArgs e)
        {
            //
            foreach (NodeUI n in nodes.Values)
            {
                n.propagateRoutingTable();
            }
        }
    }
}
