def modexp ( t, u, n ):
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

# Read a string from and return all char before 0x00
def ReadString(s):
   return s[:s.find(chr(0x00))]

# Convert a string to integer value
def StrToInt(s):
    return int(s.encode("hex"), 16)

# Convert an interger to a string
def IntToStr(v):
    u = hex(v)[2:-1]
    u = (len(u) % 2) * '0'+u
    return u.decode('hex')

# Convert a string to a nice hex output
def StrToProperHex(s):
    result = ''
    counter = 0
    for i in s:
        result += i.encode("hex")
        counter += 1
        if counter < 20:
            result += ' '
        else:
            result += '\n'
            counter = 0
    return result
