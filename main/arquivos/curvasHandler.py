import configparser
import logging

logger = logging.getLogger('log')

# Diretorio dos arquivos

curvaDir = 'main/arquivos/curva.txt'
topDir = 'main/arquivos/top.txt'
confDir = 'main/conf.ini'


def file_len(fname): #Conta o numero de linhas no arquivo
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def listGroup(tag): # lista as curvas dentro do grupo passado como parametro, exemplo listgrupo('ARROZ') retorna todas as curvas dentro do grupo arroz em forma de array
    try:
        grupoStr = '<grupo>'
        f = open(curvaDir, 'r')
        curva = []
        grupo = []
        for word in f:
            curvaTag = word.split('/r')
            grupotag = ((word.split(grupoStr))[1].split(grupoStr)[0])
            if grupotag == tag:
                grupo.append(curvaTag)
        logger.info("Charts Handler - Charts of {} Successfully listed".format(tag))
        return grupo
    except Exception as a:
        logger.error("Charts Handler - Could not list group charts {} - {}".format(tag, a))

def listName(): # separa todos os nomes em um array, apenas em pt
    try:
        nameStr = '<nome>'
        f = open(curvaDir, 'r')
        name = []
        nameIdiomas = []
        for word in f:
            nametag= ((word.split(nameStr))[1].split(nameStr)[0])
            nametagsplit = nametag.split(';')
            if nametagsplit[0] not in name:
                name.append(nametagsplit[0])
        logger.info("Charts Handler - Successfully separated charts")
        return name
    except Exception as a:
        logger.error("Charts Handler - Could not bury the charts in the array - {}".format(a))

def listNameTop(): # lista os nome do top5
    try:
        nameStr = '<nome>'
        f = open(topDir, 'r')
        name = []
        nameIdiomas = []
        for word in f:
            nametag= ((word.split(nameStr))[1].split(nameStr)[0])
            nametagsplit = nametag.split(';')
            if nametagsplit[0] not in name:
                name.append(nametagsplit[0])
        logger.info("Charts Handler - Top charts successfully listed")
        return name
    except Exception as a:
        logger.error("Charts Handler - Could not list the top charts - {}".format(a))
def getBasicInfo(grupoInd, nomeInd): # retorna o nome, grupo, umidade e temperatura da curva, precisa do id do grupo e do nome
    try:
        grupoIndex = ['ARROZ', 'FEIJAO', 'MILHO', 'SOJA', 'OUTROS', 'TRIGO', 'GIRASSOL']
        grupo = listGroup(grupoIndex[grupoInd])
        name = listName()
        NameStr = name[nomeInd]
        curva = []
        name = []
        nameIdiomas = []
        f = grupo[nomeInd-1]
        curvasLen = grupo.__len__()
        for i in range(0, curvasLen):
            nameStr = '<nome>'
            tempStr = '<temp>'
            umidadeStr = '<umidade>'
            grupoStr = '<grupo>'


            name = listName()
            indexCurva = name.index(NameStr)
            curvaCompleta = grupo[indexCurva-1]

            curvaNome = curvaCompleta[0]

            nameFull = ((curvaNome.split(nameStr))[1].split(nameStr)[0])
            nameSplit = nameFull.split(';')
            name = nameSplit[0] # pegar apenas o nome em portugues
            firstname, secondname = name.split(',')
            realname = firstname + ' ' + secondname

            tempFull = ((curvaNome.split(tempStr))[1].split(tempStr)[0])
            tempSplit = tempFull.split(';')

            grupoFull = ((curvaNome.split(grupoStr))[1].split(grupoStr)[0])
            grupoSplit = grupoFull.split(';')
            grupo = grupoSplit[0]

            umidadeFull = ((curvaNome.split(umidadeStr))[1].split(umidadeStr)[0])
            umidadeSplit = umidadeFull.split(';')

            curva = [grupo, realname, tempSplit, umidadeSplit , curvasLen]
            logger.info("Charts Handler - Info OK")
            return curva
    except Exception as a:
        logger.error("Charts Handler - Could not return information from chart - {}".format(a))

