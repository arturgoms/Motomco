
from flask import session

__author__ = ["Artur Gomes", "github.com/arturgoms"]

#!/usr/bin/python2.7
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from arquivos.umidade import *
from arquivos.jsonHandler import historic, cloud
from arquivos.rwconf import writeConf
import logging
import platform
import ctypes
system = platform.system()
freqv = 0
freqvBuffer = []

logger = logging.getLogger('log')

def initAutoTest():  # Funcao que realiza o autoteste

    global freqv
    global peso
    verifConfig = verifConf()
    print(verifConfig)

    if system == 'Windows':
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        #read resolution
        writeConf('DEFAULT', 'lcd_type', '5')

    elif system == 'Linux':
        class Command(object):
            def __init__(self, command):
                self.command = command

            def run(self, shell=True):
                import subprocess as sp
                process = sp.Popen(self.command, shell=shell, stdout=sp.PIPE, stderr=sp.PIPE)
                self.pid = process.pid
                self.output, self.error = process.communicate()
                self.failed = process.returncode
                return self

            @property
            def returncode(self):
                return self.failed

        com = Command("fbset -s").run()
        a = com.output
        d = a.find('x')

        resolution = a[d - 3:d + 4]
        w = resolution[:3]
        h = resolution[4:]

        if w == 800 and h == 480:
            writeConf('DEFAULT', 'lcd_type', '5')

    try:
        freqvBruto = getOsc('07FREQV')
        print freqvBruto
        if freqvBruto == '0BTIMEOUT##':
            logger.error("Autotest - Could not read the frequency value{}".format(freqvBruto))
            freqv = 1000
        else:
            freqv = float(readHx(freqvBruto))
            logger.info("Autotest - Frequency deals successfully {}".format(freqv))
            print (freqv)
    except:
        freqv = 1000
        writeConf('DEFAULT', 'AUTO-TEST', 'NO')
        writeConf('DEFAULT', 'ERRO-AUTO-TEST', 'ERRO-FREQ-TIMEOUT')
    try:
        tempaBruto = getOsc('07TEMPA')
        print tempaBruto
        if tempaBruto == '0BTIMEOUT##':
            logger.error("Autotest -Could not read temperature value {}".format(tempaBruto))
            tempa = 60
        else:
            tempa = float(readHx(tempaBruto))
            logger.info("Autotest - Temperature deals successfully {}".format(tempa))
            print (tempa)
    except:
        tempa = 60
        writeConf('DEFAULT', 'AUTO-TEST', 'NO')
        writeConf('DEFAULT', 'ERRO-AUTO-TEST', 'ERRO-TEMPA-TIMEOUT')
    try:
        pesoBruto = getHx('07PESO1')
        print pesoBruto
        if pesoBruto == '0BTIMEOUT##':
            logger.error("Autotest - Could not read balance value {}".format(pesoBruto))
            peso = 1000
        else:
            peso = float(readHx(pesoBruto))
            logger.info("Autotest - Weight read successfully {}".format(peso))
            print (peso)
    except:
        peso = 1000
        writeConf('DEFAULT', 'AUTO-TEST', 'NO')
        writeConf('DEFAULT', 'ERRO-AUTO-TEST', 'ERRO-PESO-TIMEOUT')

    if -20 <= peso <= 500:
        if 6000 <= freqv <=11000:
            if 15 <= tempa <= 30:
                writeConf('DEFAULT', 'AUTO-TEST', 'YES')
                writeConf('DEFAULT', 'ERRO-AUTO-TEST', 'NO')
                logger.info("Autotest - Autotest successfully done")
                return 1
            else:
                writeConf('DEFAULT', 'AUTO-TEST', 'NO')
                writeConf('DEFAULT', 'ERRO-AUTO-TEST', 'ERRO-TEMPE')
                erro = 'Erro na Temperatura'
                logger.error("Autotest - {}".format(erro))
                return(erro)
        else:
            writeConf('DEFAULT', 'AUTO-TEST', 'NO')
            writeConf('DEFAULT', 'ERRO-AUTO-TEST', 'ERRO-FREQ')
            erro = 'Erro na Frequencia'
            logger.error("Autotest - {}".format(erro))
            return(erro)
    else:
        writeConf('DEFAULT', 'AUTO-TEST', 'NO')
        writeConf('DEFAULT', 'ERRO-AUTO-TEST', 'ERRO-PESO')
        erro = 'Erro no Peso'
        logger.error("Autotest - {} - {}".format(erro, peso))
        return(erro)

def getFreq():  # Funcao que retorna o valor da frequencia
    try:
        freqvBruto = getOsc('07FREQV')
        freq = float(readHx(freqvBruto))
        return freq
    except:
         freqErro = readHx(freqvBruto)
         logger.error("Autotest - Could not read frequency - {}".format(freqErro))
         #print freqErro

