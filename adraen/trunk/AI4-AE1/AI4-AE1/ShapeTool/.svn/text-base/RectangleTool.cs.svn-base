using System;
using System.Collections.Generic;
using System.Windows;

namespace AI4_AE1.ShapeTool
{
    class RectangleTool : IShapeTool
    {
        private List<Segment> segments = new List<Segment>();
        private Point start, end = null;
        private double angle;

        public void update(Point p, bool shiftPressed, bool ctrlPressed)
        {
            Point s = (Point)start;
            segments.Clear();

            if (ctrlPressed)
            {
                // calculate the angle
                double A = p.Y < s.Y ? s.Y - p.Y : -(p.Y - s.Y);
                double B = p.X < s.X ? -(s.X - p.X) : p.X - s.X;
                angle = Math.Tanh(A / B) * 180 / Math.PI;
            }
            else
            {
                end = p;
            }

            Point e = (Point)end;

            Point a = s;
            Point b = new Point(e.X, a.Y);
            Point c = new Point(b.X, e.Y);
            Point d = new Point(a.X, c.Y);

            Segment AB = new Segment(a, b).Rotate(-angle);
            Segment BC = new Segment(b, c).Rotate(-angle).Translate(AB.End);
            Segment CD = new Segment(c, d).Rotate(-angle).Translate(BC.End);
            Segment DA = new Segment(d, a).Rotate(-angle).Translate(CD.End);

            segments.Add(AB);
            segments.Add(BC);
            segments.Add(CD);
            segments.Add(DA);
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
