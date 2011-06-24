CRYPTED_RECV_LEN = 4
data = list('acc44153'.decode("hex"))
key = '28af88e45560b9ab87d5fa8895690566fd5b44f6338f779b3b72798185040c2625b2c69156c285ee'.decode("hex")
recv_i = 0
recv_j = 0

for t in range(CRYPTED_RECV_LEN):
    recv_i %= len(key)
    x = (ord(data[t]) - recv_j) ^ ord(key[recv_i])
    recv_i += 1
    recv_j = ord(data[t])
    if x < 0:
        x += 256
    data[t] = x
    
for i in data:
    print hex(i),
