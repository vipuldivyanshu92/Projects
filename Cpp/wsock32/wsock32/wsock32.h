// The following ifdef block is the standard way of creating macros which make exporting 
// from a DLL simpler. All files within this DLL are compiled with the WSOCK32_EXPORTS
// symbol defined on the command line. This symbol should not be defined on any project
// that uses this DLL. This way any other project whose source files include this file see 
// WSOCK32_API functions as being imported from a DLL, whereas this DLL sees symbols
// defined with this macro as being exported.
#ifdef WSOCK32_EXPORTS
#define WSOCK32_API __declspec(dllexport)
#else
#define WSOCK32_API __declspec(dllimport)
#endif

// This class is exported from the wsock32.dll
class WSOCK32_API Cwsock32 {
public:
	Cwsock32(void);
	// TODO: add your methods here.
};

extern WSOCK32_API int nwsock32;

WSOCK32_API int fnwsock32(void);
