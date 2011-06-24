CRYPTED_RECV_LEN = 4
data = list('00043700'.decode("hex"))
key = '390C1DAB3E2E370BFC9E6D083ABB253B4AEF57157B51C2C0DC12523B7C35FD3FCBCABED9666264D1'.decode("hex")[::-1]
send_i = 0
send_j = 0

print data

for t in range(CRYPTED_RECV_LEN):
    send_i %= len(key)
    x = (ord(data[t]) ^ ord(key[send_i])) + send_j
    if x > 255:
        x -= 256
    send_i += 1
    send_j = x
    data[t] = send_j
    
for i in data:
    print i
