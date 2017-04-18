import json
import os
import urllib2
from arquivos.rwconf import *
import ast
import configparser
import subprocess
from ubidots import ApiClient

token = 'iTpmRSnZyIZsjCkLbHPjNxReiESAmF'

api = ApiClient(token=token)

confDir = 'main/conf.ini'
cloudDir = 'main/arquivos/cloud.json'

class cloudhandler:  # Classe que lida com a NUVEM

    def conf_handler(self): # Funcao que grava o TOKEN no arquivo conf
        try:
            writeConf('UBIDOTS', 'TOKEN', token)
            logger.info("Cloud - TOKEN Successfully saved")
        except Exception as a:
            logger.error("Cloud - Could not write token in file conf.ini - {}".format(a))

    def list_datasources(self): # Funcao que lista os equipamentos
        try:
            all_datasources = api.get_datasources()
            logger.info("Cloud - Equipment Listed Successfully")
            return all_datasources
        except Exception as b:
            logger.error("Cloud - Could not list equipment - {}".format(b))
            return "error"

    def verif_datasource(self): # Funcao que verifica se existe o equipamento na NUVEM, se nao ele cria com base no seu Numero de serie
        config = configparser.ConfigParser()
        config.read(confDir)
        nserie = config.get('DEFAULT', 'NSERIE')
        try:
            all_datasource = cloudhandler.list_datasources(self)
            if all_datasource == 'error':
                logger.error("Cloud - Could not verify the database")
                return "error"
            else:
                if nserie not in str(all_datasource):
                    data = '{"name": "nserie"}'
                    data = data.replace('nserie', nserie)
                    url = 'http://things.ubidots.com/api/v1.6/datasources/?token=' + token
                    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
                    f = urllib2.urlopen(req)
                    for x in f:
                        returnoutput = x
                        json_acceptable_string = returnoutput.replace("'", "\"")
                        output = json.loads(json_acceptable_string)
                        id = output["id"]
                        name = output["nme"]
                        variables_url = output["variables_url"]
                        try:
                            config.add_section("UBIDOTS")
                            config.set('UBIDOTS', 'datasource-id', id)
                            config.set('UBIDOTS', 'name', name)
                            config.set('UBIDOTS', 'variables_url', variables_url)
                        except:
                            config.set('UBIDOTS', 'datasource-id', id)
                            config.set('UBIDOTS', 'name', name)
                            config.set('UBIDOTS', 'variables_url', variables_url)
                        with open(confDir, 'w') as configfile:
                            config.write(configfile)
                        return output
                    f.close()

                else:
                    return "Datasource already exist"
        except Exception as c:
            logger.error("Cloud - Could not verify the database {}".format(c))

    def list_variables(self): # Funcao que lista as variaveis do equipamento na NUVEM
        try:
            config = configparser.ConfigParser()
            config.read(confDir)
            datasource_id = config.get('UBIDOTS', 'datasource-id')
            datasource = api.get_datasource(datasource_id)
            all_variables = datasource.get_variables()
            logger.info("Cloud - Variaveis listadas com sucesso")
            return all_variables
        except Exception as a:
            logger.error("Cloud - Could not list token variables - {]".format(a))

    def create_variables(self): # Funcao que cria as variaveis dentro do equipamentos
        try:
            config = configparser.ConfigParser()
            config.read(confDir)
            datasource_id = config.get('UBIDOTS', 'datasource-id')
            tipoPH = config.get('DEFAULT', 'PH')
            cloud = cloudhandler()
            all_variables = cloud.list_variables()
            f = open(cloudDir, 'r')
            dataJson = json.load(f)
            lenCloud = len(dataJson)
            count = 0
            tipo = 0
            a = []
            variables = ["Umidade", "Contador", "Temperatura", "Dial", "Dial_Corrigido", "Frequencia_Cheio", "Frequencia_Vazio", "Grupo", "Nome", "Peso", "PH", "Data"]
            for i in range(lenCloud):
                data = dataJson[i]
                a.append(data['result'])
            if all_variables == []:
                for i in variables:
                    if i == "Umidade":
                        data = '{"name": "nserie", "unit":"%" }'
                    elif i == "Temperatura":
                        data = '{"name": "nserie", "unit":"\u00baC" }'
                    elif i == "Contador":
                        data = '{"name": "nserie", "unit":"" }'
                    elif i == "Dial":
                        data = '{"name": "nserie", "unit":"" }'
                    elif i == "Dial_Corrigido":
                        data = '{"name": "nserie", "unit":"" }'
                    elif i == "Frequencia_Cheio":
                        data = '{"name": "nserie", "unit":"" }'
                    elif i == "Frequencia_Vazio":
                        data = '{"name": "nserie", "unit":"" }'
                    elif i == "Grupo":
                        data = '{"name": "nserie", "unit":"" }'
                    elif i == "Peso":
                        data = '{"name": "nserie", "unit":"g" }'
                    elif i == "PH":
                        data = '{"name": "nserie", "unit":"kg/hl" }'
                        data = data.replace('kg/hl', tipoPH)
                    data = data.replace('nserie', i)
                    url = 'http://things.ubidots.com/api/v1.6/datasources/' + datasource_id + '/variables/?token=' + token
                    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
                    f = urllib2.urlopen(req)
                    for x in f:
                        returnoutput = x
                        json_acceptable_string = returnoutput.replace("'", "\"")
                        output = json.loads(json_acceptable_string)
                        id = output["id"]
                        config.set('UBIDOTS', i, id)
                        with open(confDir, 'w') as configfile:
                            config.write(configfile)
                    f.close()
            logger.info("Cloud - Variables created successfully")
            return "OK"
        except Exception as a:
            logger.error("Cloud - Could not create the variables- {}".format(a))

    def update_values(self): # Funcao que atualiza os valores a cada resultado
        try:
            config = configparser.ConfigParser()
            config.read(confDir)
            datasource_id = config.get('UBIDOTS', 'datasource-id')
            nserie = config.get('DEFAULT', 'NSERIE')
            cloud = cloudhandler()
            f = open(cloudDir, 'r')
            dataJson = json.load(f)
            lenCloud = len(dataJson)
            count = 0
            tipo = 0
            a = []
            variables = ["Umidade", "Temperatura", "Dial", "Dial Corrigido", "Frequencia Cheio", "Frequencia Vazio", "Grupo", "Nome", "peso", "PH", "Data"]
            for i in range(lenCloud):
                data = dataJson[i]
                a.append(data['result'])
            #print a
                try:
                    for i in xrange(len(a)):
                        b = a[i]
                        for c in xrange(len(b)):
                            try:
                                if b[c]["nome"] == "":
                                    b.pop(c)
                            except:
                                b.pop(c)
                        try:
                            if b[i]["nome"] == "":
                                a.pop(i)
                        except:
                            a.pop(i)
                except:
                   w = 1
            d = a[0]

            for i in range(0, len(d)):
                e = d[i]
                del e['nome']
                del e['time']
                data = json.dumps(e)
                print data
                data2 = '{"temperatura": [23.4, 23.3, 23.2], "dial": [38.685776031434216, 36.91497758213082, 37.382283837270975],"frequencia_vazio": [10954, 10954, 10954], "umidade": [13.134394149985589, 11.481140903538265, 12.74700993187126], "peso": [237.1, 248.2, 237.9], "dial_corrigido": [45.222493894565254, 37.76788161438762, 43.42338783799405], "contador": [90, 89, 88], "frequencia_cheio": [8144.0, 8178.0, 8169.0], "grupo": [6, 6, 6], "ph": [72.43, 75.82, 72.68]}'
                print data2
                url = 'http://things.ubidots.com/api/v1.6/devices/' + nserie + '?token=' + token
                print url
                req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
                f = urllib2.urlopen(req)
                for x in f:
                    output = x
                    print output
                f.close()
            logger.info("Cloud - Variavies updated successfully")
        except Exception as a:
            logger.error("Cloud - Could not update the variables - {}".format(a))
