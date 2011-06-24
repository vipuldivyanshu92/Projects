using System;
using System.Collections.Generic;
using System.Windows;

namespace AI4_AE1
{
    class Environment
    {
        private static Environment instance;
        private List<Segment> segments;

        private Point agentPosition;
        private double agentAngle;
        private double scale;

        private Environment()
        {
            segments = new List<Segment>();
        }

        public static Environment Instance
        {
            get
            {
                if (instance == null)
                    instance = new Environment();
                return instance;
            }
        }

        public List<Segment> Segments
        {
            get { return segments; }
        }

        public Point AgentPosition
        {
            get { return agentPosition; }
            set { agentPosition = value; }
        }

        public double AgentAngle
        {
            get { return agentAngle; }
            set { agentAngle = value; }
        }

        public double Scale
        {
            get { return scale; }
            set { scale = value; }
        }
    }
}
