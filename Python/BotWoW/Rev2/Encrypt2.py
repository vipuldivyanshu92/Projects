data = '00043700'.decode("hex")
sessionkey = '390C1DAB3E2E370BFC9E6D083ABB253B4AEF57157B51C2C0DC12523B7C35FD3FCBCABED9666264D1'.decode("hex")[::-1]
send_i = 0
send_j = 0

print data

l_data = list(data[:4])                                                  # Only the header is encrypted
send_i = 0
result = ""                                                              # Init result variable
for t in range(4):                                                       # Length of the header is 4
    send_i %= len(sessionkey)                                                   #
    x = (ord(l_data[t]) ^ ord(sessionkey[send_i])) + send_j    # Calculate the xor value wrt the previous byte
    if x > 255:                                                          # Work all the time in a bytes
        x -= 256                                                         # Return the value as a overflown byte
    send_i += 1                                         
    send_j = x
    result += chr(x)

print data[4:]
v = result+data[4:]                                                   # Return the packet with the uncrypt part too
print v.encode("hex")