def getBasicInfoTop(nomeInd): # retorna o nome, grupo, temperatura e umidade da curva no top5, precisa so do id da curva
    try:
        lastCurva = []
        config = configparser.ConfigParser()
        config.read(confDir)
        lang = config.get('DEFAULT', 'LANG')

        f = open(topDir, 'r')
        for word in f:
            curva = word.split('/r')
            lastCurva.append(curva)
        curvasLen = lastCurva.__len__()
        NameStr = lastCurva[nomeInd]
        for i in range(0, curvasLen):
            nameStr = '<nome>'
            paisStr = '<pais>'
            pesoStr = '<peso>'
            dialTabStr = '<dialTab>'
            uniTempStr = '<uniTemp>'
            tempStr = '<temp>'
            umidadeStr = '<umidade>'
            dialStr = '<dial>'
            equacaoStr = '<equacao>'
            paramPesoStr = '<paramPeso>'
            grupoStr = '<grupo>'
            imgStr = '<img>'
            grupoPHStr = '<grupoPH>'
            paramVolStr = '<paramVol>'
            pesoVolStr = '<pesoVol>'
            dataStr = '<data>'
            orgaoStr = '<orgao>'
            metEstufaStr = '<metEstufa>'
            subProdutoStr = '<subProduto>'
            PHStr = '<PH>'
            QUEBECStr = '<QUEBEC>'
            VolStr = '<Vol2.0>'

            name = lastCurva[i]
            curvaCompleta = lastCurva.index(NameStr)
            curvatop1 = lastCurva[curvaCompleta]
            curvaNome = curvatop1[0]

            nameFull = ((curvaNome.split(nameStr))[1].split(nameStr)[0])
            nameSplit = nameFull.split(';')
            if lang == 'PT':
                name = nameSplit[0]
                firstname, secondname = name.split(',')
                realname = firstname + ' ' + secondname
                # pegar apenas o nome em portugues
            elif lang == 'EN':
                name = nameSplit[1]
                firstname, secondname = name.split(',')
                realname = firstname + ' ' + secondname



            paisFull = ((curvaNome.split(paisStr))[1].split(paisStr)[0])
            paisSplit = paisFull.split(';')

            pesoFull = ((curvaNome.split(pesoStr))[1].split(pesoStr)[0])
            pesoSplit = pesoFull.split(';')

            dialTabFull = ((curvaNome.split(dialTabStr))[1].split(dialTabStr)[0])
            dialTabSplit = dialTabFull.split(';')

            uniTempFull = ((curvaNome.split(uniTempStr))[1].split(uniTempStr)[0])
            uniTempSplit = uniTempFull.split(';')

            tempFull = ((curvaNome.split(tempStr))[1].split(tempStr)[0])
            tempSplit = tempFull.split(';')

            umidadeFull = ((curvaNome.split(umidadeStr))[1].split(umidadeStr)[0])
            umidadeSplit = umidadeFull.split(';')

            dialFull = ((curvaNome.split(dialStr))[1].split(dialStr)[0])
            dialSplit = dialFull.split(';')

            equacaoFull = ((curvaNome.split(equacaoStr))[1].split(equacaoStr)[0])
            equacaoSplit = equacaoFull.split(';')

            paramPesoFull = ((curvaNome.split(paramPesoStr))[1].split(paramPesoStr)[0])
            paramPesoSplit = paramPesoFull.split(';')

            grupoFull = ((curvaNome.split(grupoStr))[1].split(grupoStr)[0])
            grupoSplit = grupoFull.split(';')
            grupo = grupoSplit[0]

            imgFull = ((curvaNome.split(imgStr))[1].split(imgStr)[0])
            imgSplit = imgFull.split(';')

            grupoPHFull = ((curvaNome.split(grupoPHStr))[1].split(grupoPHStr)[0])
            grupoPHSplit = grupoPHFull.split(';')

            paramVolFull = ((curvaNome.split(paramVolStr))[1].split(paramVolStr)[0])
            paramVolSplit = paramVolFull.split(';')

            pesoVolFull = ((curvaNome.split(pesoVolStr))[1].split(pesoVolStr)[0])
            pesoVolSplit = pesoVolFull.split(';')

            dataFull = ((curvaNome.split(dataStr))[1].split(dataStr)[0])
            dataSplit = dataFull.split(';')

            orgaoFull = ((curvaNome.split(orgaoStr))[1].split(orgaoStr)[0])
            orgaoSplit = orgaoFull.split(';')

            metEstufaFull = ((curvaNome.split(metEstufaStr))[1].split(metEstufaStr)[0])
            metEstufaSplit = metEstufaFull.split(';')

            subProdutoFull = ((curvaNome.split(subProdutoStr))[1].split(subProdutoStr)[0])
            subProdutoSplit = subProdutoFull.split(';')

            PHFull = ((curvaNome.split(PHStr))[1].split(PHStr)[0])
            PHSplit = PHFull.split(';')

            QUEBECFull = ((curvaNome.split(QUEBECStr))[1].split(QUEBECStr)[0])
            QUEBECSplit = QUEBECFull.split(';')

            VolFull = ((curvaNome.split(VolStr))[1].split(VolStr)[0])
            VolSplit = VolFull.split(';')

            curva = [grupo, realname, tempSplit, umidadeSplit, curvasLen,  dialSplit, paramPesoSplit, pesoSplit, uniTempSplit, equacaoSplit, dialTabSplit]
            logger.info("Charts Handler - Chart information returned successfully")
            return curva

    except Exception as c:
        logger.error("Charts Handler - Could not return information from chart - {}".format(c))


def getCurva(grupoInd, nomeInd): # retorna a curva inteira passando o id do grupo e do nome
    try:
        grupoIndex = ['ARROZ', 'FEIJAO', 'MILHO', 'SOJA', 'OUTROS', 'TRIGO', 'GIRASSOL']
        grupo = listGroup(grupoIndex[grupoInd])
        f = grupo[nomeInd-1]
        logger.info("Charts Handler - Chart returned successfully")
        return f
    except Exception as a:
        logger.error("Charts Handler - Could not return chart - {}".format(a))

