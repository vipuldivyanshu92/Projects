#!/usr/bin/env python

import random

class SRPClient:
    def __init__(self):
        self.SRPk = 3
        self.SRPa = random.getrandbits(152)
    
    def setUsername(self, value):
        self.username = value
    
    def getUsername(self):
        return self.username
    
    def setPassword(self, value):
        self.password = value
    
    def setSRPb(self, value):
        self.SRPb = value
        
    def getSRPb(self):
        return self.SRPb
    
    def setSRPg(self, value):
        self.SRPg = value
        
    def getSRPg(self, value):
        return self.SRPg
    
    def setSRPn(self, value):
        self.SRPn = value
        
    def getSRPn(self, value):
        return self.SRPn
    
    def setSRPk(self, value):
        self.SRPk = value
        
    def getSRPk(self, value):
        return self.SRPk
    
    def setSRPsalt(self, value):
        self.SRPsalt = value
        
    def getSRPsalt(self, value):
        return self.SRPsalt
    
    def setSRPa(self, value):
        self.SRPa = value
        
    def getSRPa(self, value):
        return self.SRPa
    
    def setSRPA(self, value):
        self.SRPA = value
        
    def getSRPA(self, value):
        return self.SRPA
    
    def setSRPx(self, value):
        self.SRPx = value
        
    def getSRPx(self, value):
        return self.SRPx
    
    def setSRPv(self, value):
        self.SRPv = value
        
    def getSRPv(self, value):
        return self.SRPv
    
    