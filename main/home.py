import codecs
import sys
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from flask import json
from arquivos.SerialTTY import gps
from arquivos.autoteste import measure, getFreq, getTemp, getPeso, umidade, initAutoTest
from arquivos.cloud import cloudhandler
from arquivos.umidade import *
from arquivos.umidade import calcPH
from functools import wraps
from arquivos.rwconf import *
from gevent.wsgi import WSGIServer
from arquivos.jsonHandler import historic, cloud
from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from arquivos.cloud import *
import logging
import gc
# encoding: utf-8
import os
reload(sys)
sys.setdefaultencoding("utf-8")
lcdSet = configparser.ConfigParser()
a = lcdSet.read(confDir)
lcd_type = lcdSet.get('DEFAULT', 'lcd_type')
app = Flask(__name__)
app.secret_key = '23v23g24sg2ffjftu7y667'
# Css Config
jumbotrom_h = 0
jumbotrom_w = 0
menu_icon_size = 0

__author__ = ["Artur Gomes", "github.com/arturgoms"]

# Diretorio de arquivos

confDir = 'main/conf.ini'
langDir = 'main/lang.ini'
topDir = 'main/arquivos/top.txt'
cloudDir = 'main/arquivos/cloud.json'
cssDir = 'main/arquivos/css.ini'

logger = logging.getLogger('log')

# CRITICAL - 50
# ERROR - 40
# WARNING - 30
# INFO - 20
# DEBUG - 10
logging.basicConfig(filename='python.log', level=10, format='%(asctime)s: %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

@app.route("/") # Pagina inicial: faz o autoteste e redireciona para a tela de medir
def index():
    config = configparser.ConfigParser()
    config.read(confDir)
    firstTime = config.get('DEFAULT', 'FIRST-TIME')

    if firstTime == 'YES':
        return render_template("index2.html")
    else:
        return render_template("index.html")

def login_required(f): # Funcao que verifica se o usuario esta logado, se nao estiver ela redireciona para a pagina de login
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            logger.warning("Login - Try to log in without authentication")
            flash('You need to login first.')
            return redirect(url_for('login_page'))

    return wrap

@app.route('/medir') #Funcao utilizada pela pagina inicial para executar o autoteste
def medir():
    autoteste = initAutoTest()
    config = configparser.ConfigParser()
    config.read(confDir)
    internet = config.get('DEFAULT', 'INTERNET')
    if autoteste == 1:
        if internet == 'TRUE':
            return str(1)
        else:
            return str(1.1)
    else:
        if internet == 'TRUE':
            return str(0)
        else:
            return str(0.1)


@app.route("/language") #Pagina para escolha do idioma no primeiro uso
def language():
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    config.read(langDir)
    language = config.get(lang, 'language')
    portugues = config.get(lang, 'portugues')
    ingles = config.get(lang, 'ingles')
    alemao = config.get(lang, 'alemao')
    italiano = config.get(lang, 'italiano')
    espanhol = config.get(lang, 'espanhol')
    frances = config.get(lang, 'frances')

    a = request.args.get('a', lang, type=str)

    if a == 'PT':
        writeConf('DEFAULT', 'LANG', 'PT')
        logger.info("Config - Portuguese selected ")
    elif a == 'EN':
        writeConf('DEFAULT', 'LANG', 'EN')
        logger.info("Config - English selected")

    css = configparser.ConfigParser()
    css.read(cssDir)


    return render_template('language.html', language=language, portugues=portugues, ingles=ingles, italiano=italiano, frances=frances, alemao=alemao, espanhol=espanhol
                           , jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           , jumbotrom_w=css.get(str(lcd_type), 'all_jumbotrom_w')
                           , jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           , jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           , jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           , html_h=css.get(str(lcd_type), 'all_html_h')
                           , html_w=css.get(str(lcd_type), 'all_html_w')
                           , language_title_size=css.get(str(lcd_type), 'language_title_size')
                           , language_menu2_width=css.get(str(lcd_type), 'language_menu2_width')
                           , language_menu2_height=css.get(str(lcd_type), 'language_menu2_height')
                           , language_menu2_margin_left=css.get(str(lcd_type), 'language_menu2_margin_left')
                           , language_menu2_margin_top=css.get(str(lcd_type), 'language_menu2_margin_top')
                           , language_menu2_padding=css.get(str(lcd_type), 'language_menu2_padding')
                           , language_photo_width=css.get(str(lcd_type), 'language_photo_width')
                           , language_photo_height=css.get(str(lcd_type), 'language_photo_height')
                           , language_photo_font_size=css.get(str(lcd_type), 'language_photo_font_size')
                           , language_container_margin_left=css.get(str(lcd_type), 'language_container_margin_left')
                           , language_container_margin_top=css.get(str(lcd_type), 'language_container_margin_top')
                           , language_container_width=css.get(str(lcd_type), 'language_container_width')
                           , language_container_screen_1_width=css.get(str(lcd_type), 'language_container_screen_1_width')
                           , language_container_screen_1_min_width=css.get(str(lcd_type), 'language_container_screen_1_min_width')
                           , language_container_screen_2_width=css.get(str(lcd_type),'language_container_screen_2_width')
                           , language_container_screen_2_min_width=css.get(str(lcd_type),'language_container_screen_2_min_width')
                           , language_container_screen_3_width=css.get(str(lcd_type), 'language_container_screen_3_width')
                           , language_container_screen_3_min_width=css.get(str(lcd_type), 'language_container_screen_3_min_width')
                           , language_btn_flag_width=css.get(str(lcd_type), 'language_btn_flag_width')
                           , language_btn_flag_height=css.get(str(lcd_type), 'language_btn_flag_height')
                           , language_btn_arrow_width=css.get(str(lcd_type), 'language_btn_arrow_width')
                           , language_btn_arrow_height=css.get(str(lcd_type), 'language_btn_arrow_height'))


@app.route('/connection') #Pagina para escolha da rede wireless no primeiro uso
def connection():
    a = request.args.get('a', 'OFF', type=str)
    b = request.args.get('b', None, type=str)

    if a == 'OFF':
        cmd = 'nmcli radio wifi off'
        os.system(cmd)
        wifi = 'OFF'
        logger.info("Config - WIFI off")
    elif a == "ON":
        cmd = 'nmcli radio wifi o'
        os.system(cmd)
        wifi = 'ON'
        logger.info("Config - WIFI on")
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
            return redirect(url_for('login'))

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
            print "Connection failed. (Bad pass?)"
            logger.error("Connection - Could not connect to internet")
            writeConf('DEFAULT', 'INTERNET', 'FALSE')
            quit()

        logger.info("Connection - Internet connection established")
        print "Connected successfully!"
        writeConf('DEFAULT', 'INTERNET', 'TRUE')
        return redirect(url_for('register_page'))
    return render_template("password.html", rede=b)





@app.route('/login/', methods=["GET", "POST"]) #Pagina de login
def login_page():

    error = ''
    try:
        clouds = cloud()
        clouds.verif()
        f = open(cloudDir, 'r')
        dataJson = json.load(f)
        lenCloud = len(dataJson)
        count = 0
        tipo = 0

        for i in range(lenCloud):
            data = dataJson[i]
            a = data['username']
            b = request.form['username']
            if data['username'] == request.form['username']:
                password = data['password'][0]
                if sha256_crypt.verify(request.form['password'], password):
                    session['logged_in'] = True
                    session['username'] = request.form['username']
                    user = data['fisrtname'][0]
                    session['name'] = user
                    logger.info("Login - User logged in as {}".format(user))
                    return redirect(url_for("getBasicinfoTop", user=user))

        else:
            logger.error("Login - Failed to log in, invalid credentials? ")
            error = "Invalid credentials, try again."

        gc.collect()
        css = configparser.ConfigParser()
        css.read(cssDir)
        return render_template("login.html", error=error
        ,jumbotrom_h = css.get(str(lcd_type), 'all_jumbotrom_h')
        ,jumbotrom_w = css.get(str(lcd_type), 'all_jumbotrom_w')
        ,jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
        ,jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
        ,jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
        ,html_h = css.get(str(lcd_type), 'all_html_h')
        ,html_w = css.get(str(lcd_type), 'all_html_w')
        ,login_title_size=css.get(str(lcd_type), 'login_title_size')
        ,login_btn_arrow_width=css.get(str(lcd_type), 'login_btn_arrow_width')
        ,login_btn_arrow_height=css.get(str(lcd_type), 'login_btn_arrow_height')
        ,login_amostra_margin_left=css.get(str(lcd_type), 'login_amostra_margin_left')
        ,login_amostra_margin_top=css.get(str(lcd_type), 'login_amostra_margin_top'))

    except Exception as e:
        # flash(e)
        css = configparser.ConfigParser()
        css.read(cssDir)
        #logger.error("Login - Failed to log in")
        #error = "Invalid credentials, try again."
        return render_template("login.html", error=error
        ,jumbotrom_h = css.get(str(lcd_type), 'all_jumbotrom_h')
        ,jumbotrom_w = css.get(str(lcd_type), 'all_jumbotrom_w')
        ,jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
        ,jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
        ,jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
        ,html_h = css.get(str(lcd_type), 'all_html_h')
        ,html_w = css.get(str(lcd_type), 'all_html_w')
        ,login_title_size=css.get(str(lcd_type), 'login_title_size')
        ,login_btn_arrow_width=css.get(str(lcd_type), 'login_btn_arrow_width')
        ,login_btn_arrow_height=css.get(str(lcd_type), 'login_btn_arrow_height')
        ,login_amostra_margin_left=css.get(str(lcd_type), 'login_amostra_margin_left')
        ,login_amostra_margin_top=css.get(str(lcd_type), 'login_amostra_margin_top'))


@app.route('/logout') #Pagina de logout
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You logged In')
    logger.info("Login - User logged out")
    return redirect(url_for('getBasicinfoTop'))

@app.route('/register/', methods=["GET", "POST"]) #Pagina de registro do usuario
def register_page():
    config = configparser.ConfigParser()
    config.read(confDir)
    internet = config.get('DEFAULT', 'INTERNET')
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            #username = form.username.data
            username = request.form['username']
            #email = form.email.data
            #firstname = form.firstname.data
            firstname = request.form['firstname']
            lastname = form.lastname.data
            lastname = request.form['lastname']
            #nserie = form.nserie.data
            #password = sha256_crypt.encrypt((str(form.password.data)))
            password = sha256_crypt.encrypt((str(request.form['password'])))
            #confirm = sha256_crypt.encrypt((str(form.confirm.data)))
            confirm = sha256_crypt.encrypt((str(request.form['confirm'])))
            config = configparser.ConfigParser()
            config.read(confDir)
            lang = config.get('DEFAULT', 'LANG')
            nserie = config.get('DEFAULT', 'NSERIE')
            clouds = cloud()
            clouds.verif()
            f = open(cloudDir, 'r')
            dataJson = json.load(f)
            lenCloud = len(dataJson)
            for i in range(lenCloud):
                data = dataJson[i]
                if data['username'] == username:
                    erro = 'User already exists'
                    logger.info("Register - User already exists")
                    return render_template('register.html', form=form, error=erro)



            clouds.user_register(username, firstname, lastname, password, nserie)

            session['logged_in'] = True
            session['username'] = username
            session['name'] = firstname
            logger.info("Register - Registered user")
            return redirect(url_for('getBasicinfoTop', user=firstname))

        css = configparser.ConfigParser()
        css.read(cssDir)
        return render_template("register.html", form=form
        ,jumbotrom_h = css.get(str(lcd_type), 'all_jumbotrom_h')
        ,jumbotrom_w = css.get(str(lcd_type), 'all_jumbotrom_w')
        ,jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
        ,jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
        ,jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
        ,html_h = css.get(str(lcd_type), 'all_html_h')
        ,html_w = css.get(str(lcd_type), 'all_html_w')
       , register_title_size=css.get(str(lcd_type), 'register_title_size')
       , register_title_margin_left=css.get(str(lcd_type), 'register_title_margin_left')
       , register_menu_margin_top=css.get(str(lcd_type), 'register_menu_margin_top')
       , register_btn_arrow_width=css.get(str(lcd_type), 'register_btn_arrow_width')
       , register_btn_arrow_height=css.get(str(lcd_type), 'register_btn_arrow_height')
       , register_amostra_margin_left=css.get(str(lcd_type), 'register_amostra_margin_left')
       , register_amostra_width=css.get(str(lcd_type), 'register_amostra_width')
       , register_amostra_firstname_width=css.get(str(lcd_type), 'register_amostra_firstname_width')
       , register_amostra_firstname_margin_top=css.get(str(lcd_type), 'register_amostra_firstname_margin_top')
       , register_amostra_lastname_width=css.get(str(lcd_type), 'register_amostra_lastname_width')
       , register_amostra_lastname_margin_top=css.get(str(lcd_type), 'register_amostra_lastname_margin_top')
       , register_amostra_lastname_margin_left=css.get(str(lcd_type), 'register_amostra_lastname_margin_left')
       , register_amostra_username_width=css.get(str(lcd_type), 'register_amostra_username_width')
       , register_amostra_username_margin_top=css.get(str(lcd_type), 'register_amostra_username_margin_top')
       , register_amostra_username_margin_left=css.get(str(lcd_type), 'register_amostra_username_margin_left')
       , register_amostra_password_width=css.get(str(lcd_type), 'register_amostra_password_width')
       , register_amostra_password_margin_top=css.get(str(lcd_type), 'register_amostra_password_margin_top')
       , register_amostra_password_margin_left=css.get(str(lcd_type), 'register_amostra_password_margin_left')
       , register_amostra_confirm_width=css.get(str(lcd_type), 'register_amostra_confirm_width')
       , register_amostra_confirm_margin_top=css.get(str(lcd_type), 'register_amostra_confirm_margin_top')
       , register_amostra_confirm_margin_left=css.get(str(lcd_type), 'register_amostra_confirm_margin_left')
       , register_amostra_accept_tos_width=css.get(str(lcd_type), 'register_amostra_accept_tos_width')
       , register_amostra_accept_tos_margin_left=css.get(str(lcd_type), 'register_amostra_accept_tos_margin_left')
       , register_amostra_btn_register_margin_top=css.get(str(lcd_type),'register_amostra_btn_register_margin_top')
       ,register_amostra_btn_register_margin_left=css.get(str(lcd_type), 'register_amostra_btn_register_margin_left')
       ,register_amostra_error_margin_top=css.get(str(lcd_type), 'register_amostra_error_margin_top'))

    except Exception as e:
        logger.info("Register - Error registering {}".format(e))
        return (str(e))


class RegistrationForm(Form): #Formulario para a paginade registro

    username = TextField('Username', [validators.Length(min=4, max=20)])
    firstname = TextField('First Name', [validators.Length(min=0, max=10)])
    lastname = TextField('Last Name', [validators.Length(min=0, max=10)])
    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice',
                              [validators.Required()])






