__author__ = ["Artur Gomes", "github.com/arturgoms"]

import configparser
import json
from time import gmtime, strftime
from arquivos.SerialTTY import gps
from flask import session
import json
import logging
logger = logging.getLogger('log')
import urllib2



confDir = 'main/conf.ini'
langDir = 'main/lang.ini'
historicDir = 'main/arquivos/historic.json'
cloudDir = 'main/arquivos/cloud.json'
cloudTempDir = 'main/arquivos/cloudTemp.json'

config = configparser.ConfigParser()

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


class historic:
    @staticmethod
    def verif():

        data = []
        try:
            with open(historicDir, 'r') as f:
                return '1'
        except IOError:
            with open(historicDir, 'w') as hist:
                json.dump(data, hist, indent=4, sort_keys=True, separators=(',', ':'))
                return '0'

    def write(self, curva, umidade, temperatura, ph, dial, dialc, freqc, freqv, peso, contador, grupo):
        historic.verif()
        f = open(historicDir, 'r')
        dataJson = json.load(f)
        teste = len(dataJson)
        count = 0
        tipo = 0
        try:
            lat = float(gps.lat())
            lng = float(gps.log())
            logger.info("GPS - Working")
        except:
            lat = 0
            lng = 0
            logger.error("GPS - Error finding signal")
        for i in range(teste):
            data = dataJson[i]
            if data['nome'] == curva:
                now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                if grupo == "ARROZ":
                    data['grupo'].insert(0, 0)
                elif grupo == "FEIJAO":
                    data['grupo'].insert(0, 1)
                elif grupo == "GIRASSOL":
                    data['grupo'].insert(0, 2)
                elif grupo == "MILHO":
                    data['grupo'].insert(0, 3)
                elif grupo == "OUTROS":
                    data['grupo'].insert(0, 4)
                elif grupo == "SOJA":
                    data['grupo'].insert(0, 5)
                elif grupo == "TRIGO":
                    data['grupo'].insert(0, 6)
                elif grupo == "CUSTOM":
                    data['grupo'].insert(0, 7)
                gpsStr = {'value': float(umidade), "context": {'lat': lat, 'lng': lng}}
                data['umidade'].insert(0, gpsStr)
                data['temperatura'].insert(0, temperatura)
                data['ph'].insert(0, ph)
                data['dial'].insert(0, dial)
                data['dialc'].insert(0, dialc)
                data['freqc'].insert(0, freqc)
                data['freqv'].insert(0, freqv)
                data['peso'].insert(0, peso)
                data['contador'].insert(0, contador)
                data['time'].insert(0, now)
                user = session['username']
                user = user.encode('ascii', 'ignore')
                data['user'].insert(0, user)
                dataJson.insert(0, data)
                dataJson.pop(i+1)
                count = 1
                break

        if count == 0:
            if grupo == "ARROZ":
                tipo = 0
            elif grupo == "FEIJAO":
                tipo = 1
            elif grupo == "GIRASSOL":
                tipo = 2
            elif grupo == "MILHO":
                tipo = 3
            elif grupo == "OUTROS":
                tipo = 4
            elif grupo == "SOJA":
                tipo = 5
            elif grupo == "TRIGO":
                tipo = 6
            elif grupo == "CUSTOM":
                tipo = 7
            user = session['username']
            now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            add = {"type": "", "key": "value", 'nome': curva,
                   'umidade': [{'value': float(umidade), "context": {'lat': lat, 'lng': lng}}], 'temperatura': [temperatura], 'ph': [ph], 'dial': [dial], 'dialc': [dialc],
                   'freqc': [freqc], 'freqv': [freqv], 'peso': [peso], 'contador': [contador], 'time': [now], 'grupo': [tipo], 'user': [user]}
            dataJson.insert(0, add)
            with open(historicDir, 'w') as f:
                json.dump(dataJson, f, indent=4, sort_keys=True, separators=(',', ':'))


        else:
            with open(historicDir, 'w') as f:
                json.dump(dataJson, f, indent=4, sort_keys=True, separators=(',', ':'))

    @staticmethod
    def read():
        f = open(historicDir, 'r')
        count = 0
        historico = []
        dataJson = json.load(f)
        dataJsonlen = len(dataJson)
        for k in range(dataJsonlen):
            data = dataJson[k]
            datalen = len(data['contador'])
            for i in range(datalen):
                name = data['nome']
                try:
                    dataStr = name.encode(encoding='UTF-8', errors='strict') + ';' + str(
                        data['umidade'][i]['value']) + ';' + str(data['temperatura'][i]) + ';' + str(data['ph'][i]) + ';' + str(
                        data['dial'][i]) + ';' + str(data['dialc'][i]) + ';' + str(data['freqc'][i]) + ';' + str(
                        data['freqv'][i]) + ';' + str(data['peso'][i]) + ' ;' + str(data['contador'][i]) + ';' + str(
                        data['time'][i]) + ';' + str(data['grupo'][0]) + ';' + str(data['umidade'][i]['context']['lat']) + ';' + str(data['umidade'][i]['context']['lng'])
                except:
                    dataStr = name.encode(encoding='UTF-8', errors='strict') + ';' + str(
                        data['umidade'][i]) + ';' + str(data['temperatura'][i]) + ';' + str(data['ph'][i]) + ';' + str(
                        data['dial'][i]) + ';' + str(data['dialc'][i]) + ';' + str(data['freqc'][i]) + ';' + str(
                        data['freqv'][i]) + ';' + str(data['peso'][i]) + ';' + str(data['contador'][i]) + ';' + str(
                        data['time'][i]) + ';' + str(data['grupo'][0])

                historico.append(dataStr)
                count = count +1

        return historico

