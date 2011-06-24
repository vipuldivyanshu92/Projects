from construct import *

def string(name):
    return PascalString(name, length_field = UBInt16('length'))
