using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace AI4_AE1
{
    class Movement : IMovement
    {
        private Agent agent;

        public Movement(Agent agent)
        {
            this.agent = agent;
        }

        public void straight(int speed)
        {
            Environment env = Environment.Instance;

            Segment nextPos = new Segment();
            nextPos.Start.X = env.AgentPosition.X;
            nextPos.Start.Y = env.AgentPosition.Y;
            nextPos.End.X = env.AgentPosition.X;
            //nextPos.End.Y = env.AgentPosition.Y + (longDistance > 0 ? Math.Min(longDistance, 1) : 1);
            nextPos.End.Y = env.AgentPosition.Y + 1;
            nextPos = nextPos.Rotate(env.AgentAngle);

            env.AgentPosition = nextPos.End;
        }

        public void spinLeft(int speed, double angle)
        {
            Environment env = Environment.Instance;
            env.AgentAngle -= angle;
        }

        public void spinRight(int speed, double angle)
        {
            Environment env = Environment.Instance;
            env.AgentAngle += angle;
        }
    }
}
