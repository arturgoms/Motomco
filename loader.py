import configparser
import serial
import urllib2
import requests
from threading import Timer
import time
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from gevent.pywsgi import WSGIServer
import zipfile
import os
from urllib2 import urlopen, URLError, HTTPError

config = configparser.ConfigParser()
confDir = 'conf.ini'
cssDir = 'css.ini'
lcd_type = '5'
windows = 'COM4'
linux = '/dev/ttyUSB0'
porta = linux
app = Flask(__name__)
@app.route("/")
def index():
        return render_template("index.html")


@app.route('/internet')
def internet():
    ontest = os.popen("ping -c 1 google.com").read()
    if ontest == '':
        writeConf('DEFAULT', 'INTERNET', 'FALSE')
    else:
        writeConf('DEFAULT', 'INTERNET', 'TRUE')

    config = configparser.ConfigParser()
    config.read(confDir)
    internet = config.get('DEFAULT', 'INTERNET')

    if internet == 'TRUE':
        return str(1)
    else:
        return str(0)

@app.route('/connection') #Pagina para escolha da rede wireless no primeiro uso
def connection():
    a = request.args.get('a', 'OFF', type=str)
    b = request.args.get('b', None, type=str)

    if a == 'OFF':
        cmd = 'nmcli radio wifi off'
        os.system(cmd)
        wifi = 'OFF'
    elif a == "ON":
        cmd = 'nmcli radio wifi o'
        os.system(cmd)
        wifi = 'ON'
    nome = []
    senha = []

    if b == None:

        winame = "wlan0"
        stream = os.popen("iwlist " + winame + " scan")
        networksfound = 0
        for line in stream:

            if "Encryption key" in line:
                senha.append(line.split('Encryption key:', 1)[1])
            if "ESSID" in line:
                networksfound += 1
                nome.append(line.split('ESSID:"', 1)[1].split('"', 1)[0])
        lennome = len(nome)
    else:
        winame = "wlan0"
        stream = os.popen("iwlist " + winame + " scan")
        networksfound = 0
        for line in stream:

            if "Encryption key" in line:
                senha.append(line.split('Encryption key:', 1)[1])
            if "ESSID" in line:
                networksfound += 1
                nome.append(line.split('ESSID:"', 1)[1].split('"', 1)[0])
        c = nome.index(b)
        d = senha[c]
        if d == "on\n":
            return redirect(url_for('password', rede=b))
        else:
            os.popen("iwconfig " + winame + " essid " + c)
            return redirect(url_for('atualizar'))

    css = configparser.ConfigParser()
    css.read(cssDir)


    return render_template('connection.html', wifi=wifi, nome=nome, lennome=lennome
    ,jumbotrom_h = css.get(str(lcd_type), 'all_jumbotrom_h')
    ,jumbotrom_w = css.get(str(lcd_type), 'all_jumbotrom_w')
    ,jumbotrom_margin_left = css.get(str(lcd_type), 'all_jumbotrom_margin_left')
    ,jumbotrom_margin_top = css.get(str(lcd_type), 'all_jumbotrom_margin_top')
    ,jumbotrom_padding = css.get(str(lcd_type), 'all_jumbotrom_padding')
    ,html_h = css.get(str(lcd_type), 'all_html_h')
    ,html_w = css.get(str(lcd_type), 'all_html_w')
    ,connection_title_size = css.get(str(lcd_type), 'connection_title_size')
    ,connection_menu_width = css.get(str(lcd_type), 'connection_menu_width')
    ,connection_menu_height = css.get(str(lcd_type), 'connection_menu_height')
    ,connection_menu_margin_top = css.get(str(lcd_type), 'connection_menu_margin_top')
    ,connection_menu2_width = css.get(str(lcd_type), 'connection_menu2_width')
    ,connection_menu2_height = css.get(str(lcd_type), 'connection_menu2_height')
    ,connection_menu2_margin_top = css.get(str(lcd_type), 'connection_menu2_margin_top')
    ,connetion_list_group_item_width = css.get(str(lcd_type), 'connetion_list_group_item_width')
    ,connetion_list_group_item_height = css.get(str(lcd_type), 'connetion_list_group_item_height')
    ,connetion_list_group_item_padding = css.get(str(lcd_type), 'connetion_list_group_item_padding')
    ,connection_container_margin_left = css.get(str(lcd_type), 'connection_container_margin_left')
    ,connection_container_margin_top = css.get(str(lcd_type), 'connection_container_margin_top')
    ,connection_container_wifi_margin_left=css.get(str(lcd_type), 'connection_container_wifi_margin_left')
    ,connection_showscroll_height=css.get(str(lcd_type), 'connection_showscroll_height')
    ,connection_btn_arrow_width=css.get(str(lcd_type), 'connection_btn_arrow_width')
    ,connection_btn_arrow_height=css.get(str(lcd_type), 'connection_btn_arrow_height')
    ,connection_btn_arrow_margin_top=css.get(str(lcd_type), 'connection_btn_arrow_margin_top') )



