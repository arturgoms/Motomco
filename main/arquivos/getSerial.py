__author__ = ["Artur Gomes", "github.com/arturgoms"]

import serial

windows = 'COM3'
linux = '/dev/serial0'

def getSerial(input): # Funcao que retorna o valor recebido na serial
    try:
        port = serial.Serial(linux, baudrate=115200, timeout=15)
        while True:
            port.write(input)
            resposta = port.read(64)
            if resposta == '':
                return('0BTIMEOUT##')
            else:
                return (resposta)
    except Exception as e:
        print("Erro' %s" % e)

def readHx(str): # Funcao que formata o valor do hx
    rscStm = None
    try:
        rscStm = str.split("split")
        rsp = rscStm[2]
        return(rsp[:5])
    except Exception as e:
        rsp = rscStm[0]
        return rsp

def readOsc(str): # Funcao que formata o valor da osciladora
    try:
        nChar = int(str[0:2], 16)
        respostaF = str[2:nChar-2]
        return(respostaF)
    except Exception as e:
        print("Erro' %s" % e)

def getBalanca(input): # Funcao que pega o valor da balanca
    try:
        port = serial.Serial(linux, baudrate=115200, timeout=10)
        while True:
            port.write(input)
            resposta = port.readline()
            if resposta == '':
                return('0BTIMEOUT##')
            else:
                return (resposta)
    except Exception as e:
        print("Erro' %s" % e)

def getTeste(input):
    try:
        port = serial.Serial(linux, baudrate=115200, timeout=12)
        while True:
            port.write(input)
            resposta = port.read(64)
            return (resposta)
    except Exception as e:
        print("Erro' %s" % e)
