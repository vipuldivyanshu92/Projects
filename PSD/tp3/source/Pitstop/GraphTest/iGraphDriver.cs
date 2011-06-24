using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace GraphTest
{
    public interface IGraphDriver
    {
         int getNextValue();
         bool hasNextValue();
         void setNextValue(int NextVal);
    }
}
