using System;
using System.Net;
using System.Net.Sockets;
using System.IO;
using System.Text;
using System.Numerics;

class RealmClient
{
    private Socket client;
    private WoWSRP srp;
    private const int size = 4096;
    private byte[] data = new byte[size];

    public RealmClient(string username, string password)
    {
        srp = new WoWSRP(username, password);
    }

    public void Connect(string host, int port)
    {
        Socket newsock = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        IPAddress ipA = Dns.GetHostAddresses(host)[0];
        IPEndPoint ipEP = new IPEndPoint(ipA, port);
        newsock.BeginConnect(ipEP, new AsyncCallback(Connected), newsock);
    }

    private void sendAuthLogonChallenge()
    {
        RealmPacket packet = new RealmPacket(RealmOpcodes.AUTH_LOGON_CHALLENGE);
        packet.writeByte(8);    // error code
        packet.writeUint16((UInt16)(30 + srp.I.Length));    // Packet Size
        packet.writeString("WoW", 4);   // Game name
        packet.writeBytes(new byte[] { 3, 2, 2 }); // WoW Version
        packet.writeUint16(10505);      // WoW build
        packet.writeString("68x", 4);   // platform
        packet.writeString("niW", 4);   // Operating System
        packet.writeString("RFrf", 4);  // Country
        packet.writeUint32(0);
        packet.writeBytes(new byte[] {127, 0, 0, 1});   // IP
        packet.writePascalString(srp.I);

        client.BeginSend(packet.getFinalizedPacket(), 0, packet.Size, SocketFlags.None, new AsyncCallback(SendData), client);
    }

    private void handleAuthLogonChallenge(RealmPacket packet)
    {
        packet.readByte(); // read unknown
        packet.readByte(); // read error
        srp.B = new BigInteger(packet.readBytes(32));

        int SRP_g_len = packet.readByte(); // SRP_g length
        srp.g = new BigInteger(packet.readBytes(SRP_g_len)); // SRP_g

        int SRP_N_len = packet.readByte(); // SRP_N length
        srp.N = new BigInteger(packet.readBytes(SRP_N_len)); // SRP_N

        srp.s = packet.readBytes(32); // SRP salt

        packet.readString(16);  // CRC, not checked
        packet.readByte();      // security flag

        // Calculate the SRP values
        srp.calculateSRP_A();
        srp.calculateSRP_x();
        srp.calculateSRP_v();
        srp.calculateSRP_u();
        srp.calculateSRP_S();
        srp.calculateSRP_K();
        srp.calculateSRP_M1();
        srp.calculateSRP_M2();
    }

    private void sendAuthLogonProof()
    {
        RealmPacket packet = new RealmPacket(RealmOpcodes.AUTH_LOGON_PROOF);

        packet.writeBigInteger(srp.A, 32); // A
        packet.writeBytes(srp.M1); // M1
        packet.writeBytes(new byte[20]); // crc
        packet.writeInt16(0); //

        client.BeginSend(packet.getFinalizedPacket(), 0, packet.Size, SocketFlags.None, new AsyncCallback(SendData), client);
    }

    private void handleAuthLogonProof(RealmPacket packet)
    {
        // *TODO* Do the proper checks
        packet.readByte(); // error
        byte[] M2 = packet.readBytes(20); // M2
        packet.readUint32(); // unk1
        packet.readUint32(); // unk2
        packet.readUint16(); // unk3
    }

    private void sendRealmList()
    {
        RealmPacket packet = new RealmPacket(RealmOpcodes.REALM_LIST);

        packet.writeUint32(0);

        client.BeginSend(packet.getFinalizedPacket(), 0, packet.Size, SocketFlags.None, new AsyncCallback(SendData), client);
    }

    private void handleRealmList(RealmPacket packet)
    {
        SRealmList realmList = SRealmList.getInstance();

        packet.readUint16(); // size
        packet.readUint32(); // unk1
        int nbrealms = packet.readUint16(); // nb realms

        for (int i = 0; i < nbrealms; i++)
        {
            Realm r = new Realm();
            r.Icon = packet.readByte(); // icon
            r.IsLock = packet.readByte(); // lock
            r.Color = packet.readByte(); // color
            r.Name = packet.readCString(); // name
            r.Address = packet.readCString(); // address
            r.Population = packet.readFloat(); // population
            r.NbCharacters = packet.readByte(); // nb characters
            r.Timezone = packet.readByte(); // timezone
            packet.readByte(); // unk

            realmList.add(r);
        }

        packet.readByte(); // unk2
        packet.readByte(); // unk3
    }

    private void Connected(IAsyncResult iar)
    {
        client = (Socket)iar.AsyncState;
        try
        {
            client.EndConnect(iar);

            sendAuthLogonChallenge();

            client.BeginReceive(data, 0, size, SocketFlags.None, new AsyncCallback(ReceiveData), client);
        }
        catch (SocketException)
        {
            Console.WriteLine("Connection failed");
            // Error connecting
        }
    }

    private void ReceiveData(IAsyncResult iar)
    {
        Socket remote = (Socket)iar.AsyncState;
        int recv = remote.EndReceive(iar);

        RealmPacket packet = new RealmPacket(data);
        Console.WriteLine("Packet received : {0}", packet.Opcode);
        switch (packet.Opcode)
        {
            case RealmOpcodes.AUTH_LOGON_CHALLENGE:
                handleAuthLogonChallenge(packet);
                sendAuthLogonProof();
                break;
            case RealmOpcodes.AUTH_LOGON_PROOF:
                handleAuthLogonProof(packet);
                sendRealmList();
                break;
            case RealmOpcodes.REALM_LIST:
                handleRealmList(packet);
                break;
            default:
                Console.WriteLine("Unknown Opcode {0}", packet.Opcode);
                break;
        }

        // continue to wait for datas
        client.BeginReceive(data, 0, size, SocketFlags.None, new AsyncCallback(ReceiveData), client);
    }

    private void SendData(IAsyncResult iar)
    {
        Socket remote = (Socket)iar.AsyncState;
        int sent = remote.EndSend(iar);
    }
}
