import random

def modexp(t, u, n):
    s = 1
    while u:
        if u & 1:
            s = (s * t) % n
        u >>= 1
        t = (t * t) % n;
    return s

def HexStringToIntHash(s):
    v = []
    for i in range(0, len(s), 8):
        v.append(int(s[i:i+8].decode("hex")[::-1].encode("hex"), 16))
    return v

def Decrypt(hex_publicClientKey, encryptedMessage):
    publicClientKey = int(hex_publicClientKey, 16)
    dhPrimeNum = int("eca2e8c85d863dcdc26a429a71a9815ad052f6139669dd659f98ae159d313d13c6bf2838e10a69b6478b64a24bd054ba8248e8fa778703b418408249440b2c1edd28853e240d8a7e49540b76d120d3b1ad2878b1b99490eb4a2a5e84caa8a91cecbdb1aa7c816e8be343246f80c637abc653b893fd91686cf8d32d6cfe5f2a6f", 16)
    serverPrivateKey = int("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef", 16)

    common_key = modexp(publicClientKey, serverPrivateKey, dhPrimeNum)

    encryptedMessageSize = len(encryptedMessage)

    key = HexStringToIntHash(("%x" % common_key)[0:32])

    buf = HexStringToIntHash(encryptedMessage)

    message = buf[:]

    for i in range(0, encryptedMessageSize / 8, 2):

        m = buf[i:][0]
        n = buf[i:][1]
        
        s = 0xC6EF3720
        
        for j in range(32):
            n -= ((m >> 5) + key[3]) ^ (((m << 4) & 4294967295) + key[2]) ^ (s + m)
            n &= 4294967295
            
            m -= ((n >> 5) + key[1]) ^ (((n << 4) & 4294967295) + key[0]) ^ (s + n)
            m &= 4294967295
            
            s -= 0x9E3779B9
            s &= 4294967295
             
        buf[i] = m
        buf[i+1] = n
        
        if i > 1:
            buf[i] ^= message[i-2]
            buf[i+1] ^= message[i-1]

    message = ""
    for e in buf:
        v = "%x" % (e)
        v = (len(v) % 2) * '0' + v
        message += (v).decode("hex")[::-1]

    return message
