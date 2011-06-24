using System;
using System.Linq;
using System.Collections.Generic;
using System.Text;
using System.Runtime.InteropServices;

namespace MobileAgent
{
    public class Globals
    {
        // Declarations
        [DllImport("coredll")]
        public static extern uint GetSystemPowerStatusEx(SYSTEM_POWER_STATUS_EX lpSystemPowerStatus, bool fUpdate);

        [DllImport("coredll", SetLastError = true)]
        public static extern void GetSystemInfo(out SYSTEM_INFO pSi);

        [DllImport("coredll")]
        private static extern uint GetSystemPowerStatusEx2(SYSTEM_POWER_STATUS_EX2 lpSystemPowerStatus,
            uint dwLen, bool fUpdate);

        [DllImport("coredll.dll")]
        public extern static int GetDeviceUniqueID([In, Out] byte[] appdata, int cbApplictionData, int dwDeviceIDVersion,
            [In, Out] byte[] deviceIDOuput, out uint pcbDeviceIDOutput);

        [DllImport("coredll.dll", SetLastError = true)]
        public static extern void GlobalMemoryStatus(ref MEMORYSTATUS lpBuffer);

        [DllImport("coredll.dll", SetLastError = true, CharSet = CharSet.Auto)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool GetDiskFreeSpaceEx(string lpDirectoryName, out ulong lpFreeBytesAvailable,
        out ulong lpTotalNumberOfBytes, out ulong lpTotalNumberOfFreeBytes);

        [DllImport("coredll.dll", SetLastError = true)]
        public extern static IntPtr GetDC(IntPtr hwnd);

        [DllImport("coredll.dll", SetLastError = true)]
        public extern static Int32 ReleaseDC(IntPtr hwnd, IntPtr hdc);

        [DllImport("coredll.dll", SetLastError = true)]
        public extern static Int32 GetDeviceCaps(IntPtr hdc, Int32 index);

        

        // battery flags

        public const byte BATTERY_FLAG_HIGH = 0x01;
        public const byte BATTERY_FLAG_LOW = 0x02;
        public const byte BATTERY_FLAG_CRITICAL = 0x04;
        public const byte BATTERY_FLAG_CHARGING = 0x08;
        public const byte BATTERY_FLAG_NO_BATTERY = 0x80;
        public const byte BATTERY_FLAG_UNKNOWN = 0xFF;
        public const byte BATTERY_PERCENTAGE_UNKNOWN = 0xFF;
        public const uint BATTERY_LIFE_UNKNOWN = 0xFFFFFFFF;

        // processor architectures
       
        public const ushort PROCESSOR_ARCHITECTURE_INTEL = 0;
        public const ushort PROCESSOR_ARCHITECTURE_MIPS = 1;       
        public const ushort PROCESSOR_ARCHITECTURE_ALPHA = 2;
        public const ushort PROCESSOR_ARCHITECTURE_PPC = 3;
        public const ushort PROCESSOR_ARCHITECTURE_SHX = 4;
        public const ushort PROCESSOR_ARCHITECTURE_ARM = 5;
        public const ushort PROCESSOR_ARCHITECTURE_IA64 = 6;
        public const ushort PROCESSOR_ARCHITECTURE_ALPHA64 = 7;
        public const ushort PROCESSOR_ARCHITECTURE_MSIL = 8;
        public const ushort PROCESSOR_ARCHITECTURE_AMD64 = 9;
        public const ushort PROCESSOR_ARCHITECTURE_IA32_ON_WIN64 = 10;
        public const ushort PROCESSOR_ARCHITECTURE_UNKNOWN = 0xFFFF;
        
        
        public const ushort PROCESSOR_INTEL_386 = 386;
        public const ushort PROCESSOR_INTEL_486 = 486;
        public const ushort PROCESSOR_INTEL_PENTIUM = 586;
        public const ushort PROCESSOR_INTEL_PENTIUM2 = 686;
        public const ushort PROCESSOR_INTEL_PENTIUM3 = 786;
        public const ushort PROCESSOR_MIPS_R4000 = 4000;
        public const ushort PROCESSOR_ARM = 2577;
        public const ushort VER_PLATFORM_WIN32_NT = 2;
        public const ushort VER_PLATFORM_WIN32_WINDOWS = 1;

        /* Device Parameters for GetDeviceCaps() */
        /* Extracted from wingdi.h */
        public const Int32 DRIVERVERSION = 0;     /* Device driver version                    */
        public const Int32 TECHNOLOGY    = 2;     /* Device classification                    */
        public const Int32 HORZSIZE      = 4;     /* Horizontal size in millimeters           */
        public const Int32 VERTSIZE      = 6;     /* Vertical size in millimeters             */
        public const Int32 HORZRES       = 8;     /* Horizontal width in pixels               */
        public const Int32 VERTRES       = 10;    /* Vertical height in pixels                */
        public const Int32 BITSPIXEL     = 12;    /* Number of bits per pixel                 */
        public const Int32 PLANES        = 14;    /* Number of planes                         */
        public const Int32 NUMBRUSHES    = 16;    /* Number of brushes the device has         */
        public const Int32 NUMPENS       = 18;    /* Number of pens the device has            */
        public const Int32 NUMMARKERS    = 20;    /* Number of markers the device has         */
        public const Int32 NUMFONTS      = 22;    /* Number of fonts the device has           */
        public const Int32 NUMCOLORS     = 24;    /* Number of colors the device supports     */
        public const Int32 PDEVICESIZE   = 26;    /* Size required for device descriptor      */
        public const Int32 CURVECAPS     = 28;    /* Curve capabilities                       */
        public const Int32 LINECAPS      = 30;    /* Line capabilities                        */
        public const Int32 POLYGONALCAPS = 32;    /* Polygonal capabilities                   */
        public const Int32 TEXTCAPS      = 34;    /* Text capabilities                        */
        public const Int32 CLIPCAPS      = 36;    /* Clipping capabilities                    */
        public const Int32 RASTERCAPS    = 38;    /* Bitblt capabilities                      */
        public const Int32 ASPECTX       = 40;    /* Length of the X leg                      */
        public const Int32 ASPECTY       = 42;    /* Length of the Y leg                      */
        public const Int32 ASPECTXY      = 44;    /* Length of the hypotenuse                 */

        /* Raster capabilities of the display device */
        public const Int32 RC_BITBLT = 1;         /* Can do standard BLT.             */
        /* ... more in wingdi.h */



    }

    
    public class SYSTEM_POWER_STATUS_EX
    {
        public byte ACLineStatus;
        public byte BatteryFlag;
        public byte BatteryLifePercent;
        public byte Reserved1;
        public uint BatteryLifeTime;
        public uint BatteryFullLifeTime;
        public byte Reserved2;
        public byte BackupBatteryFlag;
        public byte BackupBatteryLifePercent;
        public byte Reserved3;
        public uint BackupBatteryLifeTime;
        public uint BackupBatteryFullLifeTime;

    }



