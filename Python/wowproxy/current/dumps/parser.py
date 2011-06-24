import psyco
psyco.full()

with open('dump-21-07-13-32.log') as f:
    while True:
        try:
            opcode = f.readline().split()[-1]
            size = f.readline().split()[-1]
            f.readline()
            data = ''
            line = f.readline().strip()
            while line:
                data += line[:48].replace(' ', '')
                line = f.readline().strip()
     
        except:
            break
