using System.IO;
using System.Threading;

namespace SslProxy
{
    public class RawProxifier
    {
        public Stream LocalStream { get; set; }
        public Stream RemoteStream { get; set; }

        //
        public RawProxifier()
        {
        }

        // 
        public RawProxifier(Stream local, Stream remote)
        {
            LocalStream = local;
            RemoteStream = remote;
        }

        //
        public void Execute()
        {
            if (Init())
            {
                var localToRemote = new RawProxyPipe(LocalStream, RemoteStream, true);
                var localToRemoteThread = new Thread(localToRemote.Transfer);
                localToRemoteThread.Start();

                var remoteToLocal = new RawProxyPipe(RemoteStream, LocalStream, true);
                var remoteToLocalThread = new Thread(remoteToLocal.Transfer);
                remoteToLocalThread.Start();
            }
        }

        //
        public virtual bool Init()
        {
            return true;
        }
    }
}