    public class SYSTEM_POWER_STATUS_EX2
    {
        public byte ACLineStatus;
        public byte BatteryFlag;
        public byte BatteryLifePercent;
        public byte Reserved1;
        public uint BatteryLifeTime;
        public uint BatteryFullLifeTime;
        public byte Reserved2;
        public byte BackupBatteryFlag;
        public byte BackupBatteryLifePercent;
        public byte Reserved3;
        public uint BackupBatteryLifeTime;
        public uint BackupBatteryFullLifeTime;
        public uint BatteryVoltage;
        public uint BatteryCurrent;
        public uint BatteryAverageCurrent;
        public uint BatteryAverageInterval;
        public uint BatterymAHourConsumed;
        public uint BatteryTemperature;
        public uint BackupBatteryVoltage;
        public byte BatteryChemistry;
    }




    public enum DevicePowerState : int
    {

        Unspecified = -1,
        D0 = 0, // Full On: full power, full functionality
        D1, // Low Power On: fully functional at low power/performance
        D2, // Standby: partially powered with automatic wake
        D3, // Sleep: partially powered with device initiated wake
        D4, // Off: unpowered
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct SYSTEM_INFO
    {
        public ushort processorArchitecture;
        ushort reserved;
        public uint pageSize;
        public IntPtr minimumApplicationAddress;
        public IntPtr maximumApplicationAddress;
        public IntPtr activeProcessorMask;
        public uint numberOfProcessors;
        public uint processorType;
        public uint allocationGranularity;
        public ushort processorLevel;
        public ushort processorRevision;
    }
   
    
    
    [StructLayout(LayoutKind.Sequential)]
    public struct MEMORYSTATUS
    {
        /// <summary>
        /// Size of the MEMORYSTATUS data structure, in bytes. You do not need to set this member before calling the GlobalMemoryStatus function; the function sets it. 
        /// </summary>
        public uint dwLength;

        /// <summary>
        /// Number between 0 and 100 that specifies the approximate percentage of physical memory that is in use (0 indicates no memory use and 100 indicates full memory use). 
        /// Windows NT:  Percentage of approximately the last 1000 pages of physical memory that is in use.
        /// </summary>
        public uint dwMemoryLoad;

        /// <summary>
        /// Total size of physical memory, in bytes. 
        /// </summary>
        public uint dwTotalPhys;

        /// <summary>
        /// Size of physical memory available, in bytes
        /// </summary>
        public uint dwAvailPhys;

        /// <summary>
        /// Size of the committed memory limit, in bytes. 
        /// </summary>
        public uint dwTotalPageFile;

        /// <summary>
        /// Size of available memory to commit, in bytes. 
        /// </summary>
        public uint dwAvailPageFile;

        /// <summary>
        /// Total size of the user mode portion of the virtual address space of the calling process, in bytes. 
        /// </summary>
        public uint dwTotalVirtual;

        /// <summary>
        /// Size of unreserved and uncommitted memory in the user mode portion of the virtual address space of the calling process, in bytes. 
        /// </summary>
        public uint dwAvailVirtual;

    } // class MEMORYSTATUS




}
