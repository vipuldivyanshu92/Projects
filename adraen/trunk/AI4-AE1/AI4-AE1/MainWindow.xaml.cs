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
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using AI4_AE1.ShapeTool;

namespace AI4_AE1
{
    [Serializable]
    public class DirtElement
    {
        public DirtElement()
        {
            this.element = null;
            this.count = 0;
        }

        [NonSerialized]
        public UIElement element;
        public int count;
    }

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private bool dirtPen;
        private IShapeTool selectedTool;
        private List<UIElement> snapshot = new List<UIElement>();
        private List<UIElement> tempElements = new List<UIElement>();
        private Agent agent;
        private Thread agentThread;
        private Point previousPoint;
        private System.Timers.Timer drawingTimer;
        private DateTime lastTimeReading;
        private double elapsedTime;
        private int times;

        public MainWindow()
        {
            InitializeComponent();
        }

        private void canvas1_PreviewMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            if (dirtPen)
            {
                Point p = e.GetPosition(grid1);

                BDNode n = Environment.Instance.Dirt.Insert(p, new DirtElement(), 0);
                DirtElement de = (DirtElement)n.Value;
                if (de.count == 0)
                {
                    Rectangle r = new Rectangle();
                    r.Stroke = Brushes.Green;
                    r.Fill = Brushes.Green;
                    r.Width = 3;
                    r.Height = 3;
                    r.HorizontalAlignment = HorizontalAlignment.Left;
                    r.VerticalAlignment = VerticalAlignment.Top;
                    r.Margin = new Thickness(p.X, p.Y, 0, 0);
                    de.element = r;
                    grid1.Children.Add(r);
                }
                de.count++;
            }
            else if (selectedTool != null)
                selectedTool.Start = e.GetPosition(grid1);

            grid1.CaptureMouse();
        }

        private void canvas1_PreviewMouseMove(object sender, MouseEventArgs e)
        {
            Point p = e.GetPosition(grid1);

            if (dirtPen && Mouse.LeftButton == MouseButtonState.Pressed)
            {
                BDNode n = Environment.Instance.Dirt.Insert(p, new DirtElement(), 0);
                DirtElement de = (DirtElement)n.Value;
                if (de.count == 0)
                {
                    Rectangle r = new Rectangle();
                    r.Stroke = Brushes.Green;
                    r.Fill = Brushes.Green;
                    r.Width = 3;
                    r.Height = 3;
                    r.HorizontalAlignment = HorizontalAlignment.Left;
                    r.VerticalAlignment = VerticalAlignment.Top;
                    r.Margin = new Thickness(p.X, p.Y, 0, 0);
                    de.element = r;
                    grid1.Children.Add(r);
                }
                de.count++;
            }
            else if (selectedTool != null && selectedTool.Start != null)
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
                lock (Environment.Instance.Segments)
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
            if (agent == null)
            {
                Environment.Instance.RemovedDirtCount = 0;
                lastTimeReading = DateTime.Now;
                agent = new Agent();
                Environment env = Environment.Instance;
                env.AgentAngle = 0;
                env.AgentPosition = new Point(50, 50);
                env.SimulationDuration = 60 * 60 * 1000;
                env.SimulationSpeed = 500;
                previousPoint = env.AgentPosition;

                dumpEnvironment();
                agentThread = new Thread(new ThreadStart(agent.run));
                agentThread.Start();

                drawingTimer = new System.Timers.Timer(100);
                drawingTimer.Elapsed += new ElapsedEventHandler(OnTimedEvent);
                drawingTimer.Enabled = true;
            }
            else
            {
                drawingTimer.Enabled = false;
                agentThread.Abort();
            }
        }

        MemoryStream ms = new MemoryStream();
        BinaryFormatter bf = new BinaryFormatter();
        private void dumpEnvironment()
        {
            bf.Serialize(ms, Environment.Instance);
        }

        private void restoreEnvironment()
        {
            // Restore the environment
            ms.Position = 0;
            Environment.Instance = (Environment)bf.Deserialize(ms);
            Environment.Instance.RemovedDirt = new List<UIElement>();
        }

        private void restart()
        {
            restoreEnvironment();
            button2_Click(null, null);
        }

        private void OnTimedEvent(object source, ElapsedEventArgs e)
        {
            DispatcherOperation dispatcherOp = grid1.Dispatcher.BeginInvoke(DispatcherPriority.Normal,
                new Action(delegate()
                    {
                        elapsedTime += (DateTime.Now - lastTimeReading).TotalMilliseconds * Environment.Instance.SimulationSpeed;
                        lastTimeReading = DateTime.Now;

                        foreach (UIElement elem in tempElements)
                            grid1.Children.Remove(elem);
                        tempElements = new List<UIElement>();

                        // Line to represent the path
                        Line line = new Line();
                        line.Stroke = Brushes.DarkOrange;
                        line.X1 = previousPoint.X;
                        line.Y1 = previousPoint.Y;
                        line.X2 = Environment.Instance.AgentPosition.X;
                        line.Y2 = Environment.Instance.AgentPosition.Y;
                        previousPoint = Environment.Instance.AgentPosition;
                        grid1.Children.Add(line);

                        // Circle to represent the agent
                        Ellipse ellipse = new Ellipse();
                        ellipse.Width = 20;
                        ellipse.Height = 20;
                        ellipse.Stroke = Brushes.Brown;
                        ellipse.Fill = Brushes.Brown;
                        ellipse.HorizontalAlignment = HorizontalAlignment.Left;
                        ellipse.VerticalAlignment = VerticalAlignment.Top;
                        ellipse.Margin = new Thickness(Environment.Instance.AgentPosition.X - 10, Environment.Instance.AgentPosition.Y - 10, 0, 0);
                        
                        tempElements.Add(agent.ShortRangeSensor.getUIElement());
                        tempElements.AddRange(agent.BumperSensor.getUIElement());
                        tempElements.Add(ellipse);

                        lock (Environment.Instance.RemovedDirt)
                        {
                            foreach (UIElement elem in Environment.Instance.RemovedDirt)
                                grid1.Children.Remove(elem);
                            Environment.Instance.RemovedDirt.Clear();
                        }

                        foreach (UIElement elem in tempElements)
                            grid1.Children.Add(elem);

                        label1.Content = String.Format("Elapsed Time : {0:hh\\:mm\\:ss}", TimeSpan.FromMilliseconds(elapsedTime));

                        if (elapsedTime >= Environment.Instance.SimulationDuration)
                        {
                            agentThread.Abort();
                            agent = null;
                            elapsedTime = 0;
                            drawingTimer.Enabled = false;
                            // performance
                            using (TextWriter tw = new StreamWriter("F:\\bench.txt", true))
                                tw.WriteLine(String.Format("{0} / {1}", Environment.Instance.RemovedDirtCount, Environment.Instance.Dirt.Count));
                            times++;
                            if (times < 25)
                                restart();
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

        private void button6_Click(object sender, RoutedEventArgs e)
        {
            if (dirtPen)
                dirtPen = false;
            else
                dirtPen = true;
        }

        private void slider2_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            Environment.Instance.SimulationSpeed = e.NewValue;
        }
    }
}
