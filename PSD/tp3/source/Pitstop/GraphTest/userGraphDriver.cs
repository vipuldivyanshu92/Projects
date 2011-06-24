using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace GraphTest
{
    class userGraphDriver : IGraphDriver
    {
        private int _value;
        private bool _ready = false;
        public int getNextValue()
        {
            _ready = false;
            return _value;
        }
        public bool hasNextValue()
        {
            return _ready;
        }
        public void setNextValue(int value)
        {
            _value = value;
            _ready = true;
        }
    }
}
