using System;

class WorldPacket : AbstractPacket
{
    // Write
    public WorldPacket(byte opcode) : base(opcode)
    {
        writeByte(Opcode);
    }

    // Read
    public RealmPacket(byte[] buffer) : base(buffer)
    {
        base.Opcode = readByte();
    }
}
