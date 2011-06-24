AoC Update Server v. 0.1

Run this to trick the AoC client into thinking it's been updated.
Please be careful you've extracted all the files before running it.

NOTE: LocalConfig.xml will be updated once you connect to the official gameserver, so
      you have to change it again to use this program. First thing someone should do if
      creating a gameserver is to make sure that a patched LocalConfig.xml is sent to client.

I take no credit for this code, as I got 99% of it from here: http://www.codeproject.com/KB/IP/CSHTTPServer.aspx
However, I take credit for the research that led to the usage of this code, and figuring out which files to send.
I also changed minor parts of the code to avoid sending a 'default.htm' file and enabling support for files
without extensions.

- Afr0