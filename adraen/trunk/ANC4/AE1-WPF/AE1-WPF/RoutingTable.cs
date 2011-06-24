using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace AE1_WPF
{
    public class RoutingTable
    {
        private Dictionary<NodeUI, RoutingTuple> routingTable = new Dictionary<NodeUI, RoutingTuple>();

        public class RoutingTuple
        {
            public NodeUI Destination { get; set; }
            public int Distance { get; set; }
            public LinkUI Link { get; set; }

            public RoutingTuple(NodeUI dest, int dist, LinkUI l)
            {
                Destination = dest;
                Distance = dist;
                Link = l;
            }
        }

        public void addRoutingEntry(NodeUI dest, int distance, LinkUI link)
        {
            routingTable.Add(dest, new RoutingTuple(dest, distance, link));
        }

        public List<RoutingTuple> displayRoutingTable()
        {
            return routingTable.Values.ToList<RoutingTuple>();
        }

        public void update(NodeUI sender, RoutingTable table)
        {
            foreach (RoutingTuple offeredTuple in table.routingTable.Values)
            {
                if (offeredTuple.Destination == sender)
                    continue;

                int distanceOffered = routingTable[sender].Distance + offeredTuple.Distance;
                if (routingTable.ContainsKey(offeredTuple.Destination))
                {
                    if (routingTable[offeredTuple.Destination].Distance > distanceOffered)
                    {
                        routingTable[offeredTuple.Destination].Distance = distanceOffered;
                        routingTable[offeredTuple.Destination].Link = routingTable[sender].Link;
                    }
                }
                else
                {
                    routingTable.Add(offeredTuple.Destination, new RoutingTuple(
                            offeredTuple.Destination,
                            distanceOffered,
                            routingTable[sender].Link
                        )
                    );
                }
            }
        }
    }
}
