using System;
using System.Linq;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using System.IO;
using System.Xml;
using Microsoft.Win32;
using Microsoft.WindowsMobile.Status;


namespace MobileAgent
{
    public partial class FrmScan : Form
    {


        public FrmScan()
        {
            InitializeComponent();
        }

        public string DeviceIDString;



        private void button1_Click(object sender, EventArgs e)
        {
            /////////////////////////////////////
            // Starting the Scan of the Device //
            /////////////////////////////////////
            
            //First we get a device id , more like a hash key to uniquely identify the Mobile Device.
            // PLease note for security reasons , Windows does not allow mobile devices device Id capture
            //unless the application is marked as truested. We will not implement this at this stage of 
            // the application development. We will do with the retrieved hash key.


            //Let's first produce a title for the scan run
            
            //clear the textarea
            txtBoard.Text = "";
            txtBoard.Text = "TPMX Mobile Agent V0.1 for Windows Mobile\r\n";
            txtBoard.Text += "*****************************************\r\n";
            txtBoard.Text += "\r\n";

            //End producing a title for the scan run
            

            //Get Device ID HASH

            byte[] DeviceID = GetDeviceID("p33krb,wv");
            DeviceIDString = ByteArrayToString(DeviceID);
            txtBoard.Text += "Unique Device ID: " + DeviceIDString + "\r\n";
            txtBoard.Text += "\r\n";

            //End Get Device ID HASH

            //Get device Names (original + current)
            RegistryKey hklm = Registry.LocalMachine;
            RegistryKey IdentK = hklm.OpenSubKey("Ident");
            txtBoard.Text += "Current Name:" + IdentK.GetValue("Name") + "\r\n";
            txtBoard.Text += "Original Name: " + IdentK.GetValue("OrigName") + "\r\n";
            txtBoard.Text += "User Name:" + IdentK.GetValue("Username") + "\r\n";
            txtBoard.Text += "\r\n";
            //End Get Device Names

            //Get OS Information
            txtBoard.Text += "OS Platform: " + Environment.OSVersion.Platform.ToString() + "\r\n";
            txtBoard.Text += "OS Version: " + Environment.OSVersion.Version.ToString() + "\r\n";
            txtBoard.Text += "OS Build: " + Environment.OSVersion.Version.Build.ToString() + "\r\n";
            txtBoard.Text += "OS Revision: " + Environment.OSVersion.Version.Revision.ToString() + "\r\n";
            txtBoard.Text += "OS Major: " + Environment.OSVersion.Version.Major.ToString() + "\r\n";
            txtBoard.Text += "OS Minor: " + Environment.OSVersion.Version.Minor.ToString() + "\r\n";
            txtBoard.Text += "\r\n";

            //EndGet OS Information


            //Get Local time information
            txtBoard.Text += "Time Informations\r\n";
            txtBoard.Text += "==================\r\n";
            txtBoard.Text += "Type:" + DateTime.Now.Kind.ToString() + "\r\n";
            txtBoard.Text += "Date:" + DateTime.Now.Date.ToString("yyyy-MM-dd") + "\r\n";
            txtBoard.Text += "Time:" + DateTime.Now.TimeOfDay.ToString() + "\r\n";
            txtBoard.Text += "Daylight Saving:" + (DateTime.Now.IsDaylightSavingTime() ? "Yes" : "No") + "\r\n";
            txtBoard.Text += "Timezone:" + TimeZone.CurrentTimeZone.DaylightName + "\r\n";
            //Get GMT time information
            txtBoard.Text += "Display UTC Informations\r\n";
            txtBoard.Text += "Type:" + DateTime.UtcNow.Kind.ToString() + "\r\n";
            txtBoard.Text += "Date:" + DateTime.UtcNow.Date.ToString("yyyy-MM-dd") + "\r\n";
            txtBoard.Text += "Time:" + DateTime.UtcNow.TimeOfDay.ToString() + "\r\n";
            txtBoard.Text += "Daylight Saving:" + (DateTime.UtcNow.IsDaylightSavingTime() ? "Yes" : "No") + "\r\n";
            txtBoard.Text += "\r\n";

            //Get Screen Information
            txtBoard.Text += "Display Informations\r\n";
            txtBoard.Text += "===================\r\n";
            Rectangle screen = Screen.PrimaryScreen.Bounds;
            txtBoard.Text += String.Format("Device Resolution: {0} x {1}\r\n", screen.Width, screen.Height);

            // Open a handle on the display device
            IntPtr deviceHandle = Globals.GetDC(IntPtr.Zero);
            if (deviceHandle == IntPtr.Zero)
            {
                // our call to GetDC failed
                txtBoard.Text += "Failed to get an handle on the device\r\n";
            }
            else
            {
                // at this point we can play with GetDeviceCaps
                txtBoard.Text += String.Format("Driver Version: {0}\r\n", Globals.GetDeviceCaps(deviceHandle, Globals.DRIVERVERSION));
                txtBoard.Text += String.Format("Bits Per Pixel: {0}\r\n", Globals.GetDeviceCaps(deviceHandle, Globals.BITSPIXEL));
                txtBoard.Text += String.Format("Colours supported: {0}\r\n", Globals.GetDeviceCaps(deviceHandle, Globals.NUMCOLORS));
                Int32 rasterCplt = Globals.GetDeviceCaps(deviceHandle, Globals.RASTERCAPS);
                txtBoard.Text += String.Format("Raster Capability: {0}\r\n", rasterCplt);
                // bitBliting is required for screen capture
                txtBoard.Text += String.Format("BitBlit: {0}\r\n", (rasterCplt & Globals.RC_BITBLT) == Globals.RC_BITBLT ? "Yes" : "No");

            }
            txtBoard.Text += "\r\n\r\n";



            //Get Memory Information

            MEMORYSTATUS MemoryStatus = new MEMORYSTATUS();
            Globals.GlobalMemoryStatus(ref MemoryStatus);
            txtBoard.Text += "Memory Load: " + String.Format("{0}%", MemoryStatus.dwMemoryLoad) + " \r\n";
            txtBoard.Text += "Total Physical Memory: " + String.Format("{0} kb", MemoryStatus.dwTotalPhys / 1024) + " \r\n";
            txtBoard.Text += "Physical Memory Available: " + String.Format("{0} kb", MemoryStatus.dwAvailPhys / 1024) + " \r\n";
            txtBoard.Text += "Total Page File Size: " + String.Format("{0} kb", MemoryStatus.dwTotalPageFile / 1024) + " \r\n";
            txtBoard.Text += "Available Page File: " + String.Format("{0} kb", MemoryStatus.dwAvailPageFile / 1024) + " \r\n";
            txtBoard.Text += "Total Virtual Memory: " + String.Format("{0} kb", MemoryStatus.dwTotalVirtual / 1024) + " \r\n";
            txtBoard.Text += "Available Virtual Memory: " + String.Format("{0} kb", MemoryStatus.dwAvailPhys / 1024) + " \r\n";
            txtBoard.Text += "\r\n";

            //End Get Memory Information





            //Check if the Device is plugged in the Cradle and Battery Power

            SYSTEM_POWER_STATUS_EX status = new SYSTEM_POWER_STATUS_EX();
            if (Globals.GetSystemPowerStatusEx(status, false) == 1)
            {


                //Check if the Device is plugged in the Cradle
                txtBoard.Text += String.Format("Device plugged in cradle: {0}\r\n", status.ACLineStatus == (byte)1 ? "Yes" : "No");
                //Check if the Device is plugged in the Cradle
                               
                
                // Check the Primary Battery
                
                txtBoard.Text += "\r\n";
                txtBoard.Text = txtBoard.Text + "Battery Life: " + String.Format("{0}%", ((int)status.BatteryLifePercent) / 255 * 100) + " \r\n";
                txtBoard.Text = txtBoard.Text + "Battery Life Time: " + (status.BatteryLifeTime / 60) + " minutes\r\n";
                txtBoard.Text = txtBoard.Text + "Battery Life Time at full charge: " + (status.BatteryFullLifeTime / 60) + " minutes\r\n";


                /*
                    Battery charge status. It can be a combination of the following values:

                    o BATTERY_FLAG_HIGH
                    o BATTERY_FLAG_CRITICAL
                    o BATTERY_FLAG_CHARGING
                    o BATTERY_FLAG_NO_BATTERY
                    o BATTERY_FLAG_UNKNOWN
                    o BATTERY_FLAG_LOW
                */

                string msg;
                switch (status.BatteryFlag)
                {
                    case Globals.BATTERY_FLAG_CHARGING:
                        msg = "Charging";
                        break;
                    case Globals.BATTERY_FLAG_CRITICAL:
                        msg = "Critical";
                        break;
                    case Globals.BATTERY_FLAG_HIGH:
                        msg = "High";
                        break;
                    case Globals.BATTERY_FLAG_LOW:
                        msg = "Low";
                        break;
                    case Globals.BATTERY_FLAG_NO_BATTERY:
                        msg = "No Backup Battery";
                        break;
                    case Globals.BATTERY_FLAG_UNKNOWN:
                        msg = "Status Unknown";
                        break;
                    default:
                        msg = "Status Unknown";
                        break;
                }
                txtBoard.Text += "Battery Status: " + msg + "\r\n";
                if (status.BatteryFlag != Globals.BATTERY_FLAG_UNKNOWN)
                    txtBoard.Text += "Battery Life: " + String.Format("{0}%", ((int)status.BatteryLifePercent) / 255 * 100) + " \r\n";

                ///////////////////////////////////////////////////////////////////////////////////////////////



                // Check the Backup Battery

                txtBoard.Text += "\r\n";
                txtBoard.Text = txtBoard.Text + "Backup Battery Life: " + String.Format("{0}%", ((int)status.BackupBatteryLifePercent) / 255 * 100) + " \r\n";
                txtBoard.Text = txtBoard.Text + "Backup Battery Life Time: " + (status.BackupBatteryLifeTime / 60) + " minutes\r\n";
                txtBoard.Text = txtBoard.Text + "Backup Battery Life Time at full charge: " + (status.BackupBatteryFullLifeTime / 60) + " minutes\r\n";

                switch (status.BackupBatteryFlag)
                {
                    case Globals.BATTERY_FLAG_CHARGING:
                        msg = "Charging";
                        break;
                    case Globals.BATTERY_FLAG_CRITICAL:
                        msg = "Critical";
                        break;
                    case Globals.BATTERY_FLAG_HIGH:
                        msg = "High";
                        break;
                    case Globals.BATTERY_FLAG_LOW:
                        msg = "Low";
                        break;
                    case Globals.BATTERY_FLAG_NO_BATTERY:
                        msg = "No Backup Battery";
                        break;
                    case Globals.BATTERY_FLAG_UNKNOWN:
                        msg = "Status Unknown";
                        break;
                    default:
                        msg = "Status Unknown";
                        break;
                }
                txtBoard.Text += "Battery Status: " + msg + "\r\n";
                if (status.BackupBatteryFlag != Globals.BATTERY_FLAG_UNKNOWN)
                    txtBoard.Text += "Backup Battery Life: " + String.Format("{0}%", (int)status.BackupBatteryLifePercent) + " \r\n";

                //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            }
            
            // Get the Processor information 

            SYSTEM_INFO si;
            Globals.GetSystemInfo(out si);
            txtBoard.Text += "\r\n";
            txtBoard.Text += "Number of Processors: " + si.numberOfProcessors + "\r\n";
            
            switch (si.processorArchitecture)
            {
                case Globals.PROCESSOR_ARCHITECTURE_ALPHA  : 
                    txtBoard.Text += "Processor Architecture: ALPHA\r\n";
                    break;
                case Globals.PROCESSOR_ARCHITECTURE_INTEL  : 
                    txtBoard.Text += "Processor Architecture: INTEL\r\n";
                    break;
                case Globals.PROCESSOR_ARCHITECTURE_MIPS  : 
                    txtBoard.Text += "Processor Architecture: MIPS\r\n";
                    break;
                case Globals.PROCESSOR_ARCHITECTURE_PPC  : 
                    txtBoard.Text += "Processor Architecture: PPC\r\n";
                    break;
                case Globals.PROCESSOR_ARCHITECTURE_UNKNOWN  : 
                    txtBoard.Text += "Processor Architecture: Uknown\r\n";
                    break;
                case Globals.PROCESSOR_ARCHITECTURE_ALPHA64:
                    txtBoard.Text += "Processor Architecture: ALPHA64\r\n";
                    break;
                case Globals.PROCESSOR_ARCHITECTURE_AMD64:
                    txtBoard.Text += "Processor Architecture: AMD64\r\n";
                    break;
                case Globals.PROCESSOR_ARCHITECTURE_ARM:
                    txtBoard.Text += "Processor Architecture: ARM\r\n";
                    break;
                case Globals.PROCESSOR_ARCHITECTURE_IA32_ON_WIN64:
                    txtBoard.Text += "Processor Architecture: IA32 on WIN64\r\n";
                    break;
                case Globals.PROCESSOR_ARCHITECTURE_IA64:
                    txtBoard.Text += "Processor Architecture: IA64\r\n";
                    break;
                case Globals.PROCESSOR_ARCHITECTURE_MSIL:
                    txtBoard.Text += "Processor Architecture: MSIL\r\n";
                    break;
                case Globals.PROCESSOR_ARCHITECTURE_SHX:
                    txtBoard.Text += "Processor Architecture: MSIL\r\n";
                    break;                   
                default:
                    txtBoard.Text += "Processor Architecture: Unidentified\r\n";
                    break;
            }
                
            
            
            if (si.processorType == 2577) 
                txtBoard.Text += "Processor Type: " + si.processorType + " ARM\r\n";
            
            else if (si.processorType == 686) 
                txtBoard.Text += "Processor Type: " + si.processorType + " Intel\r\n";
            
            else txtBoard.Text += "Processor Type: " + si.processorType + "\r\n";

            txtBoard.Text += "Processor Level: " + si.processorLevel + "\r\n";
            txtBoard.Text += "Processor Revision: " + si.processorRevision + "\r\n";

            txtBoard.Text += "\r\n";



            // Get the Installed Applications
            txtBoard.Text += "Installed Applications\r\n";
            txtBoard.Text += "======================\r\n";
            txtBoard.Text += "\r\n";

            string[] listDirectories;
            listDirectories = Directory.GetDirectories("Windows\\AppMgr", "*");
            for (int i = 0; i < listDirectories.Length; ++i)
            {
                txtBoard.Text +=  listDirectories[i] + "\r\n";
            }

            txtBoard.Text += "\r\n";

            //Get the Installed Services
            txtBoard.Text += "Installed Services\r\n";
            txtBoard.Text += "==================\r\n\r\n";

            // Open HKLM//Services
            RegistryKey servicesK = hklm.OpenSubKey("Services");
            foreach (string subkey in servicesK.GetSubKeyNames())
            {
                //Try to retrieve the name from FriendlyName, DisplayName or just use the name of the key
                RegistryKey serviceK = servicesK.OpenSubKey(subkey);
                Object name;

                name = serviceK.GetValue("FriendlyName");
                if (name == null)
                {
                    name = serviceK.GetValue("DisplayName");
                    if (name == null)
                        name = subkey;
                }

                txtBoard.Text += name + "\r\n";
            }

            txtBoard.Text += "\r\n\r\n";

            //Get the Disk Space
            txtBoard.Text += "Disk space\r\n";
            txtBoard.Text += "======================\r\n";
            txtBoard.Text += "\r\n";

            ulong FreeBytesAvailable;
            ulong TotalNumberOfBytes;
            ulong TotalNumberOfFreeBytes;

            bool success = Globals.GetDiskFreeSpaceEx("C:\\", out FreeBytesAvailable, out TotalNumberOfBytes,
                               out TotalNumberOfFreeBytes);
            if (!success)
                throw new System.ComponentModel.Win32Exception();

            txtBoard.Text +="Free Bytes Available:" + String.Format("{0,15:D}", FreeBytesAvailable) + "\r\n";
            txtBoard.Text += "Total Number Of Bytes:" + String.Format("{0,15:D}", TotalNumberOfBytes) + "\r\n";
            txtBoard.Text += "Total Number Of FreeBytes:" + String.Format("{0,15:D}", TotalNumberOfFreeBytes) + "\r\n";
            txtBoard.Text += "\r\n";

            //WriteToFile("\\My Documents","scan.xml",Encoding.UTF8);

            // Get System State
            txtBoard.Text += "System Status\r\n";
            txtBoard.Text += "======================\r\n";
            txtBoard.Text += String.Format("ActiveSync Status: {0}\r\n", SystemState.ActiveSyncStatus.ToString());
            txtBoard.Text += String.Format("Camera Present: {0}\r\n", SystemState.CameraPresent.ToString());
            //txtBoard.Text += String.Format("Owner Name: {0}\r\n", SystemState.OwnerName);
            //txtBoard.Text += String.Format("Owner Phone Number: {0}\r\n", SystemState.OwnerPhoneNumber); 
            txtBoard.Text += String.Format("Active BlueTooth Connections: {0}\r\n", SystemState.ConnectionsBluetoothCount.ToString());

        }




        private byte[] GetDeviceID(string AppString)
        {
            // Call the GetDeviceUniqueID
            byte[] AppData = Encoding.Unicode.GetBytes(AppString);
            int appDataSize = AppData.Length;
            byte[] DeviceOutput = new byte[20];
            uint SizeOut = 20;
            Globals.GetDeviceUniqueID(AppData, appDataSize, 1, DeviceOutput, out SizeOut);
            return DeviceOutput;
        }

        public static string ByteArrayToString(byte[] ba)
        {
            StringBuilder hex = new StringBuilder(ba.Length * 2);
            foreach (byte b in ba)
                hex.AppendFormat("{0:x2}", b);
            return hex.ToString();
        }

        public void WriteToFile(string strDirName, string strXMLFileName, Encoding encodeFile)
        {
            // Ensure the directory and file exist.
            if (!Directory.Exists(strDirName))
            {
                Directory.CreateDirectory(strDirName);
            }

            Directory.SetCurrentDirectory(strDirName);

            if (!File.Exists(strXMLFileName))
            {
                File.Create(strDirName +"\\"+strXMLFileName).Close();
            }
            
            // Create the XmlTextWriter.
            XmlTextWriter writer =
            new XmlTextWriter((strDirName + "\\" + strXMLFileName), encodeFile);
            // Set indentation.
            writer.Formatting = Formatting.Indented;
            writer.Indentation = 3;

            writer.WriteStartDocument();
                writer.WriteStartElement("GATHERED_DATA");
                   writer.WriteElementString("GATHERER_VERSION", "Mobile 0.1");
 
                   writer.WriteStartElement("SECTION");
                       writer.WriteStartAttribute("ID"); //Attribute "Name"
                       writer.WriteString("SYSTEM SUMMARY"); //Attribute Value 
                       writer.WriteEndAttribute();


                       writer.WriteStartElement("TABLE");
                            writer.WriteStartAttribute("ID"); //Attribute "Name"
                                    writer.WriteString("System Summary"); //Attribute Value 
                            writer.WriteEndAttribute();

                            writer.WriteStartElement("ROW");
                            writer.WriteStartAttribute("ID"); //Attribute "Name"
                                    writer.WriteString(""); //Attribute Value 
                            writer.WriteEndAttribute();

                            writer.WriteStartElement("ASC");
                            writer.WriteAttributeString("ID", "Computer Name"); //Attribute "Name"
                                writer.WriteValue(DeviceIDString);
                            writer.WriteEndElement();

                            writer.WriteStartElement("ASC");
                            writer.WriteAttributeString("ID", "System Vendor"); //Attribute "Name"
                                //writer.WriteValue("");
                            writer.WriteEndElement();

                            writer.WriteStartElement("ASC");
                            writer.WriteAttributeString("ID", "System Model"); //Attribute "Name"
                                //writer.WriteValue("");
                            writer.WriteEndElement();

                            writer.WriteStartElement("ASC");
                            writer.WriteAttributeString("ID", "System Serial Number"); //Attribute "Name"
                                writer.WriteValue(DeviceIDString);
                            writer.WriteEndElement();

                            writer.WriteStartElement("ASC");
                            writer.WriteAttributeString("ID", "BIOS Version"); //Attribute "Name"
                                //writer.WriteValue("");
                            writer.WriteEndElement();

                            writer.WriteStartElement("ASC");
                            writer.WriteAttributeString("ID", "Current User"); //Attribute "Name"
                                writer.WriteValue("");
                            writer.WriteEndElement();
                            
                            writer.WriteStartElement("ASC");
                            writer.WriteAttributeString("ID", "UUID"); //Attribute "Name"
                                    writer.WriteValue(DeviceIDString);
                            writer.WriteEndElement();
                            
                            writer.WriteStartElement("ASC");
                            writer.WriteAttributeString("ID", "GUID"); //Attribute "Name"
                                    writer.WriteValue(DeviceIDString);
                            writer.WriteEndElement();

                       writer.WriteEndElement();






                       writer.WriteStartElement("TABLE");
                           writer.WriteStartAttribute("ID"); //Attribute "Name"
                           writer.WriteString("Operating System"); //Attribute Value 
                           writer.WriteEndAttribute();

                           writer.WriteStartElement("ROW");
                               writer.WriteStartAttribute("ID"); //Attribute "Name"
                               writer.WriteString(""); //Attribute Value 
                               writer.WriteEndAttribute();

                               writer.WriteStartElement("ASC");
                                   writer.WriteAttributeString("ID", "VENDOR"); //Attribute "Name"
                                   writer.WriteValue("Microsoft Corporation");
                               writer.WriteEndElement();
                               
                               writer.WriteStartElement("ASC");
                                   writer.WriteAttributeString("ID", "NAME"); //Attribute "Name"
                                   writer.WriteValue(Environment.OSVersion.Platform.ToString());
                               writer.WriteEndElement();

                               writer.WriteStartElement("ASC");
                                    writer.WriteAttributeString("ID", "VERSION"); //Attribute "Name"
                                    writer.WriteValue(Environment.OSVersion.Version.ToString());
                               writer.WriteEndElement();

                               writer.WriteStartElement("ASC");
                                    writer.WriteAttributeString("ID", "BUILD"); //Attribute "Name"
                                    writer.WriteValue(Environment.OSVersion.Version.Build.ToString());
                               writer.WriteEndElement();

                               writer.WriteStartElement("ASC");
                                    writer.WriteAttributeString("ID", "SERVICE LEVEL"); //Attribute "Name"
                                    writer.WriteValue(Environment.OSVersion.Version.Revision.ToString());
                               writer.WriteEndElement();

                               writer.WriteStartElement("ASC");
                                    writer.WriteAttributeString("ID", "OS"); //Attribute "Name"
                                    writer.WriteValue(Environment.OSVersion.Version.Major.ToString());
                               writer.WriteEndElement();
            
                           writer.WriteEndElement();
                       
                       writer.WriteEndElement(); 
                                       
                    writer.WriteEndElement();
                
            writer.WriteEndElement();
            
            writer.WriteEndDocument();
            writer.Flush();
            writer.Close();

            


        }



    }

   

}