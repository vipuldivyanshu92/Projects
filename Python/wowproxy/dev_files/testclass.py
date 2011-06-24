class testclass:
    port = 8085

    def __init__(self):
        self.port = testclass.port
        testclass.port +=1

    def getport(self):
        return self.port

a = testclass()
print a.getport()

b = testclass()
print b.getport()
