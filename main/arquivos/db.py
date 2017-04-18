import MySQLdb

from flask import session
from arquivos.rwconf import writeConf
from MySQLdb import escape_string as thwart
import configparser
config = configparser.ConfigParser()
from curvasHandler import *
import gc


def connectiondb(): # FUncao de conexao com o banco
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="flashball",
                           db="chip")
    c = conn.cursor()

    return c, conn

def load_parameters(): # Funcao que carrega os parametros do banco
    username = session['username']
    cursor, conn = connectiondb()
    x = cursor.execute("SELECT * FROM users WHERE username = (%s)",
                  [(username)])
    for row in cursor:
        b = row

    name = b[3]
    lang = b[5]
    writeConf('DEFAULT', 'LANG', lang)
    unitemp = b[6]
    writeConf('DEFAULT', 'unitemp', unitemp)
    ph = b[7]
    writeConf('DEFAULT', 'ph', ph)
    media = b[8]
    writeConf('DEFAULT', 'media', media)

def update_chumballoy(): # Funcao que atualiza o usuario com base no banco
    config = configparser.ConfigParser()
    config.read(confDir)
    lang = config.get('DEFAULT', 'LANG')
    ph = config.get('DEFAULT', 'ph')
    unitemp = config.get('DEFAULT', 'unitemp')
    media = config.get('DEFAULT', 'media')
    user = session['username']
    cursor, conn = connectiondb()
    data = cursor.execute("SELECT * FROM users WHERE username = (%s)", [thwart(user)])
    for row in cursor:
        b = row
    uid = b[0]
    cursor.execute(
            "UPDATE `users` SET lang = %s, ph = %s, unitemp = %s, media = %s  WHERE `users`.`uid` = %s ;", (lang, ph, unitemp, media, str(uid)))
    conn.commit()
    cursor.close()
    conn.close()
    gc.collect()