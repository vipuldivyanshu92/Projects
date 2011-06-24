using System;
using System.Windows.Shapes;

namespace AI4_AE1
{
    class ProximitySensor : IProximitySensor
    {
        private double angleOffset;
        private int length;
        private Segment range;

        public ProximitySensor(int length, double angleOffset)
        {
            this.angleOffset = angleOffset;
            this.length = length;
        }

        public int Length
        {
            get { return length; }
        }

        public bool againstWall()
        {
            double distance = getDistance();
            return (int)distance == 0;
        }

        public bool inRange()
        {
            return getDistance() != -1;
        }

        public double getDistance()
        {
            // Retrieve the environment
            Environment env = Environment.Instance;
            double maxDistance = -1;

            // Create the range segment
            this.range = new Segment();
            range.Start.X = env.AgentPosition.X;
            range.Start.Y = env.AgentPosition.Y;
            range.End.X = env.AgentPosition.X;
            range.End.Y = env.AgentPosition.Y + length;
            range = range.Rotate(env.AgentAngle + angleOffset);

            // Go through the list of segments, not neat O(n) but execution
            // fast enough for this simulation purpose
            foreach (Segment s in env.Segments)
            {
                Point p;
                if ((p = range.Intersects(s)) != null)
                {
                    double v = p.Distance(range.Start);
                    if (v < maxDistance || maxDistance == -1)
                    {
                        maxDistance = v;
                    }
                }
            }
            
            return maxDistance;
        }

        public System.Windows.UIElement getUIElement()
        {
            getDistance();

            Line line = new Line();
            line.X1 = range.Start.X;
            line.Y1 = range.Start.Y;
            line.X2 = range.End.X;
            line.Y2 = range.End.Y;
            line.Stroke = System.Windows.Media.Brushes.Red;

            return line;
        }

        public Segment Range
        {
            get { return range; }
        }
    }
}
