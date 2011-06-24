using System;
using System.Collections.Generic;
using System.Windows.Shapes;

namespace AI4_AE1.Sensors
{
    class Bumper : IBumper
    {
        private int radius;
        private double angle;
        private const int nbsegments = 6;
        private Segment[] segments = new Segment[nbsegments];

        public Bumper(int radius, double angle)
        {
            this.radius = radius;
            this.angle = angle;
        }

        public bool collide()
        {
            // Retrieve the environment singleton
            Environment env = Environment.Instance;

            // Create the initial segment for the angle and starting point of the bumper
            double a = angle / nbsegments;
            Segment vector = new Segment(env.AgentPosition, env.AgentPosition + new Point(-radius, 0));
            vector = vector.Rotate(-(180 - angle) / 2);
            vector = vector.Rotate(env.AgentAngle);

            // Create the bumper segments
            for (int i = 0; i < nbsegments; i++)
            {
                Segment seg = new Segment();
                seg.Start = vector.End;
                vector = vector.Rotate(-a);
                seg.End = vector.End;

                segments[i] = seg;
            }

            // Check if any of the segment collides
            lock (env.Segments)
            {
                foreach (Segment s in env.Segments)
                {
                    foreach (Segment b in segments)
                    {
                        if (b.Intersects(s) != null)
                            return true;
                    }
                }
            }

            return false;
        }

        public List<System.Windows.UIElement> getUIElement()
        {
            collide();
            List<System.Windows.UIElement> elements = new List<System.Windows.UIElement>();

            foreach (Segment s in segments)
            {
                Line line = new Line();
                line.X1 = s.Start.X;
                line.Y1 = s.Start.Y;
                line.X2 = s.End.X;
                line.Y2 = s.End.Y;
                line.Stroke = System.Windows.Media.Brushes.Red;

                elements.Add(line);
            }

            return elements;
        }
    }
}
