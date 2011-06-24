using System;
using System.Text;
using System.Numerics;
using System.Runtime.InteropServices;

abstract class AbstractPacket
{
    private byte[] data;
    private byte opcode;
    private int offset = 0;

    public AbstractPacket(byte Opcode)
    {
        
        opcode = Opcode;
        data = new byte[64];
    }

    public AbstractPacket(byte[] buffer)
    {
        data = new byte[buffer.Length];
        Buffer.BlockCopy(buffer, 0, data, 0, data.Length);
    }

    private void increasePacketSize(int size)
    {
        if ((offset + size) > data.Length)
        {
            Array.Resize(ref data, data.Length * 2);
            increasePacketSize(size);
        }
    }

    /*
     * Setters
     */

    public void writeByte(byte v)
    {
        increasePacketSize(1);
        data[offset++] = v;
    }

    public void writeUint16(UInt16 v)
    {
        increasePacketSize(2);
        BitConverter.GetBytes(v).CopyTo(data, offset);
        offset += 2;
    }

    public void writeUint32(UInt32 v)
    {
        increasePacketSize(4);
        BitConverter.GetBytes(v).CopyTo(data, offset);
        offset += 4;
    }

    public void writeUint64(UInt64 v)
    {
        increasePacketSize(8);
        BitConverter.GetBytes(v).CopyTo(data, offset);
        offset += 8;
    }

    public void writeInt16(Int16 v)
    {
        increasePacketSize(2);
        BitConverter.GetBytes(v).CopyTo(data, offset);
        offset += 2;
    }

    public void writeInt32(Int32 v)
    {
        increasePacketSize(4);
        BitConverter.GetBytes(v).CopyTo(data, offset);
        offset += 4;
    }

    public void writeInt64(Int64 v)
    {
        increasePacketSize(8);
        BitConverter.GetBytes(v).CopyTo(data, offset);
        offset += 8;
    }

    public void writeFloat(float v)
    {
        increasePacketSize(4);
        BitConverter.GetBytes(v).CopyTo(data, offset);
        offset += 4;
    }

    public void writeDouble(double v)
    {
        increasePacketSize(8);
        BitConverter.GetBytes(v).CopyTo(data, offset);
        offset += 8;
    }

    public void writeBytes(byte[] v)
    {
        increasePacketSize(v.Length);
        v.CopyTo(data, offset);
        offset += v.Length;
    }

    public void writeBigInteger(BigInteger v, int size)
    {
        increasePacketSize(size);
        byte[] b = new byte[size];
        v.ToByteArray().CopyTo(b, 0);
        b.CopyTo(data, offset);
        offset += size;
    }

    public void writeString(string v, int size)
    {
        increasePacketSize(size);
        Encoding.ASCII.GetBytes(v).CopyTo(data, offset);
        offset += size;
    }

    public void writeCString(string v)
    {
        writeString(v, v.Length + 1);
    }

    public void writeUnicodeString(string v)
    {
        byte[] b = Encoding.Unicode.GetBytes(v);
        increasePacketSize(b.Length);
        b.CopyTo(data, offset);
        offset += b.Length;
    }

    public void writePascalString(string v)
    {
        increasePacketSize(v.Length + 1);
        data[offset++] = (byte)v.Length;
        Encoding.ASCII.GetBytes(v).CopyTo(data, offset);
        offset += v.Length;
    }

    /*
     * Readers
     */

    public byte readByte()
    {
        return data[offset++];
    }

    public UInt16 readUint16()
    {
        UInt16 v = BitConverter.ToUInt16(data, offset);
        offset += 2;
        return v;
    }

    public UInt32 readUint32()
    {
        UInt32 v = BitConverter.ToUInt32(data, offset);
        offset += 4;
        return v;
    }

    public UInt64 readUint64()
    {
        UInt64 v = BitConverter.ToUInt64(data, offset);
        offset += 8;
        return v;
    }

    public Int16 readInt16()
    {
        Int16 v = BitConverter.ToInt16(data, offset);
        offset += 2;
        return v;
    }

    public Int32 readInt32()
    {
        Int32 v = BitConverter.ToInt32(data, offset);
        offset += 4;
        return v;
    }

    public Int64 readInt64()
    {
        Int64 v = BitConverter.ToInt64(data, offset);
        offset += 8;
        return v;
    }

    public float readFloat()
    {
        float v = BitConverter.ToSingle(data, offset);
        offset += 4;
        return v;
    }

    public double readDouble()
    {
        double v = BitConverter.ToDouble(data, offset);
        offset += 8;
        return v;
    }

    public byte[] readBytes(int count)
    {
        byte[] v = new byte[count];
        Buffer.BlockCopy(data, offset, v, 0, count);
        offset += count;
        return v;
    }

    public BigInteger readBigInteger(int size)
    {
        return new BigInteger(readBytes(size));
    }

    public string readString(int size)
    {
        string v = Encoding.ASCII.GetString(data, offset, size);
        offset += size;
        return v;
    }

    public string readCString()
    {
        int pos;
        for (pos = offset; data[pos] != 0; pos++) ;
        string v = Encoding.ASCII.GetString(data, offset, pos - offset);
        offset = pos + 1;
        return v;
    }

    public string readUnicodeString()
    {
        return "";
    }

    public string readPascalString()
    {
        int l = data[offset];
        string v = Encoding.ASCII.GetString(data, offset, l);
        offset += l;
        return v;
    }


    /*
     * 
     */

    public byte Opcode
    {
        get { return opcode; }
        set { opcode = value; }
    }

    public int Size
    {
        get { return offset; }
    }

    public byte[] getFinalizedPacket()
    {
        return data;
    }
}