@app.route("/password", methods=['GET', 'POST']) #Pagina para inserir a senha depois de selecionada a rede wireless
def password():
    winame = "wlan0"
    b = request.args.get('rede', None, type=str)
    def commandExists(command):
        def canExecute(file):
            return os.path.isfile(file) and os.access(file, os.X_OK)

        for path in os.environ["PATH"].split(os.pathsep):
            file = os.path.join(path, command)
            if canExecute(file):
                return True
        return False
    if request.method == 'POST':
        senha = request.form['senha']
        connectstatus = os.popen("iwconfig " + 'wlan0' + " essid " + b + " key s:" + senha)
        print "Connecting..."
        if not commandExists("dhclient"):
            print "Looks like there isn't a dhclient program on this computer. Trying dhcpd (Used with Arch)"
            con2 = os.popen("dhcpcd " + winame).read()
            print con2
            if not commandExists("dhcpcd"):
                print "Well, I'm out of options. Try installing dhcpd or dhclient."
                quit()
        else:
            os.popen("dhclient " + winame)
        ontest = os.popen("ping -c 1 google.com").read()
        if ontest == '':
            writeConf('DEFAULT', 'INTERNET', 'FALSE')
            quit()

        print "Connected successfully!"
        writeConf('DEFAULT', 'INTERNET', 'TRUE')
        return redirect(url_for('atualizar'))
    return render_template("password.html", rede=b)

