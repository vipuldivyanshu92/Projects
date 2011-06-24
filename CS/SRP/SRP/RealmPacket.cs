using System;

class RealmPacket : AbstractPacket
{
    // Write
    public RealmPacket(byte opcode) : base(opcode)
    {
        writeByte(Opcode);
    }

    // Read
    public RealmPacket(byte[] buffer) : base(buffer)
    {
        base.Opcode = readByte();
    }
}
