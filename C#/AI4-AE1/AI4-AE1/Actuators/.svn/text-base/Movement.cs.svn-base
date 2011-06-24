using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace AI4_AE1.Actuators
{
    class Movement : IMovement
    {
        public Movement()
        {
        }

        public void straight(int speed)
        {
            // Retrieve the environment singleton
            Environment env = Environment.Instance;

            // Calculate the next position
            Segment nextPos = new Segment();
            nextPos.Start.X = env.AgentPosition.X;
            nextPos.Start.Y = env.AgentPosition.Y;
            nextPos.End.X = env.AgentPosition.X;
            nextPos.End.Y = env.AgentPosition.Y + 1;
            nextPos = nextPos.Rotate(env.AgentAngle);

            env.AgentPosition = nextPos.End;

            // Sleep to give the speed limitation behaviour
            if (env.SimulationSpeed != 0)
                System.Threading.Thread.Sleep((int)(1000 / (speed * env.SimulationSpeed)));
        }

        public void spinLeft(int speed, double angle)
        {
            Environment env = Environment.Instance;

            for (int i = 0; i < Math.Abs(angle); i++)
            {
                if (angle < 0)
                    env.AgentAngle += 1;
                else
                    env.AgentAngle -= 1;

                // Sleep to give the speed limitation behaviour
                if (env.SimulationSpeed != 0)
                    System.Threading.Thread.Sleep(((int)((1 * 1000) / (speed * env.SimulationSpeed))));
            }
        }

        public void spinRight(int speed, double angle)
        {
            Environment env = Environment.Instance;

            for (int i = 0; i < Math.Abs(angle); i++)
            {
                if (angle > 0)
                    env.AgentAngle += 1;
                else
                    env.AgentAngle -= 1;

                // Sleep to give the speed limitation behaviour
                if (env.SimulationSpeed != 0)
                    System.Threading.Thread.Sleep(((int)((1 * 1000) / (speed * env.SimulationSpeed))));
            }
        }
    }
}