class cloud:

    @staticmethod
    def verif():

        data = []
        try:
            with open(cloudDir, 'r') as f:
                return '1'
        except IOError:
            with open(cloudDir, 'w') as jsonCloud:
                json.dump(data, jsonCloud, indent=4, sort_keys=True, separators=(',', ':'))
                return '0'

    def user_register(self, username, firstname, lastname, password, nserie):
        cloud.verif()
        f = open(cloudDir, 'r')
        dataJson = json.load(f)
        lenCloud = len(dataJson)
        count = 0
        tipo = 0

        for i in range(lenCloud):
            data = dataJson[i]
            if data['username'] == username:
                now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                data['firstname'].insert(0, firstname)
                data['lastname'].insert(0, lastname)
                data['password'].insert(0, password)
                data['time'].insert(0, now)
                count = 1

        if count == 0:
            now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            add = {'username': username, 'nserie': nserie, 'fisrtname': [firstname], 'lastname': [lastname], 'password': [password], 'result': [{"nome": ""}]}
            dataJson.insert(0, add)
            with open(cloudDir, 'w') as f:
                json.dump(dataJson, f, indent=4, sort_keys=True, separators=(',', ':'))
        else:
            with open(cloudDir, 'w') as f:
                json.dump(dataJson, f, indent=4, sort_keys=True, separators=(',', ':'))


    @staticmethod
    def read():
        f = open(cloudDir, 'r')
        count = 0
        historico = []
        dataJson = json.load(f)
        dataJsonlen = len(dataJson)
        for k in range(dataJsonlen):
            data = dataJson[k]
            historico.append(data)
            count = count + 1

        return historico

    def save_result(self, curva, umidade, temperatura, ph, dial, dialc, freqc, freqv, peso, contador, grupo, username):
        cloud.verif()
        f = open(cloudDir, 'r')
        dataJson = json.load(f)
        teste = len(dataJson)
        count = 0
        tipo = 0
        for i in range(teste):
            data = dataJson[i]
            if data['username'] == username:
                a = curva
                b = data['result']
                c = data['result'][0]['nome']

                if data['result'][0]['nome'] == curva:
                    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    if grupo == "ARROZ":
                        data['result'][0]['grupo'].insert(0, 0)
                    elif grupo == "FEIJAO":
                        data['result'][0]['grupo'].insert(0, 1)
                    elif grupo == "GIRASSOL":
                        data['result'][0]['grupo'].insert(0, 2)
                    elif grupo == "MILHO":
                        data['result'][0]['grupo'].insert(0, 3)
                    elif grupo == "OUTROS":
                        data['result'][0]['grupo'].insert(0, 4)
                    elif grupo == "SOJA":
                        data['result'][0]['grupo'].insert(0, 5)
                    elif grupo == "TRIGO":
                        data['result'][0]['grupo'].insert(0, 6)
                    elif grupo == "CUSTOM":
                        data['result'][0]['grupo'].insert(0, 7)
                    try:
                        lat = float(gps.lat())
                        lng = float(gps.log())
                        logger.info("GPS - Working")
                    except:
                        lat = 0
                        lng = 0
                        logger.error("GPS - Error finding signal")

                    gpsStr = {'value': float(umidade), "context": {'lat': lat, 'lng': lng}}

                    data['result'][0]['umidade'].insert(0, gpsStr)
                    data['result'][0]['temperatura'].insert(0, temperatura)
                    data['result'][0]['ph'].insert(0, ph)
                    data['result'][0]['dial'].insert(0, dial)
                    data['result'][0]['dial_corrigido'].insert(0, dialc)
                    data['result'][0]['frequencia_cheio'].insert(0, freqc)
                    data['result'][0]['frequencia_vazio'].insert(0, freqv)
                    data['result'][0]['peso'].insert(0, peso)
                    data['result'][0]['contador'].insert(0, contador)
                    data['result'][0]['time'].insert(0, now)
                    count = 1

                if count == 0:
                    if grupo == "ARROZ":
                        tipo = 0
                    elif grupo == "FEIJAO":
                        tipo = 1
                    elif grupo == "GIRASSOL":
                        tipo = 2
                    elif grupo == "MILHO":
                        tipo = 3
                    elif grupo == "OUTROS":
                        tipo = 4
                    elif grupo == "SOJA":
                        tipo = 5
                    elif grupo == "TRIGO":
                        tipo = 6
                    elif grupo == "CUSTOM":
                        tipo = 7

                    try:
                        lat = float(gps.lat())
                        lng = float(gps.log())
                        logger.info("GPS - Working")
                    except:
                        lat = 0
                        lng = 0
                        logger.error("GPS - Error finding signal")

                    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    add = {'nome': curva,'umidade': [{'value': float(umidade), "context": {'lat': lat, 'lng': lng}}], 'temperatura': [temperatura], 'ph': [ph], 'dial': [dial], 'dial_corrigido': [dialc],
                           'frequencia_cheio': [freqc], 'frequencia_vazio': [freqv], 'peso': [peso], 'contador': [contador], 'time': [now], 'grupo': [tipo]}
                    data['result'].insert(0, add)
                    with open(cloudDir, 'w') as f:
                        json.dump(dataJson, f, indent=4, sort_keys=True, separators=(',', ':'))
                else:
                    with open(cloudDir, 'w') as f:
                        json.dump(dataJson, f, indent=4, sort_keys=True, separators=(',', ':'))


if __name__ == '__main__':
    clouds = cloud()
    clouds.user_register('artur', 'Artur', 'Gomes', 'teste', 'FRMT-09876')
    a = clouds.read()
    print a
