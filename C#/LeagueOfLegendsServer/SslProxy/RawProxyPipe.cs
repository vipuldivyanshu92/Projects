using System;
using System.IO;
using System.Text;

namespace SslProxy
{
    public class RawProxyPipe
    {
        private readonly Stream src;
        private readonly Stream dst;
        private readonly bool verbose;

        public RawProxyPipe(Stream src, Stream dst, bool verbose)
        {
            this.src = src;
            this.dst = dst;
            this.verbose = verbose;
        }

        public void Transfer()
        {
            var buffer = new byte[2048];

            try
            {
                int len;
                while ((len = src.Read(buffer, 0, buffer.Length)) > 0)
                {
                    if (verbose)
                    {
                        var content = Encoding.ASCII.GetString(buffer, 0, len);
                        Console.WriteLine(content);
                    }
                    dst.Write(buffer, 0, len);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }
    }
}