@login_required
@app.route("/historico") #Pagina de Historico
def historico():
    a = request.args.get('a', 365258, type=int)
    curvaFiltradas = listGroup('ARROZ')
    curva = getBasicInfo(0, 0)
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    config.read(langDir)

    tempRange = config.get(lang, 'nome-temperatura')
    umidRange = config.get(lang, 'nome-umidade')
    historic.verif()
    historico = historic.read()
    lenHistorico = len(historico)
    b = len(historico)
    nome = []
    temp = []
    umidade = []
    ph = []
    data = []
    tipo = []
    peso = []
    dial = []
    dialc = []
    freqv = []
    freqc = []
    cont = []
    lat = []
    lng = []
    logger.info("Screen - Historic")
    css = configparser.ConfigParser()
    css.read(cssDir)
    if a == b:
        a= b-1
        if a == 365258:
            for index in range(0, lenHistorico):
                leitura = historico[index]
                leituraSplit = leitura.split(';')
                nome.append(leituraSplit[0])
                umidade.append(format(float(leituraSplit[1]), ".2f"))
                temp.append(leituraSplit[2])
                ph.append(leituraSplit[3])
                data.append(leituraSplit[10])
                tipo.append(leituraSplit[11])

            return render_template('historico.html', nome=nome, temp=temp, umidade=umidade, lencurva=lenHistorico,
                                       ph=ph, data=data, tipo=tipo,  a=a, b=b
                    ,jumbotrom_h = css.get(str(lcd_type), 'all_jumbotrom_h')
                    ,jumbotrom_w = css.get(str(lcd_type), 'all_jumbotrom_w')
                    ,jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                    ,jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                    ,jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                    ,html_h = css.get(str(lcd_type), 'all_html_h')
                    ,html_w = css.get(str(lcd_type), 'all_html_w')
                   , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                   , menu_width=css.get(str(lcd_type), 'config_menu_width')
                   , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top')
                                   )
        else:
            leitura = historico[a]
            lenHistorico = 1
            leituraSplit = leitura.split(';')
            nome.append(leituraSplit[0])
            umidade.append(format(float(leituraSplit[1]), ".2f"))
            temp.append(leituraSplit[2])
            ph.append(leituraSplit[3])
            dial.append(leituraSplit[4])
            dialc.append(leituraSplit[5])
            freqc.append(leituraSplit[6])
            freqv.append(leituraSplit[7])
            peso.append(leituraSplit[8])
            cont.append(leituraSplit[9])
            data.append(leituraSplit[10])
            tipo.append(leituraSplit[11])
            try:
                latA = leituraSplit[12]
                lat.append(str(latA[0]))
                lngA = leituraSplit[13]
                lng.append(int(lngA[0]))
                logger.info("GPS - Working")
            except:
                lat = 0
                lng = 0
                logger.error("GPS - Error finding signal")
            return render_template('historicoLista.html', nome=nome, temp=temp, umidade=umidade, lencurva=lenHistorico,
                                   ph=ph, data=data, tipo=tipo, peso=peso,
                                   dial=dial, dialc=dialc, freqc=freqc, freqv=freqv, id=cont, a=a, b=b, lat=lat, lng =lng,jumbotrom_h = css.get(str(lcd_type), 'all_jumbotrom_h')
                    ,jumbotrom_w = css.get(str(lcd_type), 'all_jumbotrom_w')
                    ,jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                    ,jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                    ,jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                    ,html_h = css.get(str(lcd_type), 'all_html_h')
                    ,html_w = css.get(str(lcd_type), 'all_html_w')
                   , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                   , menu_width=css.get(str(lcd_type), 'config_menu_width')
                   , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top'))
    elif a <0:
        a = 0
        leitura = historico[a]
        lenHistorico = 1
        leituraSplit = leitura.split(';')
        nome.append(leituraSplit[0])
        umidade.append(format(float(leituraSplit[1]), ".2f"))
        temp.append(leituraSplit[2])
        ph.append(leituraSplit[3])
        dial.append(leituraSplit[4])
        dialc.append(leituraSplit[5])
        freqc.append(leituraSplit[6])
        freqv.append(leituraSplit[7])
        peso.append(leituraSplit[8])
        cont.append(leituraSplit[9])
        data.append(leituraSplit[10])
        tipo.append(leituraSplit[11])
        try:
            latA = leituraSplit[12]
            lat.append(str(latA[0]))
            lngA = leituraSplit[13]
            lng.append(int(lngA[0]))
            logger.info("GPS - Working")
        except:
            lat = 0
            lng = 0
            logger.error("GPS - Error finding signal")
        return render_template('historicoLista.html', nome=nome, temp=temp, umidade=umidade, lencurva=lenHistorico,
                               ph=ph, data=data, tipo=tipo, peso=peso,
                               dial=dial, dialc=dialc, freqc=freqc, freqv=freqv, id=cont, a=a, b=b, lat=lat, lng =lng,jumbotrom_h = css.get(str(lcd_type), 'all_jumbotrom_h')
                    ,jumbotrom_w = css.get(str(lcd_type), 'all_jumbotrom_w')
                    ,jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                    ,jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                    ,jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                    ,html_h = css.get(str(lcd_type), 'all_html_h')
                    ,html_w = css.get(str(lcd_type), 'all_html_w')
                   , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                   , menu_width=css.get(str(lcd_type), 'config_menu_width')
                   , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top'))
    else:
        if a == 365258:
            for index in range(0, lenHistorico):
                leitura = historico[index]
                leituraSplit = leitura.split(';')
                nome.append(leituraSplit[0])
                umidade.append(format(float(leituraSplit[1]), ".2f"))
                temp.append(leituraSplit[2])
                ph.append(leituraSplit[3])
                data.append(leituraSplit[10])
                tipo.append(leituraSplit[11])


            return render_template('historico.html', nome=nome, temp=temp, umidade=umidade, lencurva=lenHistorico,
                    ph=ph, data=data, tipo=tipo,  a=a, b=b
                    ,jumbotrom_h = css.get(str(lcd_type), 'all_jumbotrom_h')
                    ,jumbotrom_w = css.get(str(lcd_type), 'all_jumbotrom_w')
                    ,jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                    ,jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                    ,jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                    ,html_h = css.get(str(lcd_type), 'all_html_h')
                    ,html_w = css.get(str(lcd_type), 'all_html_w')
                   , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                   , menu_width=css.get(str(lcd_type), 'config_menu_width')
                   , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top'))
        else:
            leitura = historico[a]
            lenHistorico = 1
            leituraSplit = leitura.split(';')
            nome.append(leituraSplit[0])
            umidade.append(format(float(leituraSplit[1]), ".2f"))
            temp.append(leituraSplit[2])
            ph.append(leituraSplit[3])
            dial.append(leituraSplit[4])
            dialc.append(leituraSplit[5])
            freqc.append(leituraSplit[6])
            freqv.append(leituraSplit[7])
            peso.append(leituraSplit[8])
            cont.append(leituraSplit[9])
            data.append(leituraSplit[10])
            tipo.append(leituraSplit[11])
        try:
            latA = leituraSplit[12]
            lat.append(str(latA[0]))
            lngA = leituraSplit[13]
            lng.append(int(lngA[0]))
            logger.info("GPS - Working")
        except:
            lat = 0
            lng = 0
            logger.error("GPS - Error finding signal")

        return render_template('historicoLista.html', nome=nome, temp=temp, umidade=umidade, lencurva=lenHistorico, ph=ph, data=data, tipo=tipo, peso=peso,
                               dial=dial, dialc=dialc, freqc=freqc, freqv=freqv, id=cont, a=a, b=b, lat=lat, lng =lng,jumbotrom_h = css.get(str(lcd_type), 'all_jumbotrom_h')
                    ,jumbotrom_w = css.get(str(lcd_type), 'all_jumbotrom_w')
                    ,jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                    ,jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                    ,jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                    ,html_h = css.get(str(lcd_type), 'all_html_h')
                    ,html_w = css.get(str(lcd_type), 'all_html_w')
                   , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                   , menu_width=css.get(str(lcd_type), 'config_menu_width')
                   , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top'))


@app.route('/umidade') # Confere o resultado da serial
@login_required
def umidadeWeb():
    config = configparser.ConfigParser()
    config.read(confDir)
    autoteste = config.get('DEFAULT', 'AUTO-TEST')
    if autoteste == 'YES':
        umidade = measure()
        if umidade == 1:
            logger.info("Serial - Empty Grain cell")
            return str(1)
        elif umidade == 2:
            logger.info("Serial - Full Grain cell")
            return str(2)
        elif umidade == 3:
            logger.info("Serial -  Recognized sample")
            return str(3)
        elif umidade == 4:
            logger.error("Serial - CRC")
            return str(4)
        elif umidade == 5:
            logger.error("Serial - Timeout Oscilattor")
            return str(4)
        elif umidade == 6:
            logger.error("Serial - Encryption")
            return str(4)
        elif umidade == 7:
            logger.error("Serial - Unknown error")
            return str(4)
    else:

        return str(5)
@app.route("/resultado") #Pagina que faz o calculo da umidade e mostra o resultado, alem de enviar os dados para a nuvem
@login_required
def resultado():
    css = configparser.ConfigParser()
    css.read(cssDir)
    return render_template("result.html", umidade="12.38", nome="TRIGO ARGENTINA",
                           resultado="Resultado", ph=127.18, temperatura="22.6", unitemp="C"
                           , jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           , jumbotrom_w=css.get(str(lcd_type), 'all_jumbotrom_w')
                           , jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           , jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           , jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           , html_h=css.get(str(lcd_type), 'all_html_h')
                           , html_w=css.get(str(lcd_type), 'all_html_w')
                           , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                           , menu_width=css.get(str(lcd_type), 'config_menu_width')
                           , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top'))

@app.route("/result") #Pagina que faz o calculo da umidade e mostra o resultado, alem de enviar os dados para a nuvem
@login_required
def result():
    global freqv
    logger.info("Screen - Result")
    tempa = 0
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    config.read(langDir)
    resultado = config.get(lang, 'resultado')
    unitemp = 'C'
    freqv = 10926
    a = request.args.get('a', 0, type=int)
    curva = getBasicInfoTop(a)
    nome = curva[1]
    tempFull = curva[2]
    temp = ' Faixa de temperatura: ' + tempFull[0] + ' - ' + tempFull[1]
    umidadeFull = curva[3]
    Faixaumidade = ' Faixa de umidade ' + umidadeFull[0] + ' - ' + umidadeFull[1]
    ph = 0
    umidadeFinal =0
    temperatura = 0
    try:
        countUmidade = 0
        try:
            freqc = getFreq()
            if 8000 <= freqc <= 11000:
                logger.info("Humidity - Frequency Full OK - {}".format(freqc))
                countUmidade += 1
            else:
                logger.error("Humidity - Frequency Out of the way - {}".format(freqc))
        except Exception as e:
            logger.critical("Humidity - Error reading Frequency - {}".format(e))
        try:
            pesoG = getPeso()
            if 100 <= pesoG <= 500:
                logger.info("Humidity - Weigth OK - {}".format(pesoG))
                countUmidade += 1
            else:
                logger.error("Humidity -  Weigth Out of the way - {}".format(pesoG))
        except Exception as f:
            logger.critical("Humidity - Error reading Weigth- {}".format(f))
        try:
            tempa = getTemp()
            if 0 <= tempa <= 30:
                logger.info("Humidity - Temperature OK - {}".format(tempa))
                countUmidade += 1
            else:
                logger.error("Humidity - Temperature  Out of the way  - {}".format(tempa))
        except Exception as g:
            logger.critical("Humidity - Error reading Temperature - {}".format(g))
        if countUmidade == 3:
            ph = calcPH(pesoG)
            config.read(confDir)
            unitemp = config.get('DEFAULT', 'unitemp')
            if unitemp == 'C':
                temperatura = tempa
            elif unitemp == 'F':
                temperatura = tempa * 1.8 + 32
            umidadeVlr = umidade(curva[1], ph, freqv, freqc, pesoG, tempa, curva[0])
            umidadeFinal = format(umidadeVlr, '.2f')

            if config.get('DEFAULT', 'internet') == "TRUE":
                try:
                    cloud = cloudhandler()
                    cloud.update_values()
                    f = open(cloudDir, 'r')
                    dataJson = json.load(f)
                    lenCloud = len(dataJson)
                    for i in range(lenCloud):
                        data = dataJson[i]
                        add = [{"nome": ""}]
                        data['result'] = add

                    with open(cloudDir, 'w') as f:
                        json.dump(dataJson, f, indent=4, sort_keys=True, separators=(',', ':'))
                    logger.info("Humidity - Data sent to the cloud successfully")
                except Exception as a:
                    logger.error("Humidity - Could not send data to the cloud - {}".format(a))
            else:
                logger.error("Humidity - Could not send data to the cloud - No internet")
        else:
            logger.error("Humidity - countUmidade != 3")



    except Exception as e:
            logger.critical("Humidity - {}".format(e))
            print e

    css = configparser.ConfigParser()
    css.read(cssDir)
    return render_template("result.html", umidade=umidadeFinal, nome=nome, temp=temp, Faixaumidade=Faixaumidade,
                           resultado=resultado, ph=str(ph), temperatura=temperatura, unitemp=unitemp
                           , jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           , jumbotrom_w=css.get(str(lcd_type), 'all_jumbotrom_w')
                           , jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           , jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           , jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           , html_h=css.get(str(lcd_type), 'all_html_h')
                           , html_w=css.get(str(lcd_type), 'all_html_w')
                           , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                           , menu_width=css.get(str(lcd_type), 'config_menu_width')
                           , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top')
                           , result_amostra_margin_top=css.get(str(lcd_type), 'result_amostra_margin_top')
                           , result_amostra_margin_left=css.get(str(lcd_type), 'result_amostra_margin_left')
                           , result_menu2_margin_top=css.get(str(lcd_type), 'result_menu2_margin_top')
                           , result_menu2_margin_left=css.get(str(lcd_type), 'result_menu2_margin_left')
                           , result_dev_amostra_margin_top=css.get(str(lcd_type), 'result_dev_amostra_margin_top')
                           , result_div_amostra_margin_left=css.get(str(lcd_type), 'result_div_amostra_margin_left')
                           , result_div_menu2_width=css.get(str(lcd_type), 'result_div_menu2_width')
                           , result_div_title_margin_top=css.get(str(lcd_type), 'result_div_title_margin_top')
                           , result_div_title_margin_left=css.get(str(lcd_type), 'result_div_title_margin_left')
                           , result_div_title_padding=css.get(str(lcd_type), 'result_div_title_padding')
                           , result_div_umidade_margin_top=css.get(str(lcd_type), 'result_div_umidade_margin_top')
                           , result_div_umidade_width=css.get(str(lcd_type), 'result_div_umidade_width')
                           , result_div_umidade_margin_left=css.get(str(lcd_type), 'result_div_umidade_margin_left')
                           , result_div_p1_font_size=css.get(str(lcd_type), 'result_div_p1_font_size')
                           , result_div_p1_margin_top=css.get(str(lcd_type), 'result_div_p1_margin_top')
                           , result_div_p1_width=css.get(str(lcd_type), 'result_div_p1_width')
                           , result_div_p1_margin_left=css.get(str(lcd_type), 'result_div_p1_margin_left')
                           , result_div_temp_margin_top=css.get(str(lcd_type), 'result_div_temp_margin_top')
                           , result_div_temp_margin_left=css.get(str(lcd_type), 'result_div_temp_margin_left')
                           , result_div_temp_width=css.get(str(lcd_type), 'result_div_temp_width')
                           , result_div_p2_font_size=css.get(str(lcd_type), 'result_div_p2_font_size')
                           , result_div_p2_margin_top=css.get(str(lcd_type), 'result_div_p2_margin_top')
                           , result_div_p2_margin_left=css.get(str(lcd_type), 'result_div_p2_margin_left')
                           , result_div_p2_width=css.get(str(lcd_type), 'result_div_p2_width')
                           , result_div_ph_margin_top=css.get(str(lcd_type), 'result_div_ph_margin_top')
                           , result_div_ph_margin_left=css.get(str(lcd_type), 'result_div_ph_margin_left')
                           , result_div_p3_font_size=css.get(str(lcd_type), 'result_div_p3_font_size')
                           , result_div_p3_width=css.get(str(lcd_type), 'result_div_p3_width')
                           , result_div_p3_margin_top=css.get(str(lcd_type), 'result_div_p3_margin_top')
                           , result_div_p3_margin_left=css.get(str(lcd_type), 'result_div_p3_margin_left')
                           , result_div_btn_qr_margin_left=css.get(str(lcd_type), 'result_div_btn_qr_margin_left')
                           , result_div_btn_qr_margin_top=css.get(str(lcd_type), 'result_div_btn_qr_margin_top')
                           , result_div_btn_padlock_margin_left=css.get(str(lcd_type), 'result_div_btn_padlock_margin_left')
                           , result_div_btn_padlock_margin_top=css.get(str(lcd_type), 'result_div_btn_padlock_margin_top')
                           , result_div_btn_printer_margin_left=css.get(str(lcd_type), 'result_div_btn_printer_margin_left')
                           , result_div_btn_printer_margin_top=css.get(str(lcd_type), 'result_div_btn_printer_margin_top'))


@app.route("/flash")  # Pagina que mostra mensagens na tela
@login_required
def flashStr():
    return render_template("flash.html")


@app.route("/config")  # Pagina de configuracao
def config():

    config = configparser.ConfigParser()
    config.read(confDir)
    language = config.get('DEFAULT', 'LANG')
    ph = config.get('DEFAULT', 'PH')
    unit = config.get('DEFAULT', 'unitemp')
    config.read(langDir)
    config = config.get(language, 'config')
    a = request.args.get('a', language, type=str)

    if a == 'PT':
        writeConf('DEFAULT', 'LANG', 'PT')
        logger.info("Settings - Set language to PT")
    elif a == 'EN':
        writeConf('DEFAULT', 'LANG', 'EN')
        logger.info("Settings - Set language to EN")

    b = request.args.get('b', ph, type=int)

    if b == 0:
        writeConf('DEFAULT', 'PH', 'kg/hl')
        logger.info("Settings - Set PH to kg/hl")
    elif b == 1:
        writeConf('DEFAULT', 'PH', 'lb/bu')
        logger.info("Settings - Set PH to lb/bu")
    elif b == 2:
        writeConf('DEFAULT', 'PH', 'lb/A bu')
        logger.info("Settings - Set PH to lb/A bu")
    elif b == 3:
        writeConf('DEFAULT', 'PH', 'lb/W bu')
        logger.info("Settings - Set PH to lb/W bu")

    c = request.args.get('c', unit, type=str)

    if c == 'C':
        writeConf('DEFAULT', 'unitemp', 'C')
        logger.info("Settings - Set temperature of humidity to Celsius")
    elif c == 'F':
        writeConf('DEFAULT', 'unitemp', 'F')
        logger.info("Settings - Set temperature of humidity to Fahrenheit")

    css = configparser.ConfigParser()
    css.read(cssDir)


    return render_template("config.html", config=config
                           , jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           , jumbotrom_w=css.get(str(lcd_type), 'all_jumbotrom_w')
                           , jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           , jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           , jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           , html_h=css.get(str(lcd_type), 'all_html_h')
                           , html_w=css.get(str(lcd_type), 'all_html_w')
                           , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                           , menu_width=css.get(str(lcd_type), 'config_menu_width')
                           , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top')
                           , menu2_width=css.get(str(lcd_type), 'config_menu2_width')
                           , menu2_height=css.get(str(lcd_type), 'config_menu2_height')
                           , menu2_margin_right=css.get(str(lcd_type), 'config_menu2_margin_right')
                           , amostra_margin_left=css.get(str(lcd_type), 'config_amostra_margin_left')
                           , config_size=css.get(str(lcd_type), 'config_title_size')
                           , config_margin_left=css.get(str(lcd_type), 'config_title_margin_left')
                           , config_margin_top=css.get(str(lcd_type), 'config_title_margin_top')
                           , config_btn_dropbtn_width=css.get(str(lcd_type), 'config_btn_dropbtn_width')
                           , config_btn_autoteste_margin_left=css.get(str(lcd_type), 'config_btn_autoteste_margin_left')
                           , config_btn_autoteste_margin_top=css.get(str(lcd_type), 'config_btn_autoteste_margin_top')
                           , config_btn_autoteste_width=css.get(str(lcd_type), 'config_btn_autoteste_width')
                           , config_btn_historico_margin_left=css.get(str(lcd_type), 'config_btn_historico_margin_left')
                           , config_btn_historico_margin_top=css.get(str(lcd_type), 'config_btn_historico_margin_top')
                           , config_btn_historico_width=css.get(str(lcd_type), 'config_btn_historico_width')
                           , config_btn_dropdown_margin_left=css.get(str(lcd_type), 'config_btn_dropdown_margin_left')
                           , config_btn_dropdown_margin_top=css.get(str(lcd_type), 'config_btn_dropdown_margin_top')
                           , config_btn_dropdown_width=css.get(str(lcd_type), 'config_btn_dropdown_width'))


@app.route('/selectcurvatop') # Pagina de medir
@login_required
def getBasicinfoTop():

    writeConf('DEFAULT', 'first-time', 'NO')
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    config.read(langDir)
    Welcome = config.get(lang, 'bem-vindo')
    tempRange = config.get(lang, 'nome-temperatura')
    umidRange = config.get(lang, 'nome-umidade')
    copoVazio = config.get(lang, 'status-copo-vazio')
    insiraAmortra = config.get(lang, 'status-copo-vazio-2')
    copoCheio = config.get(lang, 'status-copo-cheio')
    retireAmostra = config.get(lang, 'status-copo-cheio-2')
    amostraReconhecida = config.get(lang, 'status-amostra-reconhecida')
    erroCopo = config.get(lang, 'erro-copo')
    erroCopo2 = config.get(lang, 'erro-copo-2')
    erroAutotest = config.get(lang, 'erro-autotest')
    erroAutotest2 = config.get(lang, 'erro-autotest-2')

    a = request.args.get('a', 0, type=int)

    username = session['name']
    user = request.args.get('user', username, type=str)

    curva = getBasicInfoTop(a)
    curvaFull = getCurvaTop(a + 1)
    grupo = curva[0]

    tipo = 0
    if grupo == "ARROZ":
        tipo = 0
    elif grupo == "FEIJAO":
        tipo = 1
    elif grupo == "GIRASOL":
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
    nome = curva[1]
    tempFull = curva[2]
    temp = tempRange + ' ' + tempFull[0] + ' - ' + tempFull[1]
    umidadeFull = curva[3]
    umidade = umidRange + ' ' + umidadeFull[0] + ' - ' + umidadeFull[1]
    lenCurva = ' Numero de Curvas: ' + str(curva[4])
    verif = verifTop5()
    lol = curvaFull[0]
    write = writeTop5Top(lol, a)
    logger.info("Screen - Measure")
    css = configparser.ConfigParser()
    css.read(cssDir)
    return render_template('medir.html', user=user, nome=nome, temp=temp, umidade=umidade, bemvindo=Welcome,
                           copoVazio=copoVazio, insiraAmortra=insiraAmortra, copoCheio=copoCheio,
                           retireAmostra=retireAmostra,
                           amostraReconhecida=amostraReconhecida, erroCopo=erroCopo, erroCopo2=erroCopo2,
                           erroAutotest=erroAutotest, erroAutotest2=erroAutotest2, tipo=tipo
                           , jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           , jumbotrom_w=css.get(str(lcd_type), 'all_jumbotrom_w')
                           , jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           , jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           , jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                           , menu_width=css.get(str(lcd_type), 'config_menu_width')
                           , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top')
                           , menu2_width=css.get(str(lcd_type), 'config_menu2_width')
                           , menu2_height=css.get(str(lcd_type), 'config_menu2_height')
                           , menu2_margin_right=css.get(str(lcd_type), 'config_menu2_margin_right')
                           , amostra_margin_left=css.get(str(lcd_type), 'config_amostra_margin_left')
                           , html_h=css.get(str(lcd_type), 'all_html_h')
                           , html_w=css.get(str(lcd_type), 'all_html_w')
                           , medir_title_size=css.get(str(lcd_type), 'medir_title_size')
                           , medir_img_grao_margin_top=css.get(str(lcd_type), 'medir_img_grao_margin_top')
                           , medir_img_grao_margin_left=css.get(str(lcd_type), 'medir_img_grao_margin_left')
                           , medir_amostra_width=css.get(str(lcd_type), 'medir_amostra_width')
                           , medir_amostra_margin_top=css.get(str(lcd_type), 'medir_amostra_margin_top')
                           , medir_amostra_margin_left=css.get(str(lcd_type), 'medir_amostra_margin_left')
                           , medir_nome_size=css.get(str(lcd_type), 'medir_nome_size')
                           , medir_temp_size=css.get(str(lcd_type), 'medir_temp_size')
                           , medir_umid_size=css.get(str(lcd_type), 'medir_umid_size')
                           , medir_info_margin_top=css.get(str(lcd_type), 'medir_info_margin_top')
                           , medir_info_size=css.get(str(lcd_type), 'medir_info_size')
                           )


@app.route('/selectcurva') # Pagina que seleciona a curva
@login_required
def getBasicinfo():
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    config.read(langDir)
    Welcome = config.get(lang, 'bem-vindo')
    tempRange = config.get(lang, 'nome-temperatura')
    umidRange = config.get(lang, 'nome-umidade')
    copoVazio = config.get(lang, 'status-copo-vazio')
    insiraAmortra = config.get(lang, 'status-copo-vazio-2')
    copoCheio = config.get(lang, 'status-copo-cheio')
    retireAmostra = config.get(lang, 'status-copo-cheio-2')
    amostraReconhecida = config.get(lang, 'status-amostra-reconhecida')
    erroCopo = config.get(lang, 'erro-copo')
    erroCopo2 = config.get(lang, 'erro-copo-2')
    erroAutotest = config.get(lang, 'erro-autotest')
    erroAutotest2 = config.get(lang, 'erro-autotest-2')
    deA = getGrupo()
    deB = getNome()
    a = request.args.get('a', deA, type=int)
    b = request.args.get('b', deB, type=int)
    curva = getBasicInfo(a, b)
    curvaFull = getCurva(a, b)
    nome = curva[1]
    tempFull = curva[2]
    temp = ' Faixa de temperatura: ' + tempFull[0] + ' - ' + tempFull[1]
    umidadeFull = curva[3]
    umidade = ' Faixa de umidade ' + umidadeFull[0] + ' - ' + umidadeFull[1]
    lenCurva = ' Numero de Curvas: ' + str(curva[4])
    curvatop = curvaFull[0]
    lastCurva = []
    grupo = curva[0]
    f = open(topDir, 'r')
    aux = 0
    for word in f:
        curva = word.split('/r')
        lastCurva.append(curva)
    try:
        id = getNomeTop(curvaFull)
    except ValueError:
        print 'id nao encontrado'
        # se a curva clicada e diferente do top 1
    for i in range(0,5):
        lastCurvaAux = lastCurva[i]
        gh = curvaFull[0]
        if lastCurvaAux[0] == curvaFull[0]:
            writeTop5Handler(curvaFull[0], i)
            aux = 1
    if aux == 0:
        verifTop5()
        writeTop5(curvaFull[0])
    tipo = 0
    if grupo == "ARROZ":
        tipo = 0
    elif grupo == "FEIJAO":
        tipo = 1
    elif grupo == "GIRASOL":
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
    logger.info("Screen - Chart selected - {}".format(nome))
    css = configparser.ConfigParser()
    css.read(cssDir)
    return render_template('medir.html', nome=nome, temp=temp, umidade=umidade, bemvindo=Welcome,
                           copoVazio=copoVazio, insiraAmortra=insiraAmortra, copoCheio=copoCheio,
                           retireAmostra=retireAmostra, amostraReconhecida=amostraReconhecida, erroCopo=erroCopo,
                           erroCopo2=erroCopo2, erroAutotest=erroAutotest, erroAutotest2=erroAutotest2, tipo=tipo
                           , jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           , jumbotrom_w=css.get(str(lcd_type), 'all_jumbotrom_w')
                           , jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           , jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           , jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                           , menu_width=css.get(str(lcd_type), 'config_menu_width')
                           , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top')
                           , menu2_width=css.get(str(lcd_type), 'config_menu2_width')
                           , menu2_height=css.get(str(lcd_type), 'config_menu2_height')
                           , menu2_margin_right=css.get(str(lcd_type), 'config_menu2_margin_right')
                           , amostra_margin_left=css.get(str(lcd_type), 'config_amostra_margin_left')
                           , html_h=css.get(str(lcd_type), 'all_html_h')
                           , html_w=css.get(str(lcd_type), 'all_html_w')
                           , medir_title_size=css.get(str(lcd_type), 'medir_title_size')
                           , medir_img_grao_margin_top=css.get(str(lcd_type), 'medir_img_grao_margin_top')
                           , medir_img_grao_margin_left=css.get(str(lcd_type), 'medir_img_grao_margin_left')
                           , medir_amostra_width=css.get(str(lcd_type), 'medir_amostra_width')
                           , medir_amostra_margin_top=css.get(str(lcd_type), 'medir_amostra_margin_top')
                           , medir_amostra_margin_left=css.get(str(lcd_type), 'medir_amostra_margin_left')
                           , medir_nome_size=css.get(str(lcd_type), 'medir_nome_size')
                           , medir_temp_size=css.get(str(lcd_type), 'medir_temp_size')
                           , medir_umid_size=css.get(str(lcd_type), 'medir_umid_size')
                           , medir_info_margin_top=css.get(str(lcd_type), 'medir_info_margin_top')
                           , medir_info_size=css.get(str(lcd_type), 'medir_info_size')
                           )

@app.route('/top') # Pagina que mostra as ultima curvas selecionadas
@login_required
def top():
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    config.read(langDir)

    tempRange = config.get(lang, 'nome-temperatura')
    umidRange = config.get(lang, 'nome-umidade')
    curvaStr = config.get(lang, 'curvas')
    outros = config.get(lang, 'outro')
    outros2 = config.get(lang, 'outros-2')

    curvaFiltradas = []
    f = open(topDir, 'r')
    for word in f:
        curva = word.split('/r')
        curvaFiltradas.append(curva)
    lenCurva = curvaFiltradas.__len__()
    nome = []
    temp = []
    umidade = []
    tempFormat = []
    umidadeFormat = []

    for index in range(0, lenCurva):
        curvaCompleta = curvaFiltradas[index]
        curvaNome = curvaCompleta[0]

        nameFull = ((curvaNome.split('<nome>'))[1].split('<nome>')[0])
        nameSplit = nameFull.split(';')
        nameSplitPt = nameSplit[0]
        if lang == 'PT':
            firstname, secondname = nameSplit[0].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)  # pegar apenas o nome em portugues
        elif lang == 'EN':
            firstname, secondname = nameSplit[1].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)  # pegar apenas o nome em ingles

        tempFull = ((curvaNome.split('<temp>'))[1].split('<temp>')[0])
        temp.append(tempFull.split(';'))
        tempFormat.append(temp[index])
        tempStr = tempFormat[index]
        tempLOL = tempRange + ' ' + tempFull[0] + ' - ' + tempStr[1]
        temp[index] = tempLOL

        umidadeFull = ((curvaNome.split('<umidade>'))[1].split('<umidade>')[0])
        umidade.append(umidadeFull.split(';'))
        umidadeFormat.append(umidade[index])
        umidadeStr = umidadeFormat[index]
        umidadeLOL = umidRange + ' ' + umidadeFull[0] + ' - ' + umidadeStr[1]
        umidade[index] = umidadeLOL
        if lenCurva == 5:
            lenCurva1 = 3
        elif lenCurva == 4:
            lenCurva1 = 3
        elif lenCurva == 3:
            lenCurva1 = 3
        elif lenCurva == 2:
            lenCurva1 = 2
        elif lenCurva == 1:
            lenCurva1 = 1
    logger.info("Screen - Top charts")
    css = configparser.ConfigParser()
    css.read(cssDir)
    return render_template('top.html', curva=curvaStr, nome=nome, temp=temp, umidade=umidade, lencurva=lenCurva,
                           lencurva1=lenCurva1, outros=outros, outros2=outros2
                           , jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           , jumbotrom_w=css.get(str(lcd_type), 'all_jumbotrom_w')
                           , jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           , jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           , jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                           , menu_width=css.get(str(lcd_type), 'config_menu_width')
                           , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top')
                           , top_menu_width=css.get(str(lcd_type), 'top_menu_width')
                           , top_menu_margin_top=css.get(str(lcd_type), 'top_menu_margin_top')
                           , top_amostra_margin_top=css.get(str(lcd_type), 'top_amostra_margin_top')
                           , top_amostra_margin_left=css.get(str(lcd_type), 'top_amostra_margin_left')
                           , top_menu2_margin_top=css.get(str(lcd_type), 'top_menu2_margin_top')
                           , top_menu2_margin_left=css.get(str(lcd_type), 'top_menu2_margin_left')
                           , top_menu2_width=css.get(str(lcd_type), 'top_menu2_width')
                           , top_list_group_item_width=css.get(str(lcd_type), 'top_list_group_item_width')
                           , top_list_group_item_height=css.get(str(lcd_type), 'top_list_group_item_height')
                           , top_outros_margin_left=css.get(str(lcd_type), 'top_outros_margin_left')
                           , top_outros_height=css.get(str(lcd_type), 'top_outros_height')
                           , top_outros_width=css.get(str(lcd_type), 'top_outros_width')
                           , top_outros_margin_top=css.get(str(lcd_type), 'top_outros_margin_top')
                           , top_outros_img_margin_top=css.get(str(lcd_type), 'top_outros_img_margin_top')
                           , top_outros_size_1=css.get(str(lcd_type), 'top_outros_size_1')
                           , top_outros_size_2=css.get(str(lcd_type), 'top_outros_size_2')
                           , top_list_group_item_padding=css.get(str(lcd_type), 'top_list_group_item_padding'))



@app.route('/top/grupo') # Pagina que mostra os grupos de curvas
@login_required
def topGrupo():
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    config.read(langDir)

    tempRange = config.get(lang, 'nome-temperatura')
    umidRange = config.get(lang, 'nome-umidade')
    curvaStr = config.get(lang, 'curvas')
    arroz = config.get(lang, 'arroz')
    feijao = config.get(lang, 'feijao')
    milho = config.get(lang, 'milho')
    soja = config.get(lang, 'soja')
    outro = config.get(lang, 'outros')
    trigo = config.get(lang, 'trigo')
    girassol = config.get(lang, 'girassol')
    custom = config.get(lang, 'custom')

    curvaFiltradas = []
    f = open(topDir, 'r')
    for word in f:
        curva = word.split('/r')
        curvaFiltradas.append(curva)
    lenCurva = curvaFiltradas.__len__()
    nome = []
    temp = []

    umidade = []
    tempFormat = []
    umidadeFormat = []
    for index in range(0, lenCurva):
        curvaCompleta = curvaFiltradas[index]
        curvaNome = curvaCompleta[0]

        nameFull = ((curvaNome.split('<nome>'))[1].split('<nome>')[0])
        nameSplit = nameFull.split(';')
        nameSplitPt = nameSplit[0]
        if lang == 'PT':
            firstname, secondname = nameSplit[0].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)  # pegar apenas o nome em portugues
        elif lang == 'EN':
            firstname, secondname = nameSplit[1].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)   # pegar apenas o nome em ingles

        tempFull = ((curvaNome.split('<temp>'))[1].split('<temp>')[0])
        temp.append(tempFull.split(';'))
        tempFormat.append(temp[index])
        tempStr = tempFormat[index]
        tempLOL = tempRange + ' ' + tempFull[0] + ' - ' + tempStr[1]
        temp[index] = tempLOL

        umidadeFull = ((curvaNome.split('<umidade>'))[1].split('<umidade>')[0])
        umidade.append(umidadeFull.split(';'))
        umidadeFormat.append(umidade[index])
        umidadeStr = umidadeFormat[index]
        umidadeLOL = umidRange + ' ' + umidadeFull[0] + ' - ' + umidadeStr[1]
        umidade[index] = umidadeLOL
        if lenCurva == 5:
            lenCurva1 = 3
        elif lenCurva == 4:
            lenCurva1 = 3
        elif lenCurva == 3:
            lenCurva1 = 3
        elif lenCurva == 2:
            lenCurva1 = 2
        elif lenCurva == 1:
            lenCurva1 = 1
    logger.info("Screen - Groups")
    css = configparser.ConfigParser()
    css.read(cssDir)
    return render_template('grupo.html', curva=curvaStr, nome=nome, temp=temp, umidade=umidade, lencurva=lenCurva,
                           lencurva1=lenCurva1,
                           arroz=arroz, feijao=feijao, milho=milho, soja=soja, outro=outro, trigo=trigo,
                           girassol=girassol, custom=custom
                           ,jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           ,jumbotrom_w = css.get(str(lcd_type), 'all_jumbotrom_w')
                           ,jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           ,jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           ,jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           ,html_h = css.get(str(lcd_type), 'all_html_h')
                           ,html_w = css.get(str(lcd_type), 'all_html_w')
                           ,menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                           ,menu_width=css.get(str(lcd_type), 'config_menu_width')
                           ,menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top'))


@app.route('/grupo/arroz') # Pagina que mostra as curvas do grupo arroz
@login_required
def arroz():
    curvaFiltradas = listGroup('ARROZ')
    curva = getBasicInfo(0, 0)
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    config.read(langDir)

    tempRange = config.get(lang, 'nome-temperatura')
    umidRange = config.get(lang, 'nome-umidade')
    curvaStr = config.get(lang, 'curvas')
    arroz = config.get(lang, 'arroz')
    feijao = config.get(lang, 'feijao')
    milho = config.get(lang, 'milho')
    soja = config.get(lang, 'soja')
    outro = config.get(lang, 'outros')
    trigo = config.get(lang, 'trigo')
    girassol = config.get(lang, 'girassol')
    custom = config.get(lang, 'custom')
    lenCurva = curva[4]
    nome = []
    temp = []
    umidade = []
    tempFormat = []
    umidadeFormat = []
    for index in range(0, lenCurva):

        name = listName()
        NameStr = name[index]
        indexCurva = name.index(NameStr)
        curvaCompleta = curvaFiltradas[indexCurva - 1]
        curvaNome = curvaCompleta[0]

        nameFull = ((curvaNome.split('<nome>'))[1].split('<nome>')[0])
        nameSplit = nameFull.split(';')
        nameSplitPt = nameSplit[0]
        if lang == 'PT':
            firstname, secondname = nameSplit[0].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)  # pegar apenas o nome em portugues
        elif lang == 'EN':
            firstname, secondname = nameSplit[1].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)   # pegar apenas o nome em ingles
        tempFull = ((curvaNome.split('<temp>'))[1].split('<temp>')[0])
        temp.append(tempFull.split(';'))
        tempFormat.append(temp[index])
        tempStr = tempFormat[index]
        tempLOL = tempRange + ' ' + tempFull[0] + ' - ' + tempStr[1]
        temp[index] = tempLOL

        umidadeFull = ((curvaNome.split('<umidade>'))[1].split('<umidade>')[0])
        umidade.append(umidadeFull.split(';'))
        umidadeFormat.append(umidade[index])
        umidadeStr = umidadeFormat[index]
        umidadeLOL = umidRange + ' ' + umidadeFull[0] + ' - ' + umidadeStr[1]
        umidade[index] = umidadeLOL

    css = configparser.ConfigParser()
    css.read(cssDir)
    logger.info("Screen - Groups Rice")
    return render_template('arroz.html', nome=nome, temp=temp, umidade=umidade, lencurva=lenCurva, arroz=arroz,
                           feijao=feijao, milho=milho, soja=soja, outro=outro, trigo=trigo, girassol=girassol,
                           custom=custom
                           ,jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           ,jumbotrom_w = css.get(str(lcd_type), 'all_jumbotrom_w')
                           ,jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           ,jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           ,jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           ,html_h = css.get(str(lcd_type), 'all_html_h')
                           ,html_w = css.get(str(lcd_type), 'all_html_w')
                           ,menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                           ,menu_width=css.get(str(lcd_type), 'config_menu_width')
                           ,menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top'))


@app.route('/grupo/feijao')  # Pagina que mostra as curvas do grupo Feijao
@login_required
def feijao():
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    config.read(langDir)
    tempRange = config.get(lang, 'nome-temperatura')
    umidRange = config.get(lang, 'nome-umidade')
    curvaStr = config.get(lang, 'curvas')
    arroz = config.get(lang, 'arroz')
    feijao = config.get(lang, 'feijao')
    milho = config.get(lang, 'milho')
    soja = config.get(lang, 'soja')
    outro = config.get(lang, 'outros')
    trigo = config.get(lang, 'trigo')
    girassol = config.get(lang, 'girassol')
    custom = config.get(lang, 'custom')

    curvaFiltradas = listGroup('FEIJAO')
    curva = getBasicInfo(1, 0)
    lenCurva = curva[4]
    nome = []
    temp = []
    umidade = []
    tempFormat = []
    umidadeFormat = []
    for index in range(0, lenCurva):

        name = listName()
        NameStr = name[index]
        indexCurva = name.index(NameStr)
        curvaCompleta = curvaFiltradas[indexCurva - 1]
        curvaNome = curvaCompleta[0]

        nameFull = ((curvaNome.split('<nome>'))[1].split('<nome>')[0])
        nameSplit = nameFull.split(';')
        nameSplitPt = nameSplit[0]
        if lang == 'PT':
            firstname, secondname = nameSplit[0].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)  # pegar apenas o nome em portugues
        elif lang == 'EN':
            firstname, secondname = nameSplit[1].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)   # pegar apenas o nome em ingles

        tempFull = ((curvaNome.split('<temp>'))[1].split('<temp>')[0])
        temp.append(tempFull.split(';'))
        tempFormat.append(temp[index])
        tempStr = tempFormat[index]
        tempLOL = tempRange + ' ' + tempFull[0] + ' - ' + tempStr[1]
        temp[index] = tempLOL

        umidadeFull = ((curvaNome.split('<umidade>'))[1].split('<umidade>')[0])
        umidade.append(umidadeFull.split(';'))
        umidadeFormat.append(umidade[index])
        umidadeStr = umidadeFormat[index]
        umidadeLOL = umidRange + ' ' + umidadeFull[0] + ' - ' + umidadeStr[1]
        umidade[index] = umidadeLOL
    logger.info("Screen - Group Bean")
    css = configparser.ConfigParser()
    css.read(cssDir)
    return render_template('feijao.html', nome=nome, temp=temp, umidade=umidade, lencurva=lenCurva, arroz=arroz,
                           feijao=feijao, milho=milho, soja=soja, outro=outro, trigo=trigo, girassol=girassol,
                           custom=custom
                           , jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           , jumbotrom_w=css.get(str(lcd_type), 'all_jumbotrom_w')
                           , jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           , jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           , jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           , html_h=css.get(str(lcd_type), 'all_html_h')
                           , html_w=css.get(str(lcd_type), 'all_html_w')
                           , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                           , menu_width=css.get(str(lcd_type), 'config_menu_width')
                           , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top'))

@app.route('/grupo/milho') # Pagina que mostra as curvas do grupo Milho
@login_required
def milho():
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    config.read(langDir)
    tempRange = config.get(lang, 'nome-temperatura')
    umidRange = config.get(lang, 'nome-umidade')
    curvaStr = config.get(lang, 'curvas')
    arroz = config.get(lang, 'arroz')
    feijao = config.get(lang, 'feijao')
    milho = config.get(lang, 'milho')
    soja = config.get(lang, 'soja')
    outro = config.get(lang, 'outros')
    trigo = config.get(lang, 'trigo')
    girassol = config.get(lang, 'girassol')
    custom = config.get(lang, 'custom')
    curvaFiltradas = listGroup('MILHO')
    curva = getBasicInfo(2, 0)
    lenCurva = curva[4]
    nome = []
    temp = []
    umidade = []
    tempFormat = []
    umidadeFormat = []
    for index in range(0, lenCurva):

        name = listName()
        NameStr = name[index]
        indexCurva = name.index(NameStr)
        curvaCompleta = curvaFiltradas[indexCurva - 1]
        curvaNome = curvaCompleta[0]

        nameFull = ((curvaNome.split('<nome>'))[1].split('<nome>')[0])
        nameSplit = nameFull.split(';')
        nameSplitPt = nameSplit[0]
        if lang == 'PT':
            firstname, secondname = nameSplit[0].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)  # pegar apenas o nome em portugues
        elif lang == 'EN':
            firstname, secondname = nameSplit[1].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)   # pegar apenas o nome em ingles

        tempFull = ((curvaNome.split('<temp>'))[1].split('<temp>')[0])
        temp.append(tempFull.split(';'))
        tempFormat.append(temp[index])
        tempStr = tempFormat[index]
        tempLOL = tempRange + ' ' + tempFull[0] + ' - ' + tempStr[1]
        temp[index] = tempLOL

        umidadeFull = ((curvaNome.split('<umidade>'))[1].split('<umidade>')[0])
        umidade.append(umidadeFull.split(';'))
        umidadeFormat.append(umidade[index])
        umidadeStr = umidadeFormat[index]
        umidadeLOL = umidRange + ' ' + umidadeFull[0] + ' - ' + umidadeStr[1]
        umidade[index] = umidadeLOL
    logger.info("Screen - Group Corn")
    css = configparser.ConfigParser()
    css.read(cssDir)
    return render_template('milho.html', nome=nome, temp=temp, umidade=umidade, lencurva=lenCurva, arroz=arroz,
                           feijao=feijao, milho=milho, soja=soja, outro=outro, trigo=trigo, girassol=girassol,
                           custom=custom
                           , jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           , jumbotrom_w=css.get(str(lcd_type), 'all_jumbotrom_w')
                           , jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           , jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           , jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           , html_h=css.get(str(lcd_type), 'all_html_h')
                           , html_w=css.get(str(lcd_type), 'all_html_w')
                           , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                           , menu_width=css.get(str(lcd_type), 'config_menu_width')
                           , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top'))


@app.route('/grupo/soja') # Pagina que mostra as curvas do grupo Soja
@login_required
def soja():
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    config.read(langDir)
    tempRange = config.get(lang, 'nome-temperatura')
    umidRange = config.get(lang, 'nome-umidade')
    curvaStr = config.get(lang, 'curvas')
    arroz = config.get(lang, 'arroz')
    feijao = config.get(lang, 'feijao')
    milho = config.get(lang, 'milho')
    soja = config.get(lang, 'soja')
    outro = config.get(lang, 'outros')
    trigo = config.get(lang, 'trigo')
    girassol = config.get(lang, 'girassol')
    custom = config.get(lang, 'custom')
    curvaFiltradas = listGroup('SOJA')
    curva = getBasicInfo(3, 0)
    lenCurva = curva[4]
    nome = []
    temp = []
    umidade = []
    tempFormat = []
    umidadeFormat = []
    for index in range(0, lenCurva):

        name = listName()
        NameStr = name[index]
        indexCurva = name.index(NameStr)
        curvaCompleta = curvaFiltradas[indexCurva - 1]
        curvaNome = curvaCompleta[0]

        nameFull = ((curvaNome.split('<nome>'))[1].split('<nome>')[0])
        nameSplit = nameFull.split(';')
        nameSplitPt = nameSplit[0]
        if lang == 'PT':
            firstname, secondname = nameSplit[0].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)  # pegar apenas o nome em portugues
        elif lang == 'EN':
            firstname, secondname = nameSplit[1].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)   # pegar apenas o nome em ingles

        tempFull = ((curvaNome.split('<temp>'))[1].split('<temp>')[0])
        temp.append(tempFull.split(';'))
        tempFormat.append(temp[index])
        tempStr = tempFormat[index]
        tempLOL = tempRange + ' ' + tempFull[0] + ' - ' + tempStr[1]
        temp[index] = tempLOL

        umidadeFull = ((curvaNome.split('<umidade>'))[1].split('<umidade>')[0])
        umidade.append(umidadeFull.split(';'))
        umidadeFormat.append(umidade[index])
        umidadeStr = umidadeFormat[index]
        umidadeLOL = umidRange + ' ' + umidadeFull[0] + ' - ' + umidadeStr[1]
        umidade[index] = umidadeLOL
    logger.info("Screen - Group Soy")
    css = configparser.ConfigParser()
    css.read(cssDir)
    return render_template('soja.html', nome=nome, temp=temp, umidade=umidade, lencurva=lenCurva, arroz=arroz,
                           feijao=feijao, milho=milho, soja=soja, outro=outro, trigo=trigo, girassol=girassol,
                           custom=custom
                           , jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           , jumbotrom_w=css.get(str(lcd_type), 'all_jumbotrom_w')
                           , jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           , jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           , jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           , html_h=css.get(str(lcd_type), 'all_html_h')
                           , html_w=css.get(str(lcd_type), 'all_html_w')
                           , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                           , menu_width=css.get(str(lcd_type), 'config_menu_width')
                           , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top'))


@app.route('/grupo/outros') # Pagina que mostra as curvas do grupo Outros
@login_required
def outros():
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    config.read(langDir)
    tempRange = config.get(lang, 'nome-temperatura')
    umidRange = config.get(lang, 'nome-umidade')
    curvaStr = config.get(lang, 'curvas')
    arroz = config.get(lang, 'arroz')
    feijao = config.get(lang, 'feijao')
    milho = config.get(lang, 'milho')
    soja = config.get(lang, 'soja')
    outro = config.get(lang, 'outros')
    trigo = config.get(lang, 'trigo')
    girassol = config.get(lang, 'girassol')
    custom = config.get(lang, 'custom')
    curvaFiltradas = listGroup('OUTROS')
    curva = getBasicInfo(4, 0)
    lenCurva = curva[4]
    nome = []
    temp = []
    umidade = []
    tempFormat = []
    umidadeFormat = []
    for index in range(0, lenCurva):

        name = listName()
        NameStr = name[index]
        indexCurva = name.index(NameStr)
        curvaCompleta = curvaFiltradas[indexCurva - 1]
        curvaNome = curvaCompleta[0]

        nameFull = ((curvaNome.split('<nome>'))[1].split('<nome>')[0])
        nameSplit = nameFull.split(';')
        nameSplitPt = nameSplit[0]
        if lang == 'PT':
            firstname, secondname = nameSplit[0].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)  # pegar apenas o nome em portugues
        elif lang == 'EN':
            firstname, secondname = nameSplit[1].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)   # pegar apenas o nome em ingles

        tempFull = ((curvaNome.split('<temp>'))[1].split('<temp>')[0])
        temp.append(tempFull.split(';'))
        tempFormat.append(temp[index])
        tempStr = tempFormat[index]
        tempLOL = tempRange + ' ' + tempFull[0] + ' - ' + tempStr[1]
        temp[index] = tempLOL

        umidadeFull = ((curvaNome.split('<umidade>'))[1].split('<umidade>')[0])
        umidade.append(umidadeFull.split(';'))
        umidadeFormat.append(umidade[index])
        umidadeStr = umidadeFormat[index]
        umidadeLOL = umidRange + ' ' + umidadeFull[0] + ' - ' + umidadeStr[1]
        umidade[index] = umidadeLOL
    logger.info("Screen - Group Others")
    css = configparser.ConfigParser()
    css.read(cssDir)
    return render_template('outros.html', nome=nome, temp=temp, umidade=umidade, lencurva=lenCurva, arroz=arroz,
                           feijao=feijao, milho=milho, soja=soja, outro=outro, trigo=trigo, girassol=girassol,
                           custom=custom
                           , jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           , jumbotrom_w=css.get(str(lcd_type), 'all_jumbotrom_w')
                           , jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           , jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           , jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           , html_h=css.get(str(lcd_type), 'all_html_h')
                           , html_w=css.get(str(lcd_type), 'all_html_w')
                           , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                           , menu_width=css.get(str(lcd_type), 'config_menu_width')
                           , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top'))


@app.route('/grupo/trigo') # Pagina que mostra as curvas do grupo Trigo
@login_required
def trigo():
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    config.read(langDir)
    tempRange = config.get(lang, 'nome-temperatura')
    umidRange = config.get(lang, 'nome-umidade')
    curvaStr = config.get(lang, 'curvas')
    arroz = config.get(lang, 'arroz')
    feijao = config.get(lang, 'feijao')
    milho = config.get(lang, 'milho')
    soja = config.get(lang, 'soja')
    outro = config.get(lang, 'outros')
    trigo = config.get(lang, 'trigo')
    girassol = config.get(lang, 'girassol')
    custom = config.get(lang, 'custom')
    curvaFiltradas = listGroup('TRIGO')
    curva = getBasicInfo(5, 0)
    lenCurva = curva[4]
    nome = []
    temp = []
    umidade = []
    tempFormat = []
    umidadeFormat = []
    for index in range(0, lenCurva):

        name = listName()
        NameStr = name[index]
        indexCurva = name.index(NameStr)
        curvaCompleta = curvaFiltradas[indexCurva - 1]
        curvaNome = curvaCompleta[0]

        nameFull = ((curvaNome.split('<nome>'))[1].split('<nome>')[0])
        nameSplit = nameFull.split(';')
        nameSplitPt = nameSplit[0]
        if lang == 'PT':
            firstname, secondname = nameSplit[0].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)  # pegar apenas o nome em portugues
        elif lang == 'EN':
            firstname, secondname = nameSplit[1].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)   # pegar apenas o nome em ingles

        tempFull = ((curvaNome.split('<temp>'))[1].split('<temp>')[0])
        temp.append(tempFull.split(';'))
        tempFormat.append(temp[index])
        tempStr = tempFormat[index]
        tempLOL = tempRange + ' ' + tempFull[0] + ' - ' + tempStr[1]
        temp[index] = tempLOL

        umidadeFull = ((curvaNome.split('<umidade>'))[1].split('<umidade>')[0])
        umidade.append(umidadeFull.split(';'))
        umidadeFormat.append(umidade[index])
        umidadeStr = umidadeFormat[index]
        umidadeLOL = umidRange + ' ' + umidadeFull[0] + ' - ' + umidadeStr[1]
        umidade[index] = umidadeLOL
    logger.info("Screen - Group Wheat")
    css = configparser.ConfigParser()
    css.read(cssDir)
    return render_template('trigo.html', nome=nome, temp=temp, umidade=umidade, lencurva=lenCurva, arroz=arroz,
                           feijao=feijao, milho=milho, soja=soja, outro=outro, trigo=trigo, girassol=girassol,
                           custom=custom
                           , jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           , jumbotrom_w=css.get(str(lcd_type), 'all_jumbotrom_w')
                           , jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           , jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           , jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           , html_h=css.get(str(lcd_type), 'all_html_h')
                           , html_w=css.get(str(lcd_type), 'all_html_w')
                           , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                           , menu_width=css.get(str(lcd_type), 'config_menu_width')
                           , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top'))


@app.route('/grupo/girassol') # Pagina que mostra as curvas do grupo Girassol
@login_required
def girassol():
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    config.read(langDir)
    tempRange = config.get(lang, 'nome-temperatura')
    umidRange = config.get(lang, 'nome-umidade')
    curvaStr = config.get(lang, 'curvas')
    arroz = config.get(lang, 'arroz')
    feijao = config.get(lang, 'feijao')
    milho = config.get(lang, 'milho')
    soja = config.get(lang, 'soja')
    outro = config.get(lang, 'outros')
    trigo = config.get(lang, 'trigo')
    girassol = config.get(lang, 'girassol')
    custom = config.get(lang, 'custom')
    curvaFiltradas = listGroup('GIRASSOL')
    curva = getBasicInfo(6, 0)
    lenCurva = curva[4]
    nome = []
    temp = []
    umidade = []
    tempFormat = []
    umidadeFormat = []
    for index in range(0, lenCurva):

        name = listName()
        NameStr = name[index]
        indexCurva = name.index(NameStr)
        curvaCompleta = curvaFiltradas[indexCurva - 1]
        curvaNome = curvaCompleta[0]

        nameFull = ((curvaNome.split('<nome>'))[1].split('<nome>')[0])
        nameSplit = nameFull.split(';')
        nameSplitPt = nameSplit[0]
        if lang == 'PT':
            firstname, secondname = nameSplit[0].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)  # pegar apenas o nome em portugues
        elif lang == 'EN':
            firstname, secondname = nameSplit[1].split(',')
            realname = firstname + ' ' + secondname
            nome.append(realname)   # pegar apenas o nome em ingles

        tempFull = ((curvaNome.split('<temp>'))[1].split('<temp>')[0])
        temp.append(tempFull.split(';'))
        tempFormat.append(temp[index])
        tempStr = tempFormat[index]
        tempLOL = tempRange + ' ' + tempFull[0] + ' - ' + tempStr[1]
        temp[index] = tempLOL

        umidadeFull = ((curvaNome.split('<umidade>'))[1].split('<umidade>')[0])
        umidade.append(umidadeFull.split(';'))
        umidadeFormat.append(umidade[index])
        umidadeStr = umidadeFormat[index]
        umidadeLOL = umidRange + ' ' + umidadeFull[0] + ' - ' + umidadeStr[1]
        umidade[index] = umidadeLOL
    logger.info("Tela - Group Sunflower")
    css = configparser.ConfigParser()
    css.read(cssDir)
    return render_template('girassol.html', nome=nome, temp=temp, umidade=umidade, lencurva=lenCurva, arroz=arroz,
                           feijao=feijao, milho=milho, soja=soja, outro=outro, trigo=trigo, girassol=girassol,
                           custom=custom
                           , jumbotrom_h=css.get(str(lcd_type), 'all_jumbotrom_h')
                           , jumbotrom_w=css.get(str(lcd_type), 'all_jumbotrom_w')
                           , jumbotrom_margin_left=css.get(str(lcd_type), 'all_jumbotrom_margin_left')
                           , jumbotrom_margin_top=css.get(str(lcd_type), 'all_jumbotrom_margin_top')
                           , jumbotrom_padding=css.get(str(lcd_type), 'all_jumbotrom_padding')
                           , html_h=css.get(str(lcd_type), 'all_html_h')
                           , html_w=css.get(str(lcd_type), 'all_html_w')
                           , menu_icon_size=css.get(str(lcd_type), 'config_menu_icon_size')
                           , menu_width=css.get(str(lcd_type), 'config_menu_width')
                           , menu_margin_top=css.get(str(lcd_type), 'config_menu_margin_top'))


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    logger.info("Server Start")
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    http_server.serve_forever()

