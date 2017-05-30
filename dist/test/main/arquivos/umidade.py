__author__ = ["Artur Gomes", "github.com/arturgoms"]

#!/usr/bin/python2.7
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from curvasHandler import getBasicInfoTop
from getSerial import readOsc, readHx, getSerial, getBalanca, getTeste
from SerialTTY import getOsc, getHx
from rwconf import *
from math import sqrt
import configparser
config = configparser.ConfigParser()

std_dial = []
eqp_freq = []

calc1 = 0
tabDir = 'main/arquivos/tab.txt'
confDir = 'main/conf.ini'
langDir = 'main/lang.ini'
topDir = 'main/arquivos/top.txt'

def calcUmidade(temp, dial): # dial corrigido

    global shiftMinDial
    global shiftMaxDial
    global DIAL_DIV_SHIFT
    global DIAL_ACT_STEP
    global shiftDialActMax
    global shiftDialActMin
    global coef
    global calc1
    coef = []
    DIAL_DIV_SHIFT = 40
    DIAL_ACT_STEP = 1
    shiftDialActMax = 215.0
    shiftDialActMin = -40
    curva = getBasicInfoTop(0)
    uniTemp = curva[8]

    if temp == 25:
        if uniTemp == 'C':
            temp = 25
        else:
            temp = 77
    else:
        if uniTemp == 'F':
            temp = (temp * 1.8) + 32

    paramPeso = getparamPesoCurva()
    for i in range(0, paramPeso.__len__()):
        coef.append(float(paramPeso[i]))

    parametro = curva[9]
    eqNum = int(parametro[0])

    parametro = curva[5]
    minDial = int(parametro[0]) + 40
    MaxDial = int(parametro[1]) + 40

    parametro = curva[2]
    minTemp = int(parametro[0])
    maxTemp = int(parametro[1])


    shiftMinDial = (minDial * DIAL_ACT_STEP) - DIAL_DIV_SHIFT
    shiftMaxDial = (MaxDial * DIAL_ACT_STEP) - DIAL_DIV_SHIFT

    # Se tipoDial = 1 calcula umidade normal, tipoDial = 0, calcula dial minimo e dial maximo


    return calcula(eqNum, temp, dial)


def calcula(eqNum, temp, dial): #precisa do corrigido
    global tempCalc
    global dialCalc
    tempCalc = temp
    dialCalc = dial
    global calc1
    switch = {1: eq1,
              2: eq2,
              3: eq3,
              4: eq4,
              5: eq5,
              6: eq6,
              7: eq7,
    }
    calc1 = switch[eqNum]()
    return calc1

def eq1():
    global coef
    calc1 = coef[4] * tempCalc + ((coef[3] * dialCalc + coef[2]) * dialCalc + coef[1]) * dialCalc + coef[0]
    return calc1
def eq2():
    global coef
    calc2 = ((((coef[5] * dialCalc + coef[4]) * dialCalc + coef[3]) * dialCalc + coef[2]) * dialCalc + coef[1]) * dialCalc + coef[0]
    calc3 = (((((coef[11] * tempCalc + coef[10]) * tempCalc + coef[9]) * tempCalc + coef[8]) * tempCalc + coef[7]) * tempCalc + coef[6]) * tempCalc
    calc1 = calc2 + calc3
    return calc1
def eq3():
    global coef
    calc2 = 1.0 + coef[4] * (22.0 - tempCalc)
    calc3 = coef[1] + coef[2] * ((dialCalc + coef[3] * (22.0 - tempCalc)) / calc2)
    calc1 = (coef[0] + sqrt(calc3)) / coef[5]
    return calc1

def eq4():
    global coef
    calc2 = 1.0 + coef[1] * (22.0 - tempCalc)
    calc3 = (dialCalc + coef[0] * (22.0 - tempCalc)) / calc2
    calc1 = ((coef[5] * calc3 + coef[4]) * calc3 + coef[3]) * calc3 + coef[2]
    return calc1
