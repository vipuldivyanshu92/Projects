// simple pogo class

using System;
using System.Collections.Generic;

class Realm
{
    private byte icon;
    private byte islock;
    private byte color;
    private string name;
    private string address;
    private float population;
    private byte nbcharacters;
    private byte timezone;

    public byte Icon
    {
        get { return icon; }
        set { icon = value; }
    }

    public byte IsLock
    {
        get { return islock; }
        set { islock = value; }
    }

    public byte Color
    {
        get { return color; }
        set { color = value; }
    }

    public string Name
    {
        get { return name; }
        set { name = value; }
    }

    public string Address
    {
        get { return address; }
        set { address = value; }
    }

    public float Population
    {
        get { return population; }
        set { population = value; }
    }

    public byte NbCharacters
    {
        get { return nbcharacters; }
        set { nbcharacters = value; }
    }

    public byte Timezone
    {
        get { return timezone; }
        set { timezone = value; }
    }
}
