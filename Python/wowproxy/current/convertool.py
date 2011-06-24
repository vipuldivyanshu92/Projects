import math
import string

# Convert a string to integer value
def strToInt(s):
    return int(s.encode("hex"), 16)

# Convert an int to hex with specified length
def intToHex(v, l):
    h = '%x' % (v)
    h = '0' * (l-len(h)) + h
    return h

# Convert an interger to a string
def intToStr(v):
    u = '%x' % v
    u = (len(u) % 2) * '0' + u
    return u.decode('hex')

PRINTABLE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
def strToProperHex(s):
    def printableString(s):
        result = ''
        for c in s:
            result += '%s' % c if c in PRINTABLE else '.'
        return result

    def nonChaoticHex(s):
        result = ''
        for i in range(0, len(s), 2):
            result += s[i:i+2] + ' '
        return result
        
    number_of_lines = int(math.ceil(len(s) / 16.0))
    result = ''
    for current_line in range(number_of_lines):
        hexresult = nonChaoticHex(s[current_line*16:current_line*16+16].encode('hex'))
        clrresult = printableString(s[current_line*16:current_line*16+16])
        result += '%-48s| %-16s\n' % (hexresult, clrresult)
    return result
