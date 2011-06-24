using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace args
{
    class Program
    {
        static void Main(string[] args)
        {
            foreach (string s in args)
                Console.Out.WriteLine(s);

            Console.ReadKey();
        }
    }
}
