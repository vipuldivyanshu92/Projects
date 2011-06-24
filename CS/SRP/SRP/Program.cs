using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Numerics;

namespace SRPtest
{
    class Program
    {
        static byte[] reverse(byte[] a)
        {
            byte[] r = new byte[a.Length];
            for (int i = 0, len = a.Length - 1; i < a.Length; i++, len--)
                r[len] = a[i];
            return r;
        }

        static void Main(string[] args)
        {
            // Socket connection
            RealmClient client = new RealmClient("NECROALBERT", "N3YL9RL5WOW");
            client.Connect("www.avalonserver.org", 3724);

            Console.ReadKey();
        }
    }
}
