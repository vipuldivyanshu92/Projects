using System;
using System.IO;
using System.Collections.Generic;
using System.Diagnostics;

namespace AI4_AE1
{
    class Benchmark
    {
        public static void Main()
        {
            List<Segment> seg = new List<Segment>();
            Random rand = new Random();
            Segment vector = new Segment(new Point(rand.Next(), rand.Next()), new Point(rand.Next(), rand.Next()));
            Stopwatch stopwatch = new Stopwatch();


            for (int i = 1; i <= 10000; i = i * 10)
            {
                // create the test set
                seg.Clear();
                for (int j = 0; j < i; j++)
                    seg.Add(new Segment(new Point(rand.Next(), rand.Next()), new Point(rand.Next(), rand.Next())));

                // benchmark
                stopwatch.Start();
                for (int j = 0; j < 100; j++)
                {
                    foreach (Segment s in seg)
                    {
                        vector.Intersects(s);
                    }
                }
                stopwatch.Stop();

                // display
                using (TextWriter fs = new StreamWriter("bench.txt", true))
                {
                    Console.Out.WriteLine("{0} {1}", i, stopwatch.ElapsedMilliseconds / 100);
                }
            }
        }
    }
}
