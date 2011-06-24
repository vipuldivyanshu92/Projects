using System;

namespace AI4_AE1
{
    [Serializable]
    public class Point
    {
        private double x;
        private double y;

        public double X
        {
            get { return x; }
            set { x = value; }
        }

        public double Y
        {
            get { return y; }
            set { y = value; }
        }

        public Point()
        {
            x = 0;
            y = 0;
        }

        public Point(double X, double Y)
        {
            x = X;
            y = Y;
        }

        public Point(Point p)
        {
            x = p.x;
            y = p.y;
        }

        public double Distance(Point p)
        {
            return Math.Sqrt(SquareDistance(p));
        }

        public double SquareDistance(Point p)
        {
            return Math.Pow((x - p.X), 2) + Math.Pow((y - p.Y), 2);
        }

        public static implicit operator Point(System.Windows.Point p)
        {
            return new Point(p.X, p.Y);
        }

        public static Point operator -(Point a, Point b)
        {
            return new Point(a.X - b.X, a.Y - b.Y);
        }

        public static Point operator +(Point a, Point b)
        {
            return new Point(a.X + b.X, a.Y + b.Y);
        }

        public static bool operator ==(Point a, Point b)
        {
            // If both are null, or both are same instance, return true.
            if (System.Object.ReferenceEquals(a, b))
                return true;

            // If one is null, but not both, return false.
            if (((object)a == null) || ((object)b == null))
                return false;

            return a.X == b.X && a.Y == b.Y;
        }

        public static bool operator !=(Point a, Point b)
        {
            return !(a == b);
        }

        public bool Equals(Point p)
        {
            if (p == null)
                return false;

            return x == p.X && y == p.Y;
        }

        public override bool Equals(Object o)
        {
            // If parameter is null return false.
            if (o == null)
                return false;

            // If parameter cannot be cast to Point return false.
            Point p = o as Point;
            if ((System.Object)p == null)
                return false;

            // Return true if the fields match:
            return (x == p.x) && (y == p.y);
        }

        public override int GetHashCode()
        {
            return (int)x ^ (int)y;
        }

        public override string ToString()
        {
            return String.Format("({0}, {1})", x, y);
        }
    }
}
