import hashlib
import struct

username = "TEST"
password = "TEST"
salt = "AC4DA052B28A87729D75C838095F62384A1CEDD5450C01D65449021DF4C1BFB7"

temp = username+":"+password
temphash = hashlib.sha1(temp.upper()).digest()
print temphash

salt = salt.decode("hex")
salt = salt[::-1]
print salt

#print temphash.encode("hex")
x = hashlib.sha1(salt+temphash).digest()[::-1]
print x.encode("hex")

data = struct.unpack('<BBB32sBBB32s32s16sx', '000000a9b3c34a00726db05914b86f92afde9a740c6216a798dc540aca8760f3701245010720b79b3e2a87823cab8f5ebfbf8eb10108535006298b5badbd5b53e1895e644b8979875b060f78ac719f1cedeaeadbbb7c127f4828dfd71616915054f9dae419895b1e510e3dc1940b77440c07e590e5e700'.decode("hex"))
print data
salt = data[8][::-1]
print salt.encode("hex")
