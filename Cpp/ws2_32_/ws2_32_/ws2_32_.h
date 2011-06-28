// The following ifdef block is the standard way of creating macros which make exporting 
// from a DLL simpler. All files within this DLL are compiled with the WS2_32__EXPORTS
// symbol defined on the command line. This symbol should not be defined on any project
// that uses this DLL. This way any other project whose source files include this file see 
// WS2_32__API functions as being imported from a DLL, whereas this DLL sees symbols
// defined with this macro as being exported.
#ifdef WS2_32__EXPORTS
#define WS2_32__API __declspec(dllexport)
#else
#define WS2_32__API __declspec(dllimport)
#endif

// This class is exported from the ws2_32_.dll
class WS2_32__API Cws2_32_ {
public:
	Cws2_32_(void);
	// TODO: add your methods here.
};

extern WS2_32__API int nws2_32_;

WS2_32__API int fnws2_32_(void);
