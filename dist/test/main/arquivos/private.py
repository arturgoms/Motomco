import hashlib
import random
import time
import pyqrcode
import binascii
import configparser
from operator import xor
import numpy

confDir = 'main/conf.ini'
global table

class token:

    def gera(self, paramSetup):
        """
           :rtype: object
        """
        acessBalanca = 1
        acessCalibracao = 2
        acessData = 4
        acessInstall = 8
        acessSumary = 16
        acessClear = 32
        acessCharts = 64
        acessAll = 128
        acessPrivate = 256
        acessMotors = 512
        conf = configparser.ConfigParser()
        conf.read(confDir)
        sn = conf.get('DEFAULT', 'nserie')
        random.random()

        lbToken = hex(random.randint(0, 1048575))
        lbToken = lbToken[2:]
        #print 'antes  ' + lbToken
        while lbToken.__len__() < 5:
            lbToken += '0'
        #print 'depois  ' + lbToken

        t = hex(paramSetup)
        x = t.find('x')
        t = t[x+1:]
        u = t.__len__()
        if u == 1:
            acesso = '00'+ t
        elif u == 2:
            acesso = '0' + t
        elif u == 3:
            acesso = t

        y = lbToken.find("x")
        lbToken = acesso + lbToken.upper()
        tokenn=token()
        senha = tokenn.verifica(lbToken)
        code = sn + ";" + lbToken + ";" + senha[:-1]
        return code

    def verifica(self, key): # 5523B7D9
        global table
        senha = token()
        #print key
        #key = '100428C7' #senha.gera()
        #print key
        conf = configparser.ConfigParser()
        conf.read(confDir)
        sn = conf.get('DEFAULT', 'nserie')
        x = sn + key
        #print x
        y = bytearray()
        y.extend(str(x))
        shufle = bytearray()
        shufle.insert(0,y[8])
        shufle.insert(1,y[9])
        shufle.insert(2,y[7])
        shufle.insert(3,y[10])
        shufle.insert(4,y[6])
        shufle.insert(5,y[11])
        shufle.insert(6,y[5])
        shufle.insert(7,y[12])
        shufle.insert(8,y[4])
        shufle.insert(9,y[13])
        shufle.insert(10,y[3])
        shufle.insert(11,y[14])
        shufle.insert(12,y[2])
        shufle.insert(13,y[15])
        shufle.insert(14,y[1])
        shufle.insert(15,y[16])
        shufle.insert(16,y[0])
        shufle.insert(17,y[17])


        pas = bytearray()
        pas.extend(hashlib.sha1(shufle).digest())
        pas1 = bytearray()
        pas1.extend(hashlib.sha1(shufle).hexdigest())
        d = pas.__len__()
        c = bytearray()
        c.extend(key)
        soma = 0
        for j in range(0, c.__len__()):
            soma += c[j]

        senha.make_table(soma)
        password = senha.crc32(pas)
        strPass = hex(password)

        if strPass[0] == '-':
            strPass = strPass[3:]
        else:
            strPass = strPass[2:]
        return strPass.upper()

    def make_table(self, sh1):
        global table
        poly = 0xedb88320 + sh1
        table = [0] * 256
        for i in range(256):
            crc = i
            for j in range(8):
                if crc & 1:
                    crc = ((crc >> 1) & 0x7FFFFFFF) ^ poly
                else:
                    crc = ((crc >> 1) & 0x7FFFFFFF)
            table[i] = crc
        return table

    def crc32(self, byte):

        global table
        data = bytearray()
        data.extend(byte)
        crc = 0xFFFFFFFF
        for i in range(0, byte.__len__()):
            t = crc & 255
            a = byte[i]
            u = int(byte[i])
            index = bytes(t ^ u)
            crc = int((crc >> 8) ^ table[int(index)])

        return(~crc & 0xFFFFFFFF)

if '__main__'== __name__:
    while (1):
        senha = token()
        a = senha.gera(128)
        print a
        time.sleep(1)