@app.route('/atualizar')
def atualizar():
    try:
        port = serial.Serial(porta, baudrate=115200, timeout=1)
        while True:
            port.write("07SHAF1")
            resposta = port.read(200)
            if resposta == '':
                print 'TIMEOUT'
            else:
                index = resposta.find('VERSAO_FW')
                a = resposta.split('split')
                b = a[2].split('VERSAO_FW')
                versaoMB = b[1]
                versaoCP = b[3]
                break
    except Exception as e:
        print("Erro' %s" % e)

    versaoMBSplit = versaoMB.split('.')
    print versaoMBSplit
    config = configparser.ConfigParser()
    config.read(confDir)
    ft = config.get('DEFAULT', 'FIRST-TIME')
    if ft == 'YES':
        a = urllib2.urlopen("http://motomco.hospedagemdesites.ws/arquivos/admin/uploads/CHIP/lista.txt").read()
        lista = a.split('\n')
        while True:
            try:
                lista.remove('')
            except ValueError:
                break
        AT = []
        FB = []
        FR = []
        ES = []
        EE = []
        SI = []
        CP = []
        SWcompat = []
        e = []
        h = []
        for i in lista:
            if i[0:2] == 'AT':
                AT.append(i)
            elif i[0:2] == 'FB':
                FB.append(i)
            elif i[0:2] == 'FR':
                FR.append(i)
            elif i[0:2] == 'ES':
                ES.append(i)
            elif i[0:2] == 'EE':
                EE.append(i)
            elif i[0:2] == 'SI':
                SI.append(i)
            elif i[0:2] == 'CP':
                CP.append(i)
            else:
                print 'Equipamento desocnhecido'

        if versaoMBSplit[0] == 'AT':
            for i in AT:
                d = i.split('.')
                if versaoMBSplit[2] == d[2]:
                    SWcompat.append(i)
            for i in SWcompat:
                d = i.split('.')
                e.append(int(d[3]))
                e.sort(reverse=True)
            new = [s for s in SWcompat if versaoMBSplit[0]+'.MT.'+versaoMBSplit[2]+'.0'+str(e[0]) in s]
            for i in new:
                n = i.split('.')
                h.append(int(n[4]))
                h.sort(reverse=True)
        elif versaoMBSplit[0] == 'FB':
            for i in FB:
                d = i.split('.')
                if versaoMBSplit[2] == d[2]:
                    SWcompat.append(i)
            for i in SWcompat:
                d = i.split('.')
                e.append(int(d[3]))
                e.sort(reverse=True)
            new = [s for s in SWcompat if versaoMBSplit[0]+'.MT.'+versaoMBSplit[2]+'.0'+str(e[0]) in s]
            for i in new:
                n = i.split('.')
                h.append(int(n[4]))
                h.sort(reverse=True)
        elif versaoMBSplit[0] == 'FR':
            for i in FR:
                d = i.split('.')
                if versaoMBSplit[2] == d[2]:
                    SWcompat.append(i)
            for i in SWcompat:
                d = i.split('.')
                e.append(int(d[3]))
                e.sort(reverse=True)
            new = [s for s in SWcompat if versaoMBSplit[0]+'.MT.'+versaoMBSplit[2]+'.0'+str(e[0]) in s]
            for i in new:
                n = i.split('.')
                h.append(int(n[4]))
                h.sort(reverse=True)

        elif versaoMBSplit[0] == 'ES':
            for i in ES:
                d = i.split('.')
                if versaoMBSplit[2] == d[2]:
                    SWcompat.append(i)
            for i in SWcompat:
                d = i.split('.')
                e.append(int(d[3]))
                e.sort(reverse=True)
            new = [s for s in SWcompat if versaoMBSplit[0]+'.MT.'+versaoMBSplit[2]+'.0'+str(e[0]) in s]
            for i in new:
                n = i.split('.')
                h.append(int(n[4]))
                h.sort(reverse=True)
        elif versaoMBSplit[0] == 'EE':
            for i in EE:
                d = i.split('.')
                if versaoMBSplit[2] == d[2]:
                    SWcompat.append(i)
            for i in SWcompat:
                d = i.split('.')
                e.append(int(d[3]))
                e.sort(reverse=True)
            new = [s for s in SWcompat if versaoMBSplit[0]+'.MT.'+versaoMBSplit[2]+'.0'+str(e[0]) in s]
            for i in new:
                n = i.split('.')
                h.append(int(n[4]))
                h.sort(reverse=True)
        elif versaoMBSplit[0] == 'SI':
            for i in SI:
                d = i.split('.')
                if versaoMBSplit[2] == d[2]:
                    SWcompat.append(i)
            for i in SWcompat:
                d = i.split('.')
                e.append(int(d[3]))
                e.sort(reverse=True)
            new = [s for s in SWcompat if versaoMBSplit[0]+'.MT.'+versaoMBSplit[2]+'.0'+str(e[0]) in s]
            for i in new:
                n = i.split('.')
                h.append(int(n[4]))
                h.sort(reverse=True)
        elif versaoMBSplit[0] == 'CP':
            for i in CP:
                d = i.split('.')
                if versaoMBSplit[2] == d[2]:
                    SWcompat.append(i)
            for i in SWcompat:
                d = i.split('.')
                e.append(int(d[3]))
                e.sort(reverse=True)
            new = [s for s in SWcompat if versaoMBSplit[0]+'.MT.'+versaoMBSplit[2]+'.0'+str(e[0]) in s]
            for i in new:
                n = i.split('.')
                h.append(int(n[4]))
                h.sort(reverse=True)
        else:
            print 'Equipamento desconhecido'

        url = 'http://motomco.hospedagemdesites.ws/arquivos/admin/uploads/CHIP/'+versaoMBSplit[0]+'.MT.'+versaoMBSplit[2]+'.0'+str(e[0])+'.0'+str(h[0])+'.zip'
        f = urlopen(url)
        print "downloading " + url
        with open(os.path.basename(url), "wb") as local_file:
            local_file.write(f.read())
        zip_ref = zipfile.ZipFile(versaoMBSplit[0]+'.MT.'+versaoMBSplit[2]+'.0'+str(e[0])+'.0'+str(h[0])+'.zip', 'r')
        zip_ref.extractall('main/')
        zip_ref.close()
        os.remove(versaoMBSplit[0]+'.MT.'+versaoMBSplit[2]+'.0'+str(e[0])+'.0'+str(h[0])+'.zip')
        writeConf('DEFAULT', 'FIRST-TIME', 'NO')
        writeConf('DEFAULT', 'SW-VERSION', versaoMBSplit[0]+'.MT.'+versaoMBSplit[2]+'.0'+str(e[0])+'.0'+str(h[0]))
        return str(1)
    else:
        config = configparser.ConfigParser()
        config.read(confDir)
        swversion = config.get('DEFAULT', 'SW-VERSION')

        a = urllib2.urlopen("http://motomco.hospedagemdesites.ws/arquivos/admin/uploads/CHIP/lista.txt").read()
        lista = a.split('\n')
        while True:
            try:
                lista.remove('')
            except ValueError:
                break
        AT = []
        FB = []
        FR = []
        ES = []
        EE = []
        SI = []
        CP = []
        SWcompat = []
        e = []
        h = []
        for i in lista:
            if i[0:2] == 'AT':
                AT.append(i)
            elif i[0:2] == 'FB':
                FB.append(i)
            elif i[0:2] == 'FR':
                FR.append(i)
            elif i[0:2] == 'ES':
                ES.append(i)
            elif i[0:2] == 'EE':
                EE.append(i)
            elif i[0:2] == 'SI':
                SI.append(i)
            elif i[0:2] == 'CP':
                CP.append(i)
            else:
                print 'Equipamento desocnhecido'

        if versaoMBSplit[0] == 'AT':
            for i in AT:
                d = i.split('.')
                if versaoMBSplit[2] == d[2]:
                    SWcompat.append(i)
            for i in SWcompat:
                d = i.split('.')
                e.append(int(d[3]))
                e.sort(reverse=True)
            new = [s for s in SWcompat if versaoMBSplit[0] + '.MT.' + versaoMBSplit[2] + '.0' + str(e[0]) in s]
            for i in new:
                n = i.split('.')
                h.append(int(n[4]))
                h.sort(reverse=True)
        elif versaoMBSplit[0] == 'FB':
            for i in FB:
                d = i.split('.')
                if versaoMBSplit[2] == d[2]:
                    SWcompat.append(i)
            for i in SWcompat:
                d = i.split('.')
                e.append(int(d[3]))
                e.sort(reverse=True)
            new = [s for s in SWcompat if versaoMBSplit[0] + '.MT.' + versaoMBSplit[2] + '.0' + str(e[0]) in s]
            for i in new:
                n = i.split('.')
                h.append(int(n[4]))
                h.sort(reverse=True)
        elif versaoMBSplit[0] == 'FR':
            for i in FR:
                d = i.split('.')
                if versaoMBSplit[2] == d[2]:
                    SWcompat.append(i)
            for i in SWcompat:
                d = i.split('.')
                e.append(int(d[3]))
                e.sort(reverse=True)
            new = [s for s in SWcompat if versaoMBSplit[0] + '.MT.' + versaoMBSplit[2] + '.0' + str(e[0]) in s]
            for i in new:
                n = i.split('.')
                h.append(int(n[4]))
                h.sort(reverse=True)

        elif versaoMBSplit[0] == 'ES':
            for i in ES:
                d = i.split('.')
                if versaoMBSplit[2] == d[2]:
                    SWcompat.append(i)
            for i in SWcompat:
                d = i.split('.')
                e.append(int(d[3]))
                e.sort(reverse=True)
            new = [s for s in SWcompat if versaoMBSplit[0] + '.MT.' + versaoMBSplit[2] + '.0' + str(e[0]) in s]
            for i in new:
                n = i.split('.')
                h.append(int(n[4]))
                h.sort(reverse=True)
        elif versaoMBSplit[0] == 'EE':
            for i in EE:
                d = i.split('.')
                if versaoMBSplit[2] == d[2]:
                    SWcompat.append(i)
            for i in SWcompat:
                d = i.split('.')
                e.append(int(d[3]))
                e.sort(reverse=True)
            new = [s for s in SWcompat if versaoMBSplit[0] + '.MT.' + versaoMBSplit[2] + '.0' + str(e[0]) in s]
            for i in new:
                n = i.split('.')
                h.append(int(n[4]))
                h.sort(reverse=True)
        elif versaoMBSplit[0] == 'SI':
            for i in SI:
                d = i.split('.')
                if versaoMBSplit[2] == d[2]:
                    SWcompat.append(i)
            for i in SWcompat:
                d = i.split('.')
                e.append(int(d[3]))
                e.sort(reverse=True)
            new = [s for s in SWcompat if versaoMBSplit[0] + '.MT.' + versaoMBSplit[2] + '.0' + str(e[0]) in s]
            for i in new:
                n = i.split('.')
                h.append(int(n[4]))
                h.sort(reverse=True)
        elif versaoMBSplit[0] == 'CP':
            for i in CP:
                d = i.split('.')
                if versaoMBSplit[2] == d[2]:
                    SWcompat.append(i)
            for i in SWcompat:
                d = i.split('.')
                e.append(int(d[3]))
                e.sort(reverse=True)
            new = [s for s in SWcompat if versaoMBSplit[0] + '.MT.' + versaoMBSplit[2] + '.0' + str(e[0]) in s]
            for i in new:
                n = i.split('.')
                h.append(int(n[4]))
                h.sort(reverse=True)
        else:
            print 'Equipamento desconhecido'

        if swversion != versaoMBSplit[0]+'.MT.'+versaoMBSplit[2]+'.0'+str(e[0])+'.0'+str(h[0]):
            url = 'http://motomco.hospedagemdesites.ws/arquivos/admin/uploads/CHIP/' + versaoMBSplit[0] + '.MT.' + \
                  versaoMBSplit[2] + '.0' + str(e[0]) + '.0' + str(h[0]) + '.zip'
            f = urlopen(url)
            print "downloading " + url
            with open(os.path.basename(url), "wb") as local_file:
                local_file.write(f.read())
            zip_ref = zipfile.ZipFile(
                versaoMBSplit[0] + '.MT.' + versaoMBSplit[2] + '.0' + str(e[0]) + '.0' + str(h[0]) + '.zip', 'r')
            zip_ref.extractall('main/')
            zip_ref.close()
            os.remove(versaoMBSplit[0]+'.MT.'+versaoMBSplit[2]+'.0'+str(e[0])+'.0'+str(h[0])+'.zip')
            writeConf('DEFAULT', 'FIRST-TIME', 'NO')
            writeConf('DEFAULT', 'SW-VERSION',
                      versaoMBSplit[0] + '.MT.' + versaoMBSplit[2] + '.0' + str(e[0]) + '.0' + str(h[0]))
            print ' Equipamento foi atualizado'
            return str(1)
        else:
            print 'Equipamento ja esta atualizado '    
            return str(0)

@app.route('/seriouslykill', methods=['GET', 'POST'])
def seriouslykill():
    import subprocess
    print 'Chamando o servidor'
    subprocess.call("sudo python main/home.py &", shell=True)
    time.sleep(2)
    return str(1)

def writeConf(section='DEFAULT', nome='nome', valor='NO'): # funcao para escrever no arquivo conf.ini
    config.read(confDir)
    config[section][nome] = valor
    with open(confDir, 'w') as configfile:
        config.write(configfile)

def verifConf(): # verifica se existe o arquivo conf.ini, se nao tiver ele cria

    try:
        with open(confDir, 'r') as f:
            return 0

    except IOError:
        config['DEFAULT'] = {'INTERNET': 'NO', 'lcd_type': '5', 'FIRST-TIME': 'YES'}

        with open(confDir, 'w') as configfile:
            config.write(configfile)
        return 1

if __name__ == '__main__':
    verifConf()
    app.run(host="0.0.0.0")
