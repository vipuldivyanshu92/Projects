using System;
using System.Collections.Generic;

sealed class SRealmList
{
    private static List<Realm> list = new List<Realm>();
    private static readonly SRealmList instance = new SRealmList();

    private SRealmList()
    {
    }

    public static SRealmList getInstance()
    {
        return instance;
    }

    public void add(Realm r)
    {
        list.Add(r);
    }

    public Realm get(int id)
    {
        return list[id];
    }

    public Realm getByName(string name)
    {
        foreach (Realm r in list)
        {
            if (r.Name == name)
                return r;
        }
        return null;
    }
}
