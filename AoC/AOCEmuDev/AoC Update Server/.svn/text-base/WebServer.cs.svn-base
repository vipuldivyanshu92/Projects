using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using Microsoft.Win32;

namespace AoC_Update_Server
{
    public class WebServer : CSHTTPServer
    {
        public string Folder;

        public WebServer(int Port, string FolderPath)
            : base(Port)
        {
            Folder = FolderPath;
        }

        public override void OnResponse(ref HTTPRequestStruct rq, ref HTTPResponseStruct rp)
        {
            string path = this.Folder + "\\" + rq.URL.Replace("/", "\\");

            /*if (Directory.Exists(path))
            {
                if (File.Exists(path + "default.htm"))
                    path += "\\default.htm";
                else
                {
                    string[] dirs = Directory.GetDirectories(path);
                    string[] files = Directory.GetFiles(path);

                    string bodyStr = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">\n";
                    bodyStr += "<HTML><HEAD>\n";
                    bodyStr += "<META http-equiv=Content-Type content=\"text/html; charset=windows-1252\">\n";
                    bodyStr += "</HEAD>\n";
                    bodyStr += "<BODY><p>Folder listing, to do not see this add a 'default.htm' document\n<p>\n";
                    for (int i = 0; i < dirs.Length; i++)
                        bodyStr += "<br><a href = \"" + rq.URL + Path.GetFileName(dirs[i]) + "/\">[" + Path.GetFileName(dirs[i]) + "]</a>\n";
                    for (int i = 0; i < files.Length; i++)
                        bodyStr += "<br><a href = \"" + rq.URL + Path.GetFileName(files[i]) + "\">" + Path.GetFileName(files[i]) + "</a>\n";
                    bodyStr += "</BODY></HTML>\n";

                    rp.BodyData = Encoding.ASCII.GetBytes(bodyStr);
                    return;
                }
            }*/

            if (File.Exists(path))
            {
                RegistryKey rk = Registry.ClassesRoot.OpenSubKey(Path.GetExtension(path), true);

                // Get the data from a specified item in the key.
                String s = (String)rk.GetValue("Content Type");

                if (s == null)
                    s = "";

                // Open the stream and read it back.
                rp.fs = File.Open(path, FileMode.Open);
                if (!s.Equals(""))
                    rp.Headers["Content-type"] = s;
                else //This needs to be here for files without an extension!
                {
                    rp.Headers["Content-type"] = "text/plain";
                    Console.WriteLine("Content-type: " + rp.Headers["Content-type"]);
                }
            }
            else
            {

                rp.status = (int)RespState.NOT_FOUND;

                string bodyStr = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">\n";
                bodyStr += "<HTML><HEAD>\n";
                bodyStr += "<META http-equiv=Content-Type content=\"text/html; charset=windows-1252\">\n";
                bodyStr += "</HEAD>\n";
                bodyStr += "<BODY>File not found!!</BODY></HTML>\n";

                rp.BodyData = Encoding.ASCII.GetBytes(bodyStr);

            }

        }
    }
}
