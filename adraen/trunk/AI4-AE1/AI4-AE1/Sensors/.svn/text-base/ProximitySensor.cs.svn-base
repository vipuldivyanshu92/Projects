using System;
using System.Windows.Shapes;

namespace AI4_AE1.Sensors
{
    class ProximitySensor : IProximitySensor
    {
        private double angleOffset;
        private int lengthOffset;
        private int length;
        private Segment range;

        public ProximitySensor(int length, int lengthOffset, double angleOffset)
        {
            this.angleOffset = angleOffset;
            this.length = length;
            this.lengthOffset = lengthOffset;
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
            double minDistance = -1;

            // Create the offset segment
            Segment offset = new Segment();
            offset.Start = env.AgentPosition;
            offset.End = env.AgentPosition + new Point(0, lengthOffset);

            // Create the range segment
            Segment full = new Segment();
            full.Start = env.AgentPosition;
            full.End = env.AgentPosition + new Point(0, length + lengthOffset);

            range = new Segment();
            range.Start = offset.Rotate(env.AgentAngle + angleOffset).End;
            range.End = full.Rotate(env.AgentAngle + angleOffset).End;

            // Go through the list of segments, not neat O(n) but execution
            // fast enough for this simulation purpose
            foreach (Segment s in env.Segments)
            {
                Point p;
                if ((p = range.Intersects(s)) != null)
                {
                    double v = p.Distance(range.Start);
                    if (v < minDistance || minDistance == -1)
                    {
                        minDistance = v;
                    }
                }
            }
            
            return minDistance;
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
