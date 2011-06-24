using System;
using System.Collections.Generic;
using System.Windows;

namespace AI4_AE1
{
    [Serializable]
    class Environment
    {
        private static Environment instance;
        private List<Segment> segments;
        private BDTree dirt;
        [NonSerialized]
        private List<UIElement> removedDirt;
        private int removedDirtCount;

        private Point agentPosition;
        private double agentAngle;
        private double scale;
        private double simulationSpeed;
        private double simulationDuration;

        private Environment()
        {
            segments = new List<Segment>();
            dirt = new BDTree();
            removedDirt = new List<UIElement>();
        }

        public static Environment Instance
        {
            get
            {
                if (instance == null)
                    instance = new Environment();
                return instance;
            }
            set
            {
                instance = value;
            }
        }

        public int RemovedDirtCount
        {
            get { return removedDirtCount; }
            set { removedDirtCount = value; }
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

        public BDTree Dirt
        {
            get { return dirt; }
            set { dirt = value; }
        }

        public List<UIElement> RemovedDirt
        {
            get { return removedDirt; }
            set { removedDirt = value; }
        }

        public double SimulationSpeed
        {
            get { return simulationSpeed; }
            set { simulationSpeed = value; }
        }

        public double SimulationDuration
        {
            get { return simulationDuration; }
            set { simulationDuration = value; }
        }
    }
}
