using System;

namespace AI4_AE1
{
    public class Segment
    {
        private Point start;
        private Point end;

        public Point Start
        {
            get { return start; }
            set { start = new Point(value); }
        }

        public Point End
        {
            get { return end; }
            set { end = new Point(value); }
        }

        public Segment()
        {
            start = new Point();
            end = new Point();
        }

        public Segment(Point start, Point end)
        {
            this.Start = start;
            this.End = end;
        }

        /// <summary>
        /// Perform a rotation by the angle alpha
        /// </summary>
        /// <param name="alpha">angle in degrees</param>
        /// <returns>the rotated segment</returns>
        public Segment Rotate(double alpha)
        {
            // Change from degrees to radians
            alpha = alpha * Math.PI / 180;

            // Translate to origin
            Segment r = this.Translate(new Point(0, 0));

            // Rotate
            double x = r.End.X * Math.Cos(alpha) - r.End.Y * Math.Sin(alpha);
            double y = r.End.X * Math.Sin(alpha) + r.End.Y * Math.Cos(alpha);
            r.End.X = x;
            r.End.Y = y;

            // Translate to original position
            return r.Translate(this.Start);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="p">Point to translate the origin to</param>
        /// <returns>translated segment</returns>
        public Segment Translate(Point p)
        {
            Segment r = new Segment();

            r.Start = p;
            r.End.X = this.End.X - this.Start.X + p.X;
            r.End.Y = this.End.Y - this.Start.Y + p.Y;

            return r;
        }

        /// <summary>
        /// Return the point of intersection of the two segments AB and CD
        /// if the two segments does not intersect returns null
        /// </summary>
        /// <param name="seg">segment</param>
        /// <returns>A point of intersection or null</returns>
        public Point Intersects(Segment seg)
        {
            double deltaACy = this.Start.Y - seg.Start.Y;
            double deltaDCx = seg.End.X - seg.Start.X;
            double deltaACx = this.Start.X - seg.Start.X;
            double deltaDCy = seg.End.Y - seg.Start.Y;
            double deltaBAx = this.End.X - this.Start.X;
            double deltaBAy = this.End.Y - this.Start.Y;

            double denominator = deltaBAx * deltaDCy - deltaBAy * deltaDCx;
            double numerator = deltaACy * deltaDCx - deltaACx * deltaDCy;

            if (denominator == 0)
            {
                if (numerator == 0)
                {
                    // collinear. Potentially infinite intersection points.
                    // Check and return one of them.
                    if (this.Start.X >= seg.Start.X && this.Start.X <= seg.End.X)
                    {
                        return this.Start;
                    }
                    else if (seg.Start.X >= this.Start.X && seg.Start.X <= this.End.X)
                    {
                        return seg.Start;
                    }
                    else
                    {
                        return null;
                    }
                }
                else
                { // parallel
                    return null;
                }
            }

            double r = numerator / denominator;
            if (r < 0 || r > 1)
            {
                return null;
            }

            double s = (deltaACy * deltaBAx - deltaACx * deltaBAy) / denominator;
            if (s < 0 || s > 1)
            {
                return null;
            }

            return new Point(this.Start.X + r * deltaBAx, this.Start.Y + r * deltaBAy);
        }
    }
}
