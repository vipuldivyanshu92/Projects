using System;
using System.Collections.Generic;
using System.Windows;

namespace AI4_AE1.Actuators
{
    class Cleaner : ICleaner
    {
        private static Point refPoint = new Point(8, 8);

        public Cleaner()
        {
        }

        public void clean()
        {
            // Retrieve the dirt points from the Environment instance that are under the agent in 16 by 16 square
            // centered on the agent coordinates
            List<BDNode> nodes = Environment.Instance.Dirt.Range(Environment.Instance.AgentPosition - refPoint, Environment.Instance.AgentPosition + refPoint);

            // thread safety
            lock (Environment.Instance.RemovedDirt)
            {
                foreach (BDNode n in nodes)
                {
                    // Check if the dirt density is 0 if true remove the dirt marker else decrease
                    // the density
                    DirtElement elem = (DirtElement)n.Value;
                    elem.count--;
                    if (elem.count == 0)
                    {
                        Environment.Instance.RemovedDirt.Add(elem.element);
                        Environment.Instance.RemovedDirtCount++;
                    }
                }
            }
        }
    }
}
