import os

from wifi import Cell, Scheme

port = 'wlan0'
class connection(): # Classe que lida com o WIFI da placa
    class wifi():
        @staticmethod
        def list():
            list = Cell.all(port)
            return list
        @staticmethod
        def connect(rede, nome, key):
            cell = Cell.all(port)[int(rede)]
            scheme = Scheme.for_cell(port, 'home', cell, key)
            scheme.save()
            scheme.activate()

    @staticmethod
    def is_connect():
        is_connect = os.popen("ping -c 1 google.com").read()
        if is_connect == '':
            return False
        else:
            return True


if __name__ == '__main__':
        b = connection.is_connect()
        print b