def eq5():

    global coef
    dial1 = coef[0]
    dial2 = coef[1]
    calc2 = shiftMinDial
    calc3 = shiftMaxDial
    if dialCalc < dial1:
        calc1 = coef[6] * tempCalc + ((coef[5] * dialCalc + coef[4]) * dialCalc + coef[3]) * dialCalc + coef[2]
    else:
        if(dialCalc >= dial1) and (dialCalc <= dial2):
            calc1 = coef[11] * tempCalc + ((coef[10] * dialCalc + coef[9]) * dialCalc + coef[8]) * dialCalc + coef[7]
        else:
            if dialCalc > dial2:
                calc1 = coef[16] * tempCalc + ((coef[15] * dialCalc + coef[14]) * dialCalc + coef[13]) * dialCalc + coef[12]
    return calc1
def eq6():
    calc2 = 22.0 - tempCalc
    calc1 = coef[0] + coef[1] * dialCalc + coef[2] * calc2 + coef[3] * dialCalc * calc2
    return calc1
def eq7():
    if tempCalc == 22.0:
        dial2 = dialCalc
    else:
        calc1 = coef[0] * (22.0 - tempCalc)
        calc2 = (coef[1] * (22.0 - tempCalc)) - 1.0
        calc3 = dialCalc + (coef[2] * (22.0 - tempCalc))
        dial1 = calc2 * calc2 - (4.0 * calc1 * calc3)
        dial2 = (-calc2 - sqrt(dial1)) / (2 * calc1)

    calc1 = ((coef[6] * dial2 + coef[5]) * dial2 + coef[4]) * dial2 + coef[3]
    return calc1

def calcCapx(freqVazio, freqAtual):
    calc = 0
    try:
        if freqAtual > 0:
            a = freqVazio - freqAtual
            b = freqAtual
            c = a/b
            d = c * 10000
            calc = float((float(freqVazio) - float(freqAtual)) / float(freqAtual)) * 10000
        else:
            calc = 0
        return calc
    except:
        calc = 999999
        return calc

def calcDial(capx, dialTabela):
    global std_dial
    global eqp_freq
    global dest_a
    global dest_b
    global orig_a
    global orig_b

    try:
        f = open(tabDir, 'r')
        for word in f:
            tab = word.split(";")
        for i in range(0, 11):
            a = tab[i]
            std_dial.append(a)
        for i in range(0, 11):
            eqp_freq.append(tab[i + 11])


        c = std_dial
        b = eqp_freq
        d = float(eqp_freq[10])
        if capx < (float(eqp_freq[0]) - 500):
            loadTable(0)
        elif (capx >= (float(eqp_freq[0]) - 500)) and (capx < float(eqp_freq[1])):
            loadTable(0)

        elif capx > (float(eqp_freq[10]) + 300):
            loadTable(9)

        elif (capx >= float(eqp_freq[9])) and (capx <= (float(eqp_freq[10]) + 300)):
            loadTable(9)
        else:
            for addr in range(1, 8):
                if (capx >= float(eqp_freq[addr])) and (capx < float(eqp_freq[addr + 1])):
                    loadTable(addr)
                    break
        dest_a = float(dest_a)
        orig_b = float(orig_b)
        dest_b = float(dest_b)
        dest_aN = float(-dest_a)
        dest_bN = float(-dest_b)
        orig_a = float(orig_a)
        orig_aN = float(-orig_a)
        orig_b = float(orig_b)

        dial_x = (((dest_a * orig_b) + (dest_b * capx)) + ((dest_aN * capx) + (dest_bN * orig_a))) / (orig_aN + orig_b)
        dial_x = dial_x + float(dialTabela) - 53.0
        return dial_x
    except Exception as e:
        print("Erro' %s" % e)