def getPeso():  # Funcao que retorna o valor do Peso
    try:
        pesoBruto = getHx('07PESO1')
        peso = float(readHx(pesoBruto))
        return peso
    except:
         pesoErro = readHx(pesoBruto)
         logger.error("Autotest - Could not read weight - {}".format(pesoErro))
         #print pesoErro
def getTemp():  # Funcao que retorna o valor da Temperatura
    try:
        tempBruto = getOsc('07TEMPA')
        temp = float(readHx(tempBruto))
        return temp
    except:
        tempErro = readHx(tempBruto)
        logger.error("Autotest - Could not read temperature - {}".format(tempErro))
        #print tempErro

def measure():  # Funcao que retorna a situacao do copo
    global freqvBuffer
    global freqv
    global peso
    global status
    i = 0
    k = 0
    a =0
    freqv = 10911
    while True:
        freqvBruto = getFreq()
        #print (freqvBruto)
        if freqvBruto is not None:
            if freqvBuffer.__len__() < 3:
                try:
                    freqvBuffer.append(freqvBruto)
                except:
                    #print "Erro na leitura da Frequencia"
                    logger.error("Serial - Could not read the frequency")
            else:
                freqvBuffer.pop(0)
                freqvBuffer.append(freqvBruto)
                try:
                    if freqvBuffer[2] == -1002:
                        a = a + 1
                        if a > 2:
                            a = 0
                            return 4
                        #print 'Erro no crc'
                        #logger.error("Serial - CRC")
                    elif freqvBuffer[2] == -1003:
                        a = a + 1
                        if a > 2:
                            a = 0
                            return 5
                        #print 'Erro no Timeout da Osc'
                        #logger.error("Serial - Timeout da Osciladora")
                    elif freqvBuffer[2] == -1004:
                        a = a + 1
                        if a > 2:
                            a = 0
                            return 6
                        #print 'Erro na Criptografia'
                        #logger.error("Serial - Criptografia")
                    elif freqvBuffer[0] > 10000 and freqvBuffer[2] > 10000:
                        i = i + 1
                        if i > 2:
                            i = 0
                            return 1
                        #print 'Copo Vazio'
                    elif freqvBuffer[0] < 9000 and freqvBuffer[2] < 9000:
                        k = k + 1
                        if k > 2:
                            k = 0
                            return 2
                        #print 'Copo Cheio'
                    elif freqv - 1000 > freqvBuffer[2]:
                        return 3
                    else:
                        a = a + 1
                        if a > 2:
                            a = 0
                            return 7
                except:
                    #print 'Erro'
                    logger.critical("Serial - TIMEOUT")
        else:
            a = a + 1
            if a > 2:
                a = 0
                return 7

def umidade(curva, ph, freqv, freqc, pesoG, tempa, grupo):  # Funcao que calcula a umidade

    try:
        global umidadeCount
        global freqvBuffer
        try:
            calc = calcCapx(freqv, freqc)
        except Exception as a:
            logger.critical("Humidity - Error in calculating CapX - {}".format(a))
        try:
            dialx = getBasicInfoTop(0)
            dialy = (dialx[10])
            dial = float(dialy[0])
        except Exception as b:
            logger.critical("Humidity - Erro in catch dial of the chart - {}".format(b))
        try:
            dialCalculado = calcDial(calc, dial)
        except Exception as c:
            logger.critical("Humidity - Error in calculating Dial - {}".format(c))
        try:
            dialCorrigido = calcDialCorrigido(dialCalculado, pesoG)
        except Exception as d:
            logger.critical("Humidity - Error in calculating Dial - {}".format(d))
        try:
            umidade = calcUmidade(tempa, dialCorrigido)
        except Exception as e:
            logger.critical("Humidity - Error in calculating Humidity - {}".format(e))

        #print umidade
        freqvBuffer = []
        historico = historic()
        config = configparser.ConfigParser()
        config.read(confDir)
        umidadeCount = config.get('DEFAULT', 'CONTADOR')
        umidadeCount = int(umidadeCount) + 1
        writeConf('DEFAULT', 'CONTADOR', str(umidadeCount))
        try:
            historico.write(curva, umidade, tempa, ph, dialCalculado, dialCorrigido, freqc, freqv, pesoG, umidadeCount, grupo)
        except Exception as g:
            logger.critical("Humidity - Error writing history result - {}".format(g))
        try:
            clouds = cloud()
            username = session['username']
            clouds.save_result(curva, umidade, tempa, ph, dialCalculado, dialCorrigido,
                               freqc, freqv, pesoG, umidadeCount, grupo, username)
        except Exception as h:
            logger.critical("Humidity - Error writing result to be sent to the cloud - {}".format(h))
        return umidade
    except Exception as f:
        logger.critical("Humidity - Error in Function - {}".format(f))
        return 0

if __name__ == '__main__':
    a = initAutoTest()
    print a
