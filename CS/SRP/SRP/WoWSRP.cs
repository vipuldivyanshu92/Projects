using System;
using System.Text;
using System.Numerics;
using System.Security.Cryptography;

class WoWSRP
{
    private string SRP_I;       // Username
    private string SRP_P;       // Username password
    private byte[] SRP_s;       // User's salt
    private BigInteger SRP_B;   // A public ephemeral server value
    private BigInteger SRP_g;   // A generator modulo N
    private BigInteger SRP_N;   // A large safe prime
    private BigInteger SRP_a;   // Secret ephemeral value
    private BigInteger SRP_A;   // A public ephemeral client value
    private BigInteger SRP_x;   // Private key
    private BigInteger SRP_v;   // Password verifier
    private BigInteger SRP_u;   // Random scrambling parameter
    private BigInteger SRP_S;   // session key
    private byte[] SRP_K;       // hash(session key)
    private byte[] SRP_M1;      // authentification check
    private byte[] SRP_M2;      // authentification check

    /*
     * Constructors
     */

    public WoWSRP(string username, string password)
    {
        // set SRP_I and SRP_P
        SRP_I = username.ToUpper();
        SRP_P = password.ToUpper();

        // generate SRP_a, 19bytes long value
        Random rgenerator = new Random();
        byte[] b = new byte[19];
        rgenerator.NextBytes(b);
        SRP_a = toPositive(new BigInteger(b));
    }

    /*
     * Maths methods to calculate the required value
     */

    private static BigInteger toPositive(BigInteger v)
    {
        if (v >= 0)
            return v;

        byte[] b = new byte[v.ToByteArray().Length + 1];
        v.ToByteArray().CopyTo(b, 0);
        return new BigInteger(b);
    }

    public void calculateSRP_A()
    {
        SRP_A = BigInteger.ModPow(SRP_g, SRP_a, SRP_N);
        if (SRP_A < 0)
            SRP_A += SRP_N;
    }

    public void calculateSRP_x()
    {
        SHA1 sha = new SHA1CryptoServiceProvider();

        // authstr = username:password
        string authstr = string.Format("{0}:{1}", SRP_I, SRP_P);

        // userhash = sha1(authstr)
        byte[] userhash = sha.ComputeHash(Encoding.ASCII.GetBytes(authstr));

        // concatenate the salt and the hash
        byte[] concat = new byte[SRP_s.Length + userhash.Length];
        SRP_s.CopyTo(concat, 0);
        userhash.CopyTo(concat, SRP_s.Length);

        // compute the salted auth string SHA1
        byte[] hash = sha.ComputeHash(concat);

        // recreate an array with trailing 0 to specify a positive value
        byte[] b = new byte[hash.Length + 1];
        hash.CopyTo(b, 0);

        SRP_x = new BigInteger(b);
    }

    public void calculateSRP_v()
    {
        SRP_v = BigInteger.ModPow(SRP_g, SRP_x, SRP_N);
        if (SRP_v < 0)
            SRP_v += SRP_N;
    }

    public void calculateSRP_u()
    {
        // create the sha object
        SHA1 sha = new SHA1CryptoServiceProvider();

        // get array of bytes
        byte[] Abytes = SRP_A.ToByteArray();
        byte[] Bbytes = SRP_B.ToByteArray();

        // concatenate A and B
        byte[] concat = new byte[Abytes.Length + Bbytes.Length];
        Abytes.CopyTo(concat, 0);
        Bbytes.CopyTo(concat, Abytes.Length);

        // Compute sha(concat(A, B))
        byte[] hash = sha.ComputeHash(concat);

        // add 0 to the end of the hash to get a positive value
        byte[] b = new byte[hash.Length + 1];
        hash.CopyTo(b, 0);

        SRP_u = new BigInteger(b);
    }

    public void calculateSRP_S()
    {
        BigInteger Bv = SRP_B - 3 * SRP_v;
        BigInteger aux = SRP_a + SRP_u * SRP_x;

        SRP_S = BigInteger.ModPow(Bv, aux, SRP_N);
        if (SRP_S < 0)
            SRP_S += SRP_N;
    }

