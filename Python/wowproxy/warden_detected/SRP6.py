"""
    Written by Adraen for use in a WoW / Client server
"""

import random
import hashlib
import convertool

def modexp (t, u, n):
    #computes s = (t ^ u) mod n
    #args are base, exponent, modulus
    #(see Bruce Schneier's book, _Applied Cryptography_ p. 244)
    # From "http://dkerr.com/using%20python.html"
    s = 1
    while u:
        if u & 1:
            s = (s * t)%n
        u >>= 1
        t = (t * t)%n;
    return s

class ValueNotSetException(Exception):
    def __init__(self, var):
        self.var = var
    def __str__(self):
        return repr(self.var)

class SRP6:
    def __init__(self, **kwargs):
        self.SRP_g = kwargs.get('g', None)
        self.SRP_N = kwargs.get('N', None)       # modulus
        self.SRP_a = kwargs.get('a', None)
        self.SRP_A = kwargs.get('A', None)       # A = g^a
        self.SRP_s = kwargs.get('s', None)       # salt
        self.SRP_I = kwargs.get('I', None)       # username
        self.SRP_P = kwargs.get('P', None)       # password
        self.SRP_x = kwargs.get('x', None)       # x = H(s, I, P)
        self.SRP_v = kwargs.get('v', None)       # v = g^x
        self.SRP_b = kwargs.get('b', None)
        self.SRP_B = kwargs.get('B', None)       # B = 3v+g^b
        self.SRP_u = kwargs.get('u', None)       # u=Hash(A,B)
        self.SRP_S = kwargs.get('S', None)       # S = (B-3g^x)^(a+ux)
        self.SRP_K = kwargs.get('K', None)       # K = Hash(S)
        self.SRP_M1 = kwargs.get('M1', None)
        self.SRP_M2 = kwargs.get('M2', None)


    # SRP_g
    def get_g(self):
        if not self.SRP_g:
            raise ValueNotSetException('SRP_g')
        return self.SRP_g

    def set_g(self, g):
        self.SRP_g = g

    # SRP_N
    def get_N(self):
        if not self.SRP_N:
            raise ValueNotSetException('SRP_N')
        return self.SRP_N

    def set_N(self, N):
        self.SRP_N = N
        
    # SRP_a
    def generate_a(self):
        self.SRP_a = random.getrandbits(19 * 8) # 19 bytes

    def get_a(self):
        if not self.SRP_a:
            raise ValueNotSetException('SRP_a')
        return self.SRP_a

    def set_a(self, a):
        self.SRP_a = a

    # SRP_A
    def calculate_A(self):
        if not self.SRP_a:
            raise ValueNotSetException('SRP_a')
        if not self.SRP_g:
            raise ValueNotSetException('SRP_g')
        if not self.SRP_N:
            raise ValueNotSetException('SRP_N')
        self.SRP_A = modexp(self.SRP_g, self.SRP_a, self.SRP_N)

    def get_A(self):
        if not self.SRP_A:
            raise ValueNotSetException('SRP_A')
        return self.SRP_A

    def set_A(self, A):
        self.SRP_A = A

    # SRP_s
    def generate_s(self):
        self.SRP_s = random.getrandbits(32 * 8) # 32 bytes

    def get_s(self):
        if not self.SRP_s:
            raise ValueNotSetException('SRP_s')
        return self.SRP_s

    def set_s(self, s):
        self.SRP_s = s

    # SRP_I
    def get_I(self):
        if not self.SRP_I:
            raise ValueNotSetException('SRP_I')
        return self.SRP_I

    def set_I(self, I):
        self.SRP_I = I.upper()

    # SRP_P
    def get_P(self):
        if not self.SRP_P:
            raise ValueNotSetException('SRP_P')
        return self.SRP_P

    def set_P(self, P):
        self.SRP_P = P.upper()

    # SRP_x
    def calculate_x(self):
        if not self.SRP_I:
            raise ValueNotSetException('SRP_I')
        if not self.SRP_P:
            raise ValueNotSetException('SRP_P')
        if not self.SRP_s:
            raise ValueNotSetException('SRP_s')
        SRP_authstr = '%s:%s' % (self.SRP_I, self.SRP_P)                            # Concatenate USER:PASS
        SRP_userhash = hashlib.sha1(SRP_authstr.upper()).digest()                   # Get the SHA hash
        print "%s" % ((convertool.intToStr(self.SRP_s)[::-1]+SRP_userhash).encode('hex'))
        self.SRP_x = convertool.strToInt(hashlib.sha1(convertool.intToStr(self.SRP_s)[::-1]+SRP_userhash).digest()[::-1])    # Get SHA of salted user hash

    def get_x(self):
        if not self.SRP_x:
            raise ValueNotSetException('SRP_x')
        return self.SRP_x

    def set_x(self, x):
        self.SRP_x = x

    # SRP_v
    def calculate_v(self):
        if not self.SRP_g:
            raise ValueNotSetException('SRP_g')
        if not self.SRP_x:
            raise ValueNotSetException('SRP_x')
        if not self.SRP_N:
            raise ValueNotSetException('SRP_N')
        self.SRP_v = modexp(self.SRP_g, self.SRP_x, self.SRP_N)

    def get_v(self):
        if not self.SRP_v:
            raise ValueNotSetException('SRP_v')
        return self.SRP_v

    def set_v(self, v):
        self.SRP_v = v

    # SRP_b
    def generate_b(self):
        self.SRP_b = random.getrandbits(19 * 8) # 19 bytes

    def get_b(self):
        if not self.SRP_b:
            raise ValueNotSetException('SRP_b')
        return self.SRP_b

    def set_b(self, b):
        self.SRP_b = b

    # SRP_B
    def calculate_B(self):
        if not self.SRP_g:
            raise ValueNotSetException('SRP_g')
        if not self.SRP_b:
            raise ValueNotSetException('SRP_b')
        if not self.SRP_N:
            raise ValueNotSetException('SRP_N')
        if not self.SRP_v:
            raise ValueNotSetException('SRP_v')
        gmod = modexp(self.SRP_g, self.SRP_b, self.SRP_N)
        self.SRP_B = ((self.SRP_v * 3) + gmod) % self.SRP_N

    def get_B(self):
        if not self.SRP_B:
            raise ValueNotSetException('SRP_B')
        return self.SRP_B

    def set_B(self, B):
        self.SRP_B = B

    # SRP_u
    def calculate_u(self):
        if not self.SRP_A:
            raise ValueNotSetException('SRP_A')
        if not self.SRP_B:
            raise ValueNotSetException('SRP_B')
        print('hash', hashlib.sha1(convertool.intToStr(self.SRP_A)[::-1]+convertool.intToStr(self.SRP_B)[::-1]).hexdigest())
        self.SRP_u = convertool.strToInt(hashlib.sha1(convertool.intToStr(self.SRP_A)[::-1]+convertool.intToStr(self.SRP_B)[::-1]).digest()[::-1])

    def get_u(self):
        if not self.SRP_u:
            raise ValueNotSetException('SRP_u')
        return self.SRP_u

    def set_u(self, u):
        self.SRP_u = u


    # SRP_S
    def calculate_S_client(self):
        # S = (B-3g^x)^{a+ux}
        if not self.SRP_B:
            raise ValueNotSetException('SRP_B')
        if not self.SRP_v:
            raise ValueNotSetException('SRP_v')
        if not self.SRP_a:
            raise ValueNotSetException('SRP_a')
        if not self.SRP_u:
            raise ValueNotSetException('SRP_u')
        if not self.SRP_x:
            raise ValueNotSetException('SRP_x')
        if not self.SRP_N:
            raise ValueNotSetException('SRP_N')
        self.SRP_S = modexp(self.SRP_B - 3 * self.SRP_v, self.SRP_a + self.SRP_u * self.SRP_x, self.SRP_N)

    def calculate_S_server(self):
        # S = (A * (v^u))^ b
        if not self.SRP_A:
            raise ValueNotSetException('SRP_A')
        if not self.SRP_v:
            raise ValueNotSetException('SRP_v')
        if not self.SRP_b:
            raise ValueNotSetException('SRP_b')
        if not self.SRP_u:
            raise ValueNotSetException('SRP_u')
        if not self.SRP_N:
            raise ValueNotSetException('SRP_N')
        self.SRP_S = modexp(self.SRP_A * modexp(self.SRP_v, self.SRP_u, self.SRP_N), self.SRP_b, self.SRP_N)

    def get_S(self):
        if not self.SRP_S:
            raise ValueNotSetException('SRP_S')
        return self.SRP_S

    def set_S(self, s):
        self.SRP_S = s

    #SRP_K
    def calculate_K(self):
        if not self.SRP_S:
            raise ValueNotSetException('SRP_S')
        SRP_S1 = ""
        SRP_S2 = ""
        tmp_S = convertool.intToStr(self.SRP_S)[::-1]       # SRP_S is reversed
        for i in range(32):                 # Split the S value in S1 and S2, interleaving each char
           if i % 2 == 0:
              SRP_S1 += tmp_S[i]
           else:
              SRP_S2 += tmp_S[i]
              
        SRP_S1hash = hashlib.sha1(SRP_S1).digest()      # Calculate SHA hash
        SRP_S2hash = hashlib.sha1(SRP_S2).digest()

        SRP_SKhash = ""
        for i in range(20):
           SRP_SKhash += SRP_S1hash[i] + SRP_S2hash[i]  # Join S1hash and S2hash in one string, interleaving each char
        self.SRP_K = convertool.strToInt(SRP_SKhash[::-1])

    def get_K(self):
        if not self.SRP_K:
            raise ValueNotSetException('SRP_K')
        return self.SRP_K

    def set_K(self, k):
        self.SRP_K = k

    #SRP_M1
    def calculate_M1(self):
        if not self.SRP_N:
            raise ValueNotSetException('SRP_N')
        if not self.SRP_g:
            raise ValueNotSetException('SRP_g')
        if not self.SRP_I:
            raise ValueNotSetException('SRP_I')
        if not self.SRP_s:
            raise ValueNotSetException('SRP_s')
        if not self.SRP_A:
            raise ValueNotSetException('SRP_A')
        if not self.SRP_B:
            raise ValueNotSetException('SRP_B')
        if not self.SRP_K:
            raise ValueNotSetException('SRP_K')
        SRP_nhash = hashlib.sha1(convertool.intToStr(self.SRP_N)[::-1]).digest()                                    # Calculates hashes of previous values
        SRP_ghash = hashlib.sha1(chr(self.SRP_g)).digest()
        SRP_userhash = hashlib.sha1(self.SRP_I).digest()      

        SRP_nghash = ""
        for i in range(20):                                                         # Xor n and g
            SRP_nghash += chr(ord(SRP_nhash[i]) ^ ord(SRP_ghash[i]))

        self.SRP_M1 =convertool.strToInt(hashlib.sha1(SRP_nghash + SRP_userhash + convertool.intToStr(self.SRP_s)[::-1] \
                        + convertool.intToStr(self.SRP_A)[::-1] \
                        + convertool.intToStr(self.SRP_B)[::-1] \
                        + convertool.intToStr(self.SRP_K)[::-1]).digest())

    def get_M1(self):
        if not self.SRP_M1:
            raise ValueNotSetException('SRP_M1')
        return self.SRP_M1

    def set_M1(self, M1):
        self.SRP_M1 = M1

    #SRP_M2
    def calculate_M2(self):
        self.SRP_M2 = convertool.strToInt(hashlib.sha1(convertool.intToStr(self.SRP_A)[::-1] \
                        + convertool.intToStr(self.SRP_M1) \
                        + convertool.intToStr(self.SRP_K)[::-1]).digest())
        print
        print(((convertool.intToStr(self.SRP_A)[::-1] \
                        + convertool.intToStr(self.SRP_M1) \
                        + convertool.intToStr(self.SRP_K)[::-1])).encode('hex'))
        print

        print(hashlib.sha1(convertool.intToStr(self.SRP_A)[::-1] \
                        + convertool.intToStr(self.SRP_M1) \
                        + convertool.intToStr(self.SRP_K)[::-1]).hexdigest())

    def get_M2(self):
        if not self.SRP_M2:
            raise ValueNotSetException('SRP_M2')
        return self.SRP_M2

    def set_M1(self, M2):
        self.SRP_M2 = M2
