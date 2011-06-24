using System;
using System.Text.RegularExpressions;

namespace RegExpTP3
{
    class Program
    {
        static void Main(string[] args)
        {
            String f = "44b4B";
            //Regex regex = new Regex("([0-9]*)([xcbBiIlLdDs])");
            Regex regex = new Regex("(?<multiplier>[0-9]*)(?<format>[xcbBiIlLdDs])");
            MatchCollection mc = regex.Matches(f, 0);
            Console.WriteLine(mc.Count);
            foreach(Match m in mc)
            {
                GroupCollection groups = m.Groups;
                Console.WriteLine(groups["multiplier"].Value);
                Console.WriteLine(groups["format"].Value);
            }
            Console.ReadKey();
        }
    }
}
