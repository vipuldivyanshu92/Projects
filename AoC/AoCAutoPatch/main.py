#!/usr/bin/env python

import md5
import sys
import os

FUNCOM_KEY = '9c32cc23d559ca90fc31be72df817d0e124769e809f936bc14360ff4bed758f260a0d596584eacbbc2b88bdd410416163e11dbf62173393fbc0c6fefb2d855f1a03dec8e9f105bbad91b3437d8eb73fe2f44159597aa4053cf788d2f9d7012fb8d7c4ce3876f7d6cd5d0c31754f4cd96166708641958de54a6def5657b9f2e92'
FAOLAN_KEY = '26b5a3b4ac1177f24a2d9de44bafef477ff23ef1cb5f646919b1be26516053030b65d5afb60cef6f49de539958ba0b7922a099319b8016a8673cb27a696ae4b60fdece25ddcdad42e7f0056b87fc35687fe033b242e17e960d79806fd46c4a79cbc64f558660a50cabc1c242dace70de6af452e3433f97e30e202567f187de70'

def md5File(filename):
    f = open(filename, 'rb')
    sum = md5.new(f.read()).hexdigest()
    f.close()
    return sum

sums = {}
path = sys.argv[1]
serv = sys.argv[2]

print "Retrieving AgeOfConan.exe MD5"
sums["AgeOfConan.exe_ORG"] = md5File(path+"\AgeOfConan.exe")
print sums["AgeOfConan.exe_ORG"]
print

print "Modifying AgeOfConan.exe public key"
f = open(path+"\AgeOfConan.exe", 'rb')
content = f.read()
pos = content.find(FUNCOM_KEY)
f.close()
if pos == -1:
    print "Unable to find the Key maybe the EXE is already patched."
else:
    print "Key found at position %d." % (pos)
    f = open(path+"\AgeOfConan.exe", 'wb')
    f.write(content.replace(FUNCOM_KEY, FAOLAN_KEY))
    f.close()
print

print "Retrieving new AgeOfConan.exe MD5"
sums["AgeOfConan.exe_MOD"] = md5File(path+"\AgeOfConan.exe")
print sums["AgeOfConan.exe_MOD"]
print

print "Modifying FileHashes"
f = open(path+"\FileHashes", 'rb')
content = f.read()
pos = content.find(sums["AgeOfConan.exe_ORG"].decode("hex"))
f.close()
if pos == -1:
    print "Unable to find the Original AgeOfConan.exe MD5 maybe already patched."
else:
    print "Key found at position %d." % (pos)
    f = open(path+"\FileHashes", 'wb')
    f.write(content.replace(sums["AgeOfConan.exe_ORG"].decode("hex"), sums["AgeOfConan.exe_MOD"].decode("hex")))
    f.close()
print

print "Modifying LocalConfig.xml"
f = open(path+"\LocalConfig.xml", 'r')
content = f.read()
pos = content.find('aoc-eu-update.live.ageofconan.com')
if pos == -1:
    print "Error, maybe already patched"
else:
    content = content.replace('aoc-eu-update.live.ageofconan.com', serv)
pos = content.find('aoc-eu-gameupdate.live.ageofconan.com')
if pos == -1:
    print "Error, maybe already patched"
else:
    content = content.replace('aoc-eu-gameupdate.live.ageofconan.com', serv)
pos = content.find('aoc-eu-control.live.ageofconan.com')
if pos == -1:
    print "Error, maybe already patched"
else:
    content = content.replace('aoc-eu-control.live.ageofconan.com', serv)
pos = content.find('aoc-eu-um.live.ageofconan.com')
if pos == -1:
    print "Error, maybe already patched"
else:
    content = content.replace('aoc-eu-um.live.ageofconan.com', serv)
f = open(path+"\LocalConfig.xml", 'w')
f.write(content)
f.close()
print

print "Retrieving FileHashes MD5"
sums["FileHashes"] = md5File(path+"\FileHashes")
print sums["FileHashes"]
print

print "Retrieving ConanPatcher.exe MD5"
sums["ConanPatcher"] = md5File(path+"\ConanPatcher.exe")
print sums["ConanPatcher"]
print

print "Retrieving PatcherSetup.exe MD5"
sums["PatcherSetup"] = md5File(path+"\PatcherSetup.exe")
print sums["PatcherSetup"]
print

print "Retrieving RDBHash MD5"
print "TODO : Identify concerned file(s)"
sums["RDBHash"] = raw_input("RDBHash = ")
print sums["RDBHash"]
print

print "Retrieving RDBHashIndex.bin MD5"
sums["RDBHashIndex"] = md5File(path+"\RDB\\RDBHashIndex.bin")
print sums["RDBHashIndex"]
print

print "Creating Tree"
try:
    os.mkdir("www")
except Exception, err:
    print err
try:
    os.mkdir("www\\upm")
except Exception, err:
    print err
try:
    os.mkdir("www\\upm\\AoCLiveEU")
except Exception, err:
    print err
try:
    os.mkdir("www\\upm\\client")
except Exception, err:
    print err
try:
    os.mkdir("www\\upm\\client\\%s" % (sums["FileHashes"][0:2]))
except Exception, err:
    print err
print

print "Creating PatchInfoClient.txt"
content = """RootHash=%s
PatchVersion=x%s
PatcherSetupHash=%s
RDBHash=%s
RDBHash-5=%s""" % (sums["FileHashes"].lower(), sums["ConanPatcher"].lower(), sums["PatcherSetup"].lower(), sums["RDBHash"].lower(), sums["RDBHashIndex"].lower())
f = open("www\\upm\\AoCLiveEU\\PatchInfoClient.txt", 'w')
f.write(content)
f.close()
print

print "Copying LocalConfig.xml"
f = open(path+"\LocalConfig.xml", 'r')
content = f.read()
f.close()
f = open("www\\upm\\AoCLiveEU\\LocalConfig.xml", 'w')
f.write(content)
f.close()
print

print "Copying FileHashes"
f = open(path+"\FileHashes", 'r')
content = f.read()
f.close()
f = open("www\\upm\\client\\%s\\%s" % (sums["FileHashes"].lower()[0:2], sums["FileHashes"].lower()[2:]), 'w')
f.write(content)
f.close()
