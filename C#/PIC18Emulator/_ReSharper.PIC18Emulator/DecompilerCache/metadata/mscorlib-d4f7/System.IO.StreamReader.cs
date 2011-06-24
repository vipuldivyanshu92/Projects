// Type: System.IO.StreamReader
// Assembly: mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089
// Assembly location: C:\Windows\Microsoft.NET\Framework\v4.0.30319\mscorlib.dll

using System;
using System.Runtime.InteropServices;
using System.Security;
using System.Text;

namespace System.IO
{
    [ComVisible(true)]
    [Serializable]
    public class StreamReader : TextReader
    {
        public new static readonly StreamReader Null;
        public StreamReader(Stream stream);
        public StreamReader(Stream stream, bool detectEncodingFromByteOrderMarks);
        public StreamReader(Stream stream, Encoding encoding);
        public StreamReader(Stream stream, Encoding encoding, bool detectEncodingFromByteOrderMarks);
        public StreamReader(Stream stream, Encoding encoding, bool detectEncodingFromByteOrderMarks, int bufferSize);

        [SecuritySafeCritical]
        public StreamReader(string path);

        [SecuritySafeCritical]
        public StreamReader(string path, bool detectEncodingFromByteOrderMarks);

        [SecuritySafeCritical]
        public StreamReader(string path, Encoding encoding);

        [SecuritySafeCritical]
        public StreamReader(string path, Encoding encoding, bool detectEncodingFromByteOrderMarks);

        [SecuritySafeCritical]
        public StreamReader(string path, Encoding encoding, bool detectEncodingFromByteOrderMarks, int bufferSize);

        public virtual Encoding CurrentEncoding { get; }
        public virtual Stream BaseStream { get; }

        public bool EndOfStream { [SecuritySafeCritical]
        get; }

        public override void Close();
        protected override void Dispose(bool disposing);
        public void DiscardBufferedData();

        [SecuritySafeCritical]
        public override int Peek();

        [SecuritySafeCritical]
        public override int Read();

        [SecuritySafeCritical]
        public override int Read([In, Out] char[] buffer, int index, int count);

        [SecuritySafeCritical]
        public override string ReadToEnd();

        [SecuritySafeCritical]
        public override string ReadLine();
    }
}
