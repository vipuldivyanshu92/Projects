using System;
using System.Globalization;
using System.IO;

namespace PIC18Emulator
{
    class Program
    {
        private static byte[] memoryProgram = new byte[0x1FFFFF];

        public class HexStreamReader : StreamReader
        {
            public HexStreamReader(string path)
                : base(path)
            {
            }

            public int ReadHex(int length)
            {
                var chars = new char[length];
                Read(chars, 0, length);
                return int.Parse(new string(chars), NumberStyles.HexNumber);
            }
        }

        public enum RecordType
        {
            Data = 0,
            EndOfFile = 1,
            ExtendedSegmentAddress = 2,
            ExtendedLinearAddress = 4
        }

        static void LoadHexProgram()
        {
            using (var hexStreamReader = new HexStreamReader("program.hex"))
            {
                RecordType recordType;
                var extendedLinearAddress = 0;
                do
                {
                    // Consume the leading semicolon
                    hexStreamReader.Read();

                    // Retrieve the informations
                    var recordLength = hexStreamReader.ReadHex(2);
                    var recordAddress = hexStreamReader.ReadHex(4);
                    recordType = (RecordType)hexStreamReader.ReadHex(2);
                    byte[] data = null;

                    switch (recordType)
                    {
                        case RecordType.Data:
                            data = new byte[recordLength];
                            for (var i = 0; i < recordLength; i++)
                            {
                                data[i] = (byte)hexStreamReader.ReadHex(2);
                            }
                            break;
                        case RecordType.ExtendedLinearAddress:
                            extendedLinearAddress = hexStreamReader.ReadHex(4);
                            break;
                        case RecordType.ExtendedSegmentAddress:
                            throw new NotImplementedException("Segment Addressing is not supported");
                    }

                    // Todo check the CRC
                    var crc = hexStreamReader.ReadHex(2);

                    // Consume the newline characters, can be \n or \r\n depending on the environment
                    foreach (var t in Environment.NewLine)
                    {
                        hexStreamReader.Read();
                    }

                    // Populate the memory                   
                    if (recordType == RecordType.Data)
                    {
                        var effectiveAddress = (extendedLinearAddress << 8) | (recordAddress);
                        Array.Copy(data, 0, memoryProgram, effectiveAddress, recordLength);
                    }

                } while (recordType != RecordType.EndOfFile);
            }
        }

