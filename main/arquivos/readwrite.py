#!/usr/bin/python3
# Arquivo para teste de serial, nao faz parte do programa principal
# Author: Artur Gomes
import serial
#from time import sleep

def get():
    comando = raw_input("Insira o comando:")
    resposta = getSerial(comando)

    print resposta


def getSerial(input):
    try:
        port = serial.Serial('COM3', baudrate=115200, timeout=100)
        while True:
            port.write(input)

            resposta = port.read(64)
            return (resposta)
    except Exception as e:
        print("Erro' %s" % e)
def readHx(str):
    rscStm = str.split("split")
    rsp = rscStm[2]
    return(rsp[:5])

def getHx(input):
    try:
        port = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=5)
        while True:
            port.write(input)
            resposta = port.read(64)
            if resposta == '':
                return('0BTIMEOUT##')
            else:
                return (resposta)
    except Exception as e:
        print("Erro' %s" % e)

def readOsc(str):
    respostaF = str[2:6]
    return(respostaF)

if __name__ == '__main__':
    a = getSerial("07FREQV")
    print a