    public void calculateSRP_K()
    {
        byte[] S = SRP_S.ToByteArray();
        byte[] S1 = new byte[16];
        byte[] S2 = new byte[16];

        // Split the S value in S1 and S2, interleaving each char
        uint j = 0;
        for (uint i = 0; i < 32; i+=2)
        {
            S1[j] = S[i];
            S2[j] = S[i + 1];
            j++;
        }

        // Calculate S1 and S2 sha
        SHA1 sha = new SHA1CryptoServiceProvider();
        byte[] S1hash = sha.ComputeHash(S1);
        byte[] S2hash = sha.ComputeHash(S2);

        // 
        j = 0;
        byte[] SKhash = new byte[40];
        for (uint i = 0; i < 20; i++)
        {
            SKhash[j++] = S1hash[i];
            SKhash[j++] = S2hash[i];
        }

        SRP_K = SKhash;
    }

    public void calculateSRP_M1()
    {
        SHA1 sha = new SHA1CryptoServiceProvider();

        // limit SRP_N to 32 bytes
        byte[] N = new byte[32];
        Buffer.BlockCopy(SRP_N.ToByteArray(), 0, N, 0, 32);
        // Calculate the hashes
        byte[] Nhash = sha.ComputeHash(N);
        byte[] ghash = sha.ComputeHash(SRP_g.ToByteArray());
        byte[] userhash = sha.ComputeHash(Encoding.ASCII.GetBytes(SRP_I));

        byte[] nghash = new byte[20];
        for (uint i = 0; i < nghash.Length; i++)
            nghash[i] = (byte)(Nhash[i] ^ ghash[i]);

        // Convert to array and ensure the right size
        byte[] Abytes = new byte[32];
        Buffer.BlockCopy(SRP_A.ToByteArray(), 0, Abytes, 0, 32);
        byte[] Bbytes = new byte[32];
        Buffer.BlockCopy(SRP_B.ToByteArray(), 0, Bbytes, 0, 32);

        byte[] concat = new byte[nghash.Length + userhash.Length + SRP_s.Length
            + Abytes.Length + Bbytes.Length + SRP_K.Length];

        int offset = 0;
        nghash.CopyTo(concat, 0);
        offset += nghash.Length;
        userhash.CopyTo(concat, offset);
        offset += userhash.Length;
        SRP_s.CopyTo(concat, offset);
        offset += SRP_s.Length;
        Abytes.CopyTo(concat, offset);
        offset += Abytes.Length;
        Bbytes.CopyTo(concat, offset);
        offset += Bbytes.Length;
        SRP_K.CopyTo(concat, offset);

        SRP_M1 = sha.ComputeHash(concat);
    }

    public void calculateSRP_M2()
    {
        SHA1 sha = new SHA1CryptoServiceProvider();
        byte[] Abytes = SRP_A.ToByteArray();

        byte[] concat = new byte[Abytes.Length + SRP_M1.Length + SRP_K.Length];
        int offset = 0;

        Abytes.CopyTo(concat, offset);
        offset += Abytes.Length;
        SRP_M1.CopyTo(concat, offset);
        offset += SRP_M1.Length;
        SRP_K.CopyTo(concat, offset);

        SRP_M2 = sha.ComputeHash(concat);
    }

    /*
     * Accessors and Mutators
     */

    public string I
    {
        get { return SRP_I; }
    }

    public string P
    {
        get { return SRP_P; }
    }

    public BigInteger A
    {
        get { return SRP_A; }
        set { SRP_A = toPositive(value); }
    }

    public byte[] s
    {
        get { return SRP_s; }
        set { SRP_s = value; }
    }

    public BigInteger g
    {
        get { return SRP_g; }
        set { SRP_g = toPositive(value); }
    }

    public BigInteger N
    {
        get { return SRP_N; }
        set { SRP_N = toPositive(value); }
    }

    public BigInteger B
    {
        get { return SRP_B; }
        set { SRP_B = toPositive(value); }
    }

    public byte[] K
    {
        get { return SRP_K; }
    }

    public byte[] M1
    {
        get { return SRP_M1; }
    }

    public byte[] M2
    {
        get { return SRP_M2; }
    }

    public BigInteger x
    {
        get { return SRP_x; }
    }

    public BigInteger v
    {
        get { return SRP_v; }
    }

    public BigInteger u
    {
        get { return SRP_u; }
    }

    public BigInteger S
    {
        get { return SRP_S; }
    }
}
