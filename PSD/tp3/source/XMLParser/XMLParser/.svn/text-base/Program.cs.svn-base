using System;
using System.Collections.Generic;
using System.Text;
using System.Xml.Serialization;

namespace XMLParser
{
    class Program
    {
        static void Main(string[] args)
        {
            System.IO.StreamReader str = new System.IO.StreamReader("test.xml");
            XmlSerializer xSerializer = new XmlSerializer(typeof(module));
            module m = (module)xSerializer.Deserialize(str);
            str.Close();

            Console.WriteLine(m.name);
            
            Console.ReadLine();
        }
    }
}