def getCurvaTop(nomeInd):# retorna a primeira curva inteira do top 5
    try:
        lastCurva = []
        f = open(topDir, 'r')
        for word in f:
            curva = word.split('/r')
            lastCurva.append(curva)
        f = lastCurva[nomeInd-1]
        logger.info("Charts Handler - Top Chart returned successfully")
        return f
    except Exception as a:
        logger.error("Charts Handler - Could not return the first top chart - {}".format(a))

def getLastCurva(): # retorna as inf basicas da ultima curva
    try:
        lastCurva = []
        f = open(topDir, 'r')
        for word in f:
            curva = word.split('/r')
            lastCurva.append(curva)
        nameStr = '<nome>'
        tempStr = '<temp>'
        umidadeStr = '<umidade>'
        grupoStr = '<grupo>'

        curvaNome = lastCurva[0]

        nameFull = ((curvaNome.split(nameStr))[1].split(nameStr)[0])
        nameSplit = nameFull.split(';')
        name = nameSplit[0]  # pegar apenas o nome em portugues

        tempFull = ((curvaNome.split(tempStr))[1].split(tempStr)[0])
        tempSplit = tempFull.split(';')

        grupoFull = ((curvaNome.split(grupoStr))[1].split(grupoStr)[0])
        grupoSplit = grupoFull.split(';')
        grupo = grupoSplit[0]

        umidadeFull = ((curvaNome.split(umidadeStr))[1].split(umidadeStr)[0])
        umidadeSplit = umidadeFull.split(';')

        curva = [grupo, name, tempSplit, umidadeSplit]
        logger.info("Charts Handler - Last Chart Information Returned Successfully")
        return curva
    except Exception as a:
        logger.error("Charts Handler - Could not return last chart information - {}".format(a))

def getGrupo(): # retorna o id do grupo da ultima curva
    try:
        grupoIndex = ['ARROZ', 'FEIJAO', 'MILHO', 'SOJA', 'OUTROS', 'TRIGO', 'GIRASSOL']
        grupoStr = '<grupo>'
        lastCurva = []
        f = open(topDir, 'r')
        for word in f:
            curva = word.split('/r')
            lastCurva.append(curva)

        curvaFull = lastCurva[0]
        curvagrupo = curvaFull[0]
        grupoFull = ((curvagrupo.split(grupoStr))[1].split(grupoStr)[0])
        grupoSplit = grupoFull.split(';')
        tag = grupoSplit[0]
        grupo = grupoIndex.index(tag)
        logger.info("Charts Handler - Id Returned Successfully")
        return grupo
    except Exception as a:
        logger.error("Charts Handler - Could not return id - {}".format(a))

def getGrupoId(id): # retorna o id do grupo da ultima curva
    try:
        grupoIndex = ['ARROZ', 'FEIJAO', 'MILHO', 'SOJA', 'OUTROS', 'TRIGO', 'GIRASSOL']
        grupoStr = '<grupo>'
        lastCurva = []
        f = open(topDir, 'r')
        for word in f:
            curva = word.split('/r')
            lastCurva.append(curva)

        curvaFull = lastCurva[id]
        curvagrupo = curvaFull[0]
        grupoFull = ((curvagrupo.split(grupoStr))[1].split(grupoStr)[0])
        grupoSplit = grupoFull.split(';')
        tag = grupoSplit[0]
        grupo = grupoIndex.index(tag)
        logger.info("Charts Handler - Group ID returned successfully")
        return grupo
    except Exception as a:
          logger.error("Charts Handler - Could not return Group ID - {}".format(a))

def getNome(): # retorna o id do nome da ultima curva selecionada, ta com problema
    try:
        nameStr = '<nome>'
        grupoInd = getGrupo()
        grupoIndex = ['ARROZ', 'FEIJAO', 'MILHO', 'SOJA', 'OUTROS', 'TRIGO', 'GIRASSOL']
        grupo = listGroup(grupoIndex[grupoInd])
        curvasLen = grupo.__len__()
        lastCurva = []
        f = open(topDir, 'r')
        for word in f:
            curva = word.split('/r')
            lastCurva.append(curva)

        curvaFull = lastCurva[0]
        curvaNome = curvaFull[0]

        idNome = grupo.index(curvaFull)
        logger.info("Charts Handler - Name ID successfully returned")
        return idNome+1

    except Exception as a:
        logger.error("Charts Handler - Could not return Name ID - {}".format(a))

def getNomeTop(nome): # retorna o id da ultima curva do top
    try:
        lastCurva = []
        f = open(topDir, 'r')
        for word in f:
            curva = word.split('/r')
            lastCurva.append(curva)

        curvaFull = nome
        curvaNome = curvaFull[0]

        try:
            idNome = lastCurva.index(curvaFull)
            logger.info("Charts Handler - Last Chart ID returned successfully")
            return idNome
        except Exception as b:
            logger.error("Charts Handler - Last Chart ID Name not returned - {}".format(b))
            return 0
    except Exception as a:
        logger.error("Charts Handler -Could not return ID of last Chart - {}".format(a))

if __name__ == '__main__':
    teste = getNome()
    print teste