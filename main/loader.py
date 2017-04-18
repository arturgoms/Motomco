import configparser
from flask import Flask
from flask import render_template
from gevent.pywsgi import WSGIServer
confDir = 'conf.ini'
app = Flask(__name__)
@app.route("/") # Pagina inicial: faz o autoteste e redireciona para a tela de medir
def index():
    config = configparser.ConfigParser()
    config.read(confDir)
    firstTime = config.get('DEFAULT', 'FIRST-TIME')

    if firstTime == 'YES':
        return render_template("index2.html")
    else:
        return render_template("index.html")

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 1212), app)
    http_server.serve_forever()
