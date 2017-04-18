from flask import flash

__author__ = ["Artur Gomes", "github.com/arturgoms"]

#!/usr/bin/python2.7
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from getSerial import *

def measure():
    while True:
        freqvBuffer = []
        for i in range(0, 4):
            print i
            freqvBruto = getSerial('07FREQV')
            if freqvBruto == '0BTIMEOUT##':
                print ('Freq TIMEOUT')
            else:
                freq = float(readOsc(freqvBruto))
                freqvBuffer.append(freq)
        try:
            if freq - 1000 > freqvBuffer[3]:
                break
            else:
                return 2
        except:
            return 0
    return 1
