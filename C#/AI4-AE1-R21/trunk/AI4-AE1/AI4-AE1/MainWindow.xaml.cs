using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Shapes;
using System.Timers;
using System.Threading;
using System.Windows.Threading;
using AI4_AE1.ShapeTool;

namespace AI4_AE1
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private IShapeTool selectedTool;
        private List<UIElement> snapshot = new List<UIElement>();
        private Agent agent;
        private List<UIElement> tempElements = new List<UIElement>();
        private Point panStart;
        private Point offset = new Point();

        public MainWindow()
        {
            InitializeComponent();
        }

        private void canvas1_PreviewMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            if (selectedTool != null)
                selectedTool.Start = e.GetPosition(grid1);

            grid1.CaptureMouse();
        }

        private void canvas1_PreviewMouseMove(object sender, MouseEventArgs e)
        {
            Point p = e.GetPosition(grid1);

            if (selectedTool != null && selectedTool.Start != null)
            {

                selectedTool.update(p, Keyboard.IsKeyDown(Key.LeftShift) || Keyboard.IsKeyDown(Key.RightShift),
                    Keyboard.IsKeyDown(Key.LeftCtrl) || Keyboard.IsKeyDown(Key.RightCtrl));

                // Remove old snapshot
                foreach (UIElement elem in snapshot)
                    grid1.Children.Remove(elem);

                // Add new
                foreach (Segment s in selectedTool.Segments)
                {
                    snapshot.Add(drawSegment(s, Brushes.Black));
                }
            }
        }

        private void canvas1_PreviewMouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            grid1.ReleaseMouseCapture();

            if (selectedTool != null && selectedTool.Start != null && selectedTool.Segments != null)
            {
                Environment.Instance.Segments.AddRange(selectedTool.Segments);

                snapshot.Clear();
                selectedTool.finalize();
                selectedTool = (IShapeTool)Activator.CreateInstance(selectedTool.GetType());
            }
        }

        private UIElement drawSegment(Segment s, SolidColorBrush color)
        {
            Line line = new Line();

            line.X1 = s.Start.X;
            line.Y1 = s.Start.Y;
            line.X2 = s.End.X;
            line.Y2 = s.End.Y;
            line.Stroke = color;

            //canvas1.Children.Add(line);
            grid1.Children.Add(line);

            return line;
        }

        private void button2_Click(object sender, RoutedEventArgs e)
        {
            agent = new Agent();
            Environment env = Environment.Instance;
            env.AgentAngle = 0;
            env.AgentPosition = new Point(50, 50);

            Thread thread = new Thread(new ThreadStart(agent.run));
            thread.Start();

            System.Timers.Timer t = new System.Timers.Timer(100);
            t.Elapsed += new ElapsedEventHandler(OnTimedEvent);
            t.Enabled = true;

            System.Timers.Timer t2 = new System.Timers.Timer(100);
            t2.Elapsed += new ElapsedEventHandler(OnTimedEvent2);
            t2.Enabled = true;
        }

        private void OnTimedEvent(object source, ElapsedEventArgs e)
        {
            DispatcherOperation dispatcherOp = grid1.Dispatcher.BeginInvoke(DispatcherPriority.Normal,
                new Action(delegate()
                    {
                        foreach (UIElement elem in tempElements)
                            grid1.Children.Remove(elem);
                        tempElements = new List<UIElement>();
                        
                        tempElements.Add(agent.ShortRangeSensor.getUIElement());
                        tempElements.Add(agent.LongRangeSensor.getUIElement());

                        foreach (UIElement elem in tempElements)
                            grid1.Children.Add(elem);
                    }
            ));
        }

        private void OnTimedEvent2(object source, ElapsedEventArgs e)
        {
            DispatcherOperation dispatcherOp = grid2.Dispatcher.BeginInvoke(DispatcherPriority.Normal,
                new Action(delegate()
                {
                    grid2.Children.Clear();

                    List<BDNode> nodes = agent.Nodes;
                    Line line;

                    label1.Content = String.Format("Amount of reference points {0}", nodes.Count);

                    line = new Line();
                    line.Stroke = Brushes.Red;
                    line.StrokeThickness = 5;
                    BDNode n = agent.Nearest;
                    if (n != null)
                    {
                        line.X1 = n.Coord.X + offset.X;
                        line.Y1 = n.Coord.Y + offset.Y;
                        line.X2 = n.Coord.X + 2 + offset.X;
                        line.Y2 = n.Coord.Y + 2 + offset.Y;
                        grid2.Children.Add(line);
                    }


                    line = new Line();
                    line.Stroke = Brushes.Green;
                    line.StrokeThickness = 5;
                    Point currentPoint = agent.CurrentPosition;
                    if (n != null)
                    {
                        line.X1 = currentPoint.X + offset.X;
                        line.Y1 = currentPoint.Y + offset.Y;
                        line.X2 = currentPoint.X + 2 + offset.X;
                        line.Y2 = currentPoint.Y + 2 + offset.Y;
                        grid2.Children.Add(line);
                    }

                    foreach (BDNode node in nodes)
                    {
                        if (node.Next != null)
                        {
                            line = new Line();
                            line.Stroke = Brushes.Black;
                            line.X1 = node.Coord.X + offset.X;
                            line.Y1 = node.Coord.Y + offset.Y;
                            line.X2 = node.Next.Coord.X + offset.X;
                            line.Y2 = node.Next.Coord.Y + offset.Y;

                            grid2.Children.Add(line);
                        }
                    }
                }
            ));
        }

        private void button3_Click(object sender, RoutedEventArgs e)
        {
            selectedTool = new LineTool();
        }

        private void button4_Click(object sender, RoutedEventArgs e)
        {
            selectedTool = new RectangleTool();
        }

        private void button5_Click(object sender, RoutedEventArgs e)
        {
            selectedTool = new EllipseTool();
        }

        private void grid2_PreviewMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            panStart = e.GetPosition(grid2);
            grid2.CaptureMouse();
        }

        private void grid2_PreviewMouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            Point panEnd = e.GetPosition(grid2);
            offset += panEnd - panStart;

            grid2.ReleaseMouseCapture();
        }

        private void button1_Click(object sender, RoutedEventArgs e)
        {
            if (agent != null)
                agent.GoHome();
        }
    }
}