        static void Main(string[] args)
        {
            LoadHexProgram();

            for (var i = 0; i < 100; i += 2)
            {
                UInt16 word = BitConverter.ToUInt16(memoryProgram, i);

                string opcode = "UNKNO";

                // 4 bits opcodes
                switch ((word & 0xF000) >> 12)
                {
                    case 0: // 0b0000:
                        opcode = "NOP";
                        break;
                    case 0x7: // 0b0111:
                        opcode = "BTG";
                        break;
                    case 0x8: // 0b1000:
                        opcode = "BSF";
                        break;
                    case 0x9: // 0b1001:
                        opcode = "BCF";
                        break;
                    case 0xA: // 0b1010:
                        opcode = "BTFSS";
                        break;
                    case 0xB: // 0b1011:
                        opcode = "BTFSC";
                        break;
                    case 0xC: // 0b1100:
                        opcode = "MOVFF";
                        i += 2;
                        break;
                }

                // 5 bits opcodes
                switch ((word & 0xF800) >> 11)
                {
                    case 0x1A: // 0b11010:
                        opcode = "BRA";
                        break;
                    case 0x1B: // 0b11011:
                        opcode = "RCALL";
                        break;
                }

                // 6 bits opcodes
                switch ((word & 0xFC00) >> 10)
                {
                    case 0x01: // 0b000001:
                        opcode = "DECF";
                        break;
                    // Include OR
                    case 0x04: // 0b000100:
                        opcode = "IORWF";
                        break;
                    case 0x05: // 0b000101:
                        opcode = "ANDWF";
                        break;
                    case 0x06: // 0b000110:
                        opcode = "XORWF";
                        break;
                    case 0x07: // 0b000111:
                        opcode = "COMF";
                        break;
                    case 0x08: // 0b001000:
                        opcode = "ADDWFC";
                        break;
                    case 0x09: // 0b001001:
                        opcode = "ADDWF";
                        break;
                    case 0x0A: // 0b001010:
                        opcode = "INCF";
                        break;
                    case 0x0B: // 0b001011:
                        opcode = "DECFSZ";
                        break;
                    case 0x0C: // 0b001100:
                        opcode = "RRCF";
                        break;
                    case 0x0D: // 0b001101:
                        opcode = "RLCF";
                        break;
                    case 0x0E: // 0b001110:
                        opcode = "SWAPF";
                        break;
                    case 0x0F: // 0b001111:
                        opcode = "INCFSZ";
                        break;
                    case 0x10: // 0b010000:
                        opcode = "RRNCF";
                        break;
                    case 0x11: // 0b010001:
                        opcode = "RLNCF";
                        break;
                    case 0x12: // 0b010010:
                        opcode = "INFSNZ";
                        break;
                    case 0x13: // 0b010011:
                        opcode = "DCFSNZ";
                        break;
                    case 0x14: // 0b010100:
                        opcode = "MOVF";
                        break;
                    case 0x15: // 0b010101:
                        opcode = "SUBFWB";
                        break;
                    case 0x16: // 0b010110:
                        opcode = "SUBWFB";
                        break;
                    case 0x17: // 0b010111:
                        opcode = "SUBWF";
                        break;
                }

                // 7 bits opcodes
                switch ((word & 0xFE00) >> 9)
                {
                    case 0x01: // 0b0000001:
                        opcode = "MULWF";
                        break;

                    case 0x30: // 0b0110000:
                        opcode = "CPFSLT";
                        break;
                    case 0x31: // 0b0110001:
                        opcode = "CPFSEQ";
                        break;
                    case 0x32: // 0b0110010:
                        opcode = "CPFSGT";
                        break;
                    case 0x33: // 0b0110011:
                        opcode = "TSTFSZ";
                        break;
                    case 0x34: // 0b0110100:
                        opcode = "SETF";
                        break;
                    case 0x35: // 0b0110101:
                        opcode = "CLRF";
                        break;
                    case 0x36: // 0b0110110:
                        opcode = "NEGF";
                        break;
                    case 0x37: // 0b0110111:
                        opcode = "MOVWF";
                        break;

                    case 0x76: // 0b1110110:
                        opcode = "CALL";
                        break;
                }

                // 8 bits opcodes
                switch ((word & 0xFF00) >> 8)
                {
                    case 0x01: // 0b00000001:
                        opcode = "MOVLB";
                        break;
                    case 0x08: // 0b00001000:
                        opcode = "SUBLW";
                        break;
                    case 0x09: // 0b00001001:
                        opcode = "IORLW";
                        break;
                    case 0x0A: // 0b00001010:
                        opcode = "XORLW";
                        break;
                    case 0x0B: // 0b00001011:
                        opcode = "ANDLW";
                        break;
                    case 0x0C: // 0b00001100:
                        opcode = "RETLW";
                        break;
                    case 0x0D: // 0b00001101:
                        opcode = "MULLW";
                        break;
                    case 0x0E: // 0b00001110:
                        opcode = "MOVLW";
                        break;
                    case 0x0F: // 0b00001111
                        opcode = "ADDLW";
                        break;

                    case 0xE0: // 0b11100000:
                        opcode = "BZ";
                        break;
                    case 0xE1: // 0b11100001:
                        opcode = "BNZ";
                        break;
                    case 0xE2: // 0b11100010:
                        opcode = "BC";
                        break;
                    case 0xE3: // 0b11100011:
                        opcode = "BNC";
                        break;
                    case 0xE4: // 0b11100100:
                        opcode = "BOV";
                        break;
                    case 0xE5: // 0b11100101:
                        opcode = "BNOV";
                        break;
                    case 0xE6: // 0b11100110:
                        opcode = "BN";
                        break;
                    case 0xE7: // 0b11100111:
                        opcode = "BNN";
                        break;
                    case 0xEF: // 0b11101111
                        opcode = "GOTO";
                        i += 2;
                        break;
                }

                // 10 bits opcodes
                switch ((word & 0xFFC0) >> 6)
                {
                    case 0x3B8: // 0b1110111000:
                        opcode = "LFSR";
                        i += 2;
                        break;
                }

                // 14 bits opcodes
                switch ((word & 0xFFFC) >> 2)
                {
                    case 0x2: // 0b00000000000010:
                        opcode = "TBLRD";
                        break;
                }

                // 15 bits opcodes
                switch ((word & 0xFFFE) >> 1)
                {
                    case 0x2: // 0b00000000000010:
                        opcode = "RETFIE";
                        break;
                    case 0x3: // 0b00000000000011:
                        opcode = "TBLWT";
                        break;
                    case 0x9: // 0b000000000001001
                        opcode = "RETURN";
                        break;
                }

                // 16 bits opcodes
                switch (word)
                {
                    case 0x0000: // 0b0000000000000000:
                        opcode = "NOP";
                        break;
                    case 0x0003: // 0b0000000000000011:
                        opcode = "SLEEP";
                        break;
                    case 0x0004: // 0b0000000000000100:
                        opcode = "CLRWDT";
                        break;
                    case 0x0005: // 0b0000000000000101:
                        opcode = "PUSH";
                        break;
                    case 0x0006: // 0b0000000000000110:
                        opcode = "POP";
                        break;
                    case 0x0007: // 0b0000000000000111:
                        opcode = "DAW";
                        break;
                    case 0x00FF: // 0b0000000011111111:
                        opcode = "RESET";
                        break;
                }

                Console.Write("{0:X4}\t{1}\n", word, opcode);
            }

            Console.ReadKey();
        }
    }
}
