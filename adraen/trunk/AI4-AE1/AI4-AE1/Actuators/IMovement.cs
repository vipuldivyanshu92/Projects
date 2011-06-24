using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace AI4_AE1.Actuators
{
    interface IMovement
    {
        void straight(int speed);

        void spinLeft(int speed, double angle);

        void spinRight(int speed, double angle);
    }
}
