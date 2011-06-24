from win32con import TOKEN_ADJUST_PRIVILEGES, TOKEN_QUERY, SE_PRIVILEGE_ENABLED, PROCESS_VM_READ
from win32api import GetCurrentProcess, CloseHandle, OpenProcess
from win32gui import FindWindow
from win32security import OpenProcessToken, LookupPrivilegeValue, AdjustTokenPrivileges, SE_DEBUG_NAME
from win32process import GetWindowThreadProcessId
from ctypes import c_ulong, c_long, c_ubyte, byref, windll
import sys
import array
import socket

# Get the ReadProcessMemory function
ReadProcessMemory = windll.kernel32.ReadProcessMemory

# Constants
CONNECTION_PTR_OFFSET = 0x01139F94
SESSIONKEY_OFFSET = 0x508
SESSIONKEY_LENGTH = 40

# Adjust current process privileges
hToken = OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY)
luid = LookupPrivilegeValue(None, SE_DEBUG_NAME)
AdjustTokenPrivileges(hToken, False, [(luid, SE_PRIVILEGE_ENABLED)])
CloseHandle(hToken)

# Get an handle on wow
windowHandle = FindWindow(None, 'World of Warcraft')
if not windowHandle:
    print('ERROR : Unable to find WoW window')
    sys.exit(0)
    
threadID, processID = GetWindowThreadProcessId(windowHandle)
wowHandle = OpenProcess(PROCESS_VM_READ, False, processID)

# Get a pointer to the sessionkey
lpBuffer = c_ulong()
nSize = 4
lpNumberOfBytesRead = c_long(0)
if not ReadProcessMemory(wowHandle.handle, CONNECTION_PTR_OFFSET, byref(lpBuffer), 4, byref(lpNumberOfBytesRead)):
    print('ERROR : Unable to get the sessionkey pointer')
    sys.exit(0)

# Retrieve the sessionkey
sessionkey = (c_ubyte * 40)()
lpNumberOfBytesRead = c_long(0)
if not ReadProcessMemory(wowHandle.handle, SESSIONKEY_OFFSET+lpBuffer.value, byref(sessionkey), SESSIONKEY_LENGTH, byref(lpNumberOfBytesRead)):
    print('ERROR : Unable to get the sessionkey')
    sys.exit(0)

CloseHandle(wowHandle)

# Check the sessionkey
sk = array.array('B', sessionkey)
if sk.count(0) == SESSIONKEY_LENGTH:
    print('ERROR : Invalid sessionkey')
    sys.exit(0)

# Send the datas
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))
s.send('%s' % sk.tostring().encode('hex'))
s.close()
