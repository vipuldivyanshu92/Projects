using System;
using System.Linq;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Collections.ObjectModel;
using System.Runtime.InteropServices;

namespace MobileAgent
{
    static class MobileAgent
    {
        

        
        
        
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [MTAThread]
        static void Main()
        {

            Application.Run(new FrmScan());

        }
    }

}