using System;
using System.Linq;
using System.Collections.Generic;
using System.Threading;
using System.Windows;

namespace AI4_AE1
{
    class Agent
    {
        private Point startPoint = new Point(0, 0);
        private ProximitySensor longRangeSensor;
        private ProximitySensor shortRangeSensor;
        private Movement movement;
        private Random random;
        private bool gohome;

        //private List<Point> nodes = new List<Point>();
        //private TwoDTree nodes = new TwoDTree();
        //private Point prevPoint = null;
        private BDTree nodes = new BDTree();

        private int distance = 0;
        private double angle = 0;

        public ProximitySensor LongRangeSensor
        {
            get { return longRangeSensor; }
        }

        public ProximitySensor ShortRangeSensor
        {
            get { return shortRangeSensor; }
        }

        public List<BDNode> Nodes
        {
            get { return nodes.Nodes; }
        }

        public BDNode Nearest
        {
            get { return nodes.Nearest(nodes.CurrentPosition(distance, angle), 1)[0]; }
        }

        public void GoHome()
        {
            gohome = true;
        }

        public Point CurrentPosition
        {
            get { return nodes.CurrentPosition(distance, angle); }
        }

        public Agent()
        {
            // create the long range sensor
            longRangeSensor = new ProximitySensor(60, 0);

            // create the short range sensor for wall following
            shortRangeSensor = new ProximitySensor(5, 90);

            // create the movement interface
            movement = new Movement(this);

            random = new Random();
        }

        public void run()
        {
            double prevReading = 0;
            double newReading = 0;

            // Wall following
            while (!gohome)
            {
                // Go to the wall
                while (!longRangeSensor.againstWall())
                {
                    movement.straight(1);
                    distance += 1;
                    System.Threading.Thread.Sleep(5);
                }

                nodes.Insert(distance, angle, 5);
                distance = 0;

                // While the agent is touching a wall
                while (longRangeSensor.againstWall())
                {
                    movement.spinLeft(1, 1);
                    angle = (angle - 1) % 360;
                    System.Threading.Thread.Sleep(5);
                }

                // start following the wall adjusting the angle
                prevReading = ShortRangeSensor.getDistance();
                while (!longRangeSensor.againstWall())
                {
                    movement.straight(1);
                    distance += 1;
                    newReading = shortRangeSensor.getDistance();

                    double alpha;

                    if (prevReading == -1)
                        alpha = 0;
                    else if (newReading == -1)
                    {
                        alpha = 90;
                    }
                    else
                    {
                        alpha = Math.Atan((newReading - prevReading) / 1) * 180 / Math.PI;
                        if (Math.Abs(alpha) < 5)
                            alpha = 0;
                    }

                    if (alpha != 0)
                    {
                        //no more wall
                        nodes.Insert(distance, angle, 5);
                        distance = 0;
                    }

                    movement.spinRight(1, alpha);
                    angle = (angle + alpha) % 360;

                    prevReading = newReading;

                    System.Threading.Thread.Sleep(5);
                }
            }

            nodes.Insert(distance, angle, 5);
            distance = 0;

            while (nodes.CurrentPosition(distance, angle).Distance(startPoint) > 5)
            {
                // Go home
                // point in direction to the start
                Point A = new Point(0, 0);
                Point C = nodes.CurrentPosition(distance, angle);
                Point Btemp = C + new Point(0, 100);
                Point B = new Segment(C, Btemp).Rotate(angle).End;

                double a_sq = Math.Pow(100, 2);
                double b_sq = A.SquareDistance(C);
                double c_sq = A.SquareDistance(B);

                double gamma;

                gamma = Math.Acos((c_sq - a_sq - b_sq) / (-2 * Math.Sqrt(a_sq) * Math.Sqrt(b_sq))) * 180 / Math.PI;

                if (b_sq > c_sq)
                {
                    gamma = 90 - gamma;
                }

                if (angle < 0)
                    angle = (360 + angle);

                if (angle < 180)
                {
                    movement.spinRight(1, gamma);
                    angle = (angle + gamma) % 360;
                }
                else
                {
                    movement.spinLeft(1, gamma);
                    angle = (angle - gamma) % 360;
                }

                // no wall let's move straight
                while (longRangeSensor.getDistance() == -1)
                {
                    movement.straight(1);
                    distance++;
                    System.Threading.Thread.Sleep(5);
                }

                // A wall is in range
                Point pos = nodes.CurrentPosition(distance, angle);
                Segment sensor = new Segment(pos, new Point(longRangeSensor.getDistance(), 0)).Rotate(angle);
                BDNode near = nodes.Nearest(sensor.End, 1)[0];
                if (near.Next != null && new Segment(near.Coord, near.Next.Coord).Intersects(sensor) != null)
                    ;//MessageBox.Show("intersect");
                else if (near.Previous != null && new Segment(near.Coord, near.Previous.Coord).Intersects(sensor) != null)
                    ;//MessageBox.Show("intersect");
                else
                    ;// MessageBox.Show("unknown wall");

                // move straight until hit the wall
                while (!longRangeSensor.againstWall() && nodes.CurrentPosition(distance, angle).Distance(startPoint) > 5)
                {
                    movement.straight(1);
                    distance++;
                    System.Threading.Thread.Sleep(5);
                }

                nodes.Insert(distance, angle, 5);
                distance = 0;

                // While the agent is touching a wall
                while (longRangeSensor.inRange())
                {
                    movement.spinLeft(1, 1);
                    angle = (angle - 1) % 360;
                    System.Threading.Thread.Sleep(5);
                }
                while (shortRangeSensor.inRange())
                {
                    movement.straight(1);
                    distance++;
                    System.Threading.Thread.Sleep(5);
                }
                nodes.Insert(distance, angle, 5);
                distance = 0;
            }
        }
    }
}
