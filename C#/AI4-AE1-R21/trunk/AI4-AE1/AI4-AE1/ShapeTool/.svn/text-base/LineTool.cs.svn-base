using System;
using System.Collections.Generic;

namespace AI4_AE1.ShapeTool
{
    class LineTool : IShapeTool
    {
        private List<Segment> segments = new List<Segment>();
        private Point start;

        public void update(Point p, bool shiftPressed, bool ctrlPressed)
        {
            segments.Clear();
            segments.Add(new Segment((Point)start, p));
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
