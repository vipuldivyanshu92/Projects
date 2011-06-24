using System;
using System.Collections.Generic;
using System.Linq;

namespace AI4_AE1.ShapeTool
{
    class EllipseTool : IShapeTool
    {
        private List<Segment> segments;
        private Point start, end;
        private double angle;

        /// <summary>
        /// 
        /// </summary>
        /// <param name="x">X coordinate</param>
        /// <param name="y">Y coordinate</param>
        /// <param name="a">semimajor axis</param>
        /// <param name="b">semiminor axis</param>
        /// <param name="angle">angle of the ellipse</param>
        /// <param name="steps"></param>
        /// <returns></returns>
        public static List<Point> calculateEllipse(double x, double y, double a, double b, double angle, int steps)
        {
            List<Point> points = new List<Point>();

            // Angle is in degrees
            double beta = -angle * (Math.PI / 180);
            double sinbeta = Math.Sin(beta);
            double cosbeta = Math.Cos(beta);

            for (int i = 0; i < 360; i += 360 / steps)
            {
                double alpha = i * (Math.PI / 180);
                double sinalpha = Math.Sin(alpha);
                double cosalpha = Math.Cos(alpha);

                Point p = new Point();
                p.X = x + (a * cosalpha * cosbeta - b * sinalpha * sinbeta);
                p.Y = y + (a * cosalpha * sinbeta + b * sinalpha * cosbeta);

                points.Add(p);
            }

            return points;
        }

        private static List<Segment> connectPoints(List<Point> points, bool loop)
        {
            List<Segment> segs = new List<Segment>();

            if (points.Count < 2)
                throw new ArgumentException();

            Point prev = points.First();

            Segment segment;
            for (int i = 1; i < points.Count; i++)
            {
                segment = new Segment();
                segment.Start = prev;
                segment.End = points[i];
                prev = points[i];

                segs.Add(segment);
            }

            if (loop)
            {
                segment = new Segment();
                segment.Start = points.First();
                segment.End = points.Last();
                segs.Add(segment);
            }

            return segs;
        }

        public void update(Point p, bool shiftPressed, bool ctrlPressed)
        {
            Point s = (Point)start;

            if (ctrlPressed)
            {
                // calculate the angle
                double a = p.Y < s.Y ? s.Y - p.Y : -(p.Y - s.Y);
                double b = p.X < s.X ? -(s.X - p.X) : p.X - s.X;
                angle = Math.Tanh(a / b) * 180 / Math.PI;
            }
            else
            {
                end = p;
            }

            Point e = (Point)end;

            segments = connectPoints(calculateEllipse(
                s.X,
                s.Y,
                s.X < e.X ? e.X - s.X : s.X - e.X,
                s.Y < e.Y ? e.Y - s.Y : s.Y - e.Y, angle, 36), true);
        }

        public void finalize()
        {
        }

        public List<Segment> Segments
        {
            get { return segments; }
        }

        public Point Start
        {
            get { return start; }
            set { start = value; }
        }
    }
}