def calcDialCorrigido(dial, peso):
    global coef
    coef = []
    pesoFull = getPesoCurva()
    peso_corr = float(pesoFull[0])

    massa_memoria = 0
    cont_erro = 0
    delta = 0
    flag_primeira = True

    paramPeso = getparamPesoCurva()
    for i in range(0, paramPeso.__len__()):
        coef.append(float(paramPeso[i]))

    lin_x3 = coef[17]
    lin_x2 = coef[18]
    lin_x = coef[19]
    lin = coef[20]
    ang_x3 = coef[21]
    ang_x2 = coef[22]
    ang_x = coef[23]
    ang = coef[24]
    corr_x3 = coef[25]
    corr_x2 = coef[26]
    corr_x = coef[27]
    corr = coef[28]

    while True:
        coef_lin = (lin_x3 * (delta ** 3)) + (lin_x2 * (delta ** 2)) + (lin_x * delta) + lin
        coef_ang = (ang_x3 * (delta ** 3)) + (ang_x2 * (delta ** 2)) + (ang_x * delta) + ang
        massa_teste = coef_ang * dial + coef_lin

        if flag_primeira == True:
            flag_primeira = False
            massa_memoria = massa_teste
        if (massa_teste < peso) and (massa_memoria > peso):
            delta = delta - 2

            while True:
                coef_lin = (lin_x3 * (delta ** 3)) + (lin_x2 * (delta ** 2)) + (lin_x * delta) + lin
                coef_ang = (ang_x3 * (delta ** 3)) + (ang_x2 * (delta ** 2)) + (ang_x * delta) + ang
                massa_teste = coef_ang * dial + coef_lin

                if (peso < (massa_teste + 0.01)) and (peso > (massa_teste - 0.01)):
                    DIAL_PRECORR = ((peso_corr - coef_lin) / coef_ang)
                    break

                delta = delta + 0.001
                cont_erro = cont_erro + 1

                if cont_erro == 30000:
                    return 9999
            break
        else:
            massa_memoria = massa_teste
            delta = delta + 2
        cont_erro = cont_erro + 1
        if cont_erro == 30000:
            return 9999
    val_correcao = (corr_x3 * (DIAL_PRECORR ** 3)) + (corr_x2 * (DIAL_PRECORR ** 2)) + (corr_x * DIAL_PRECORR) + corr
    if peso < peso_corr:
        peso_diferenca = peso_corr - peso
        DIAL_diferenca = peso_diferenca * val_correcao
        DIAL_retorno = DIAL_PRECORR - DIAL_diferenca
    elif peso > peso_corr:
        peso_diferenca = peso - peso_corr
        DIAL_diferenca = peso_diferenca * val_correcao
        DIAL_retorno = DIAL_PRECORR + DIAL_diferenca
    else:
        DIAL_retorno = DIAL_PRECORR

    return DIAL_retorno



def loadTable(id):
    global std_dial
    global eqp_freq
    global dest_a
    global dest_b
    global orig_a
    global orig_b
    try:
        dest_a = std_dial[id]
        dest_b = std_dial[id + 1]
        orig_a = eqp_freq[id]
        orig_b = eqp_freq[id + 1]
    except:
        print 'Deu ruim na tabela'

def calcPH(peso):
    config.read(confDir)
    tipoPH = config.get('DEFAULT', 'PH')
    pesoPH = peso / 3.273405

    if tipoPH == 'lb/bu':
        pesoPH = pesoPH / 1.247
    elif tipoPH == 'lb/A bu':
        pesoPH = pesoPH / 1.247
    elif tipoPH == 'lb/W bu':
        pesoPH = pesoPH * 0.1552

    pesoPH = format(pesoPH, '.2f')
    pesoPHformat = str(pesoPH) + ' ' + tipoPH

    return float(pesoPH)



def getDialCurva():
    curva = getBasicInfoTop(0)
    dial = curva[5]
    return dial
def getPesoCurva():
    curva = getBasicInfoTop(0)
    peso = curva[7]
    return peso
def getparamPesoCurva():
    curva = getBasicInfoTop(0)
    paramPeso = curva[6]
    return paramPeso


def VerifTab():

    tabBruto = []
    try:
        with open(tabDir, 'r') as f:
            tabBruto = getTeste('07R_TAB')
            tab = readHx(tabBruto)
            return '1'
    except IOError:
        with open(tabDir, 'w') as configfile:
            config.write(configfile)
            tabBruto = getTeste('07R_TAB')
            tab = readHx(tabBruto)
        return '0'

if __name__ == '__main__':
    dialx = getBasicInfoTop(0)
    dial = (dialx[10])
    print int(dial[0])