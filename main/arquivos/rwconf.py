#Author: Artur Gomes
import fileinput
import configparser

config = configparser.ConfigParser()
from curvasHandler import *
import logging

confDir = 'main/conf.ini'
langDir = 'main/lang.ini'
topDir = 'main/arquivos/top.txt'
logger = logging.getLogger('log')
def verifConf(): # verifica se existe o arquivo conf.ini, se nao tiver ele cria

    try:
        with open(confDir, 'r') as f:
            logger.info("RWconf - Conf.ini file found")
            return 0

    except IOError:
        config['DEFAULT'] = {'File': 'YES', 'AUTO-TEST': 'NO', 'ERRO-AUTO-TEST': 'ERRO', 'PH': 'kg/hl', 'LANG': 'PT', 'CONTADOR': 0,
                             'uniTemp': 'C', 'FIRST-TIME': 'YES', 'MEDIA': 'NO', 'lcd_type': '5'}

        with open(confDir, 'w') as configfile:
            config.write(configfile)
        logger.info("RWconf - Conf.ini file not found, but successfully created")
        return 1

def writeConf(section='DEFAULT', nome='nome', valor='NO'): # funcao para escrever no arquivo conf.ini
    config.read(confDir)
    config[section][nome] = valor
    with open(confDir, 'w') as configfile:
        config.write(configfile)

def verifTop5(): # verifica se existe o arquivo top5.txt se nao tiver ele cria
    try:
        with open(topDir, 'r') as f:
            return '1'
    except IOError:
        with open(topDir, 'w') as configfile:
            config.write(configfile)
        return '0'

def writeTop5(curva): # escreve no arquivo top 5, joga a curva pra posicao numero 0 e deleta a ultima
    curvaTop5 = [5]
    f = open(topDir, 'r+')
    first_line = f.readline()
    lines = f.readlines()
    f.seek(0)
    f.write(curva)
    f.write(first_line)
    f.writelines(lines)
    with open(topDir) as f:
        top5len = sum(1 for _ in f)
    for i in range(top5len, 5, -1):
        lines = file(topDir, 'r+').readlines()
        del lines[-1]
        file(topDir, 'w').writelines(lines)
    f.close()
    return top5len

def writeTop5Top(curva, a): # escreve no arquivo top5 porem quando e clicado da lista top 5, deleta a curva clicada e adiciona por cima
    f = open(topDir, 'r+')
    first_line = f.readline()
    lines = f.readlines()
    f.seek(0)
    f.write(curva)
    f.write(first_line)
    f.writelines(lines)
    with f as f:
        top5len = file_len(topDir)
    for i in range(top5len,5,-1):
        lines = file(topDir, 'r+').readlines()
        del lines[a+1]
        file(topDir, 'w').writelines(lines)

    f.close()
    return top5len

def writeTop5Handler(curva, a): # escreve no arquivo top5 porem quando e clicado da lista top 5, deleta a curva clicada e adiciona por cima
    f = open(topDir, 'r+')
    first_line = f.readline()
    lines = f.readlines()
    f.seek(0)
    f.write(curva)
    f.write(first_line)
    f.writelines(lines)
    with f as f:
        top5len = file_len(topDir)
    for i in range(top5len, 5, -1):
        lines = file(topDir, 'r+').readlines()
        del lines[a+1]
        file(topDir, 'w').writelines(lines)

    f.close()
    return top5len