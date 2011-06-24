using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace GraphTest
{
    interface IGraph 
    {
    //    IGraph(Object Parent, int max, int min);
        IGraphDriver Driver
        {
            get;
            set;
        }
        bool GraphEnabled
        {
            get;
            set;
        }
        int RefreshRate
        {
            get;
            set;
        }
        string TitleX
        {
            get;
            set;
        }
        string TitleY
        {
            get;
            set;
        }
        int MaximumY
        {
            get; 
            set;
        }
        int MinimumY
        {
            get;
            set;
        }
    }
}
