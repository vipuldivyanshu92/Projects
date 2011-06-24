using System;
using System.Linq;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
using System.Windows;
using AI4_AE1.Sensors;
using AI4_AE1.Actuators;

namespace AI4_AE1
{
    class Agent
    {
        private ProximitySensor shortRangeSensor;
        private Bumper bumperSensor;
        private Movement movement;
        private Cleaner cleaner;
        private Random random;

        public ProximitySensor ShortRangeSensor
        {
            get { return shortRangeSensor; }
        }

        public Bumper BumperSensor
        {
            get { return bumperSensor; }
        }

        public Agent()
        {
            // create the short range sensor for wall following
            shortRangeSensor = new ProximitySensor(10, 10, 90);

            // Create the bumper sensor
            bumperSensor = new Bumper(12, 130);

            // create the movement interface
            movement = new Movement();

            // create the cleaning module
            cleaner = new Cleaner();

            random = new Random();
        }

        enum EState
        {
            NONE,
            RANDOM,
            WALLFOLLOWING
        }

        public void run()
        {
            // prev and new reading store short range sensor distances
            double prevReading = 0;
            double newReading = 0;

            // State of the agent
            EState state = EState.NONE;

            // Stopwatch to measure the amount of time spent in each mode
            Stopwatch stopwatch = new Stopwatch();
            long randomTime = 0;
            long wallTime = 0;

            // Agent loop
            while (true)
            {
                // find what to do
                
                //if (wallTime > randomTime)
                 //   state = EState.RANDOM;
                //else
                    state = EState.WALLFOLLOWING;
                //state = EState.RANDOM;

                // do it
                stopwatch.Start();
                if (state == EState.RANDOM)
                {
                    while (bumperSensor.collide())
                    {
                        // spin left
                        movement.spinLeft(45, random.Next(0, 360));
                        cleaner.clean();
                    }

                    while (!bumperSensor.collide())
                    {
                        // move straight at 10cm/s
                        movement.straight(10);
                        cleaner.clean();
                    }
                }

                else if (state == EState.WALLFOLLOWING)
                {
                    // while against a wall turn left
                    while (bumperSensor.collide())
                    {
                        movement.spinLeft(45, 1);
                        cleaner.clean();
                    }

                    // start following the wall adjusting the angle
                    prevReading = ShortRangeSensor.getDistance();
                    movement.spinLeft(45, 1);
                    while (!bumperSensor.collide())
                    {
                        double alpha;

                        movement.straight(10);
                        cleaner.clean();
                        newReading = shortRangeSensor.getDistance();

                        // if no previous reading do not modify the angle
                        if (prevReading == -1)
                            alpha = 0;
                        // if we are not against a wall anymore do a 90 degree turn
                        // to look for the wall
                        else if (newReading == -1)
                        {
                            for (int i = 0; i < 10; i++)
                            {
                                if (bumperSensor.collide())
                                    break;
                                movement.straight(10);
                                cleaner.clean();
                            }
                            alpha = 90;
                        }
                        // if we got the previous and current reading calculate the inverse tangent
                        // of the angle that would put the agent in the right angle
                        else
                            alpha = Math.Atan((newReading - prevReading) / 1) * 180 / Math.PI;

                        movement.spinRight(45, alpha);
                        cleaner.clean();

                        prevReading = newReading;
                    }
                }
                stopwatch.Stop();

                // allocate the time spent
                if (state == EState.WALLFOLLOWING)
                    wallTime += stopwatch.ElapsedTicks;
                else
                    randomTime += stopwatch.ElapsedTicks;
            }
        }
    }
}
