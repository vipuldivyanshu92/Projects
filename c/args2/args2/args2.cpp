// args2.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"


int _tmain(int argc, _TCHAR* argv[])
{
	FILE *f = fopen("test", "w");
	int i;

	for (i = 0; i < argc; i++)
	{
		fwrite(argv[i], _tcslen(argv[i]) * sizeof(_TCHAR), 1, f);
		fwrite("\n", 1, 1, f);
	}

	fclose(f);

	return 0;
}

