import serial, time

windows = 'COM4'
linux = '/dev/ttyUSB0'
porta = linux
def getOsc(input):
    # type: (object) -> object
    try:
        port = serial.Serial(porta, baudrate=115200, timeout=.25)
        while True:
            port.write(input)
            resposta = port.readline()
            if resposta == '':
               # port.close()
                return('TIMEOUTsplit')
            else:
                return (resposta)
    except Exception as e:
        print("Erro' %s" % e)

def getHx(input):
    try:
        port = serial.Serial(porta, baudrate=115200, timeout=1)
        while True:
            port.write(input)
            resposta = port.read(64)
            if resposta == '':
                return('0BTIMEOUT##')
            else:
                return (resposta)
    except Exception as e:
        print("Erro' %s" % e)

def getGps(input):
    # type: (object) -> object
    try:
        port = serial.Serial(porta, baudrate=115200, timeout=2)
        while True:
            port.write(input)
            resposta = port.readline()
            if resposta == '':
               # port.close()
                return('TIMEOUTsplit')
            else:
                return (resposta)
    except Exception as e:
        print("Erro' %s" % e)

class gps:

    @staticmethod
    def read():
        receiveGPS = getGps('07GPSOK')
        #string = receiveGPS.split('\r\n')
        gpsStr = receiveGPS.find('$GPGGA')
        gpsStr2 = receiveGPS.find('$GPGSA')
        gps = receiveGPS[gpsStr:gpsStr2]

        return gps

    @staticmethod
    def array():
        a = gps.read()
        array = a.split(',')
        return array

    @staticmethod
    def utc():
        a = gps.read()
        utc = a.split(',')
        return utc[1]

    @staticmethod
    def lat():
        a = gps.read()
        lat = a.split(',')
        try:
            if lat[3] == 'S':
                latConvert = float(lat[2])/-100
        except:
            latConvert = 0
        return str(latConvert)

    @staticmethod
    def log():
        a = gps.read()
        log = a.split(',')
        try:
            if log[5] == 'W':
                logConvert = float(log[4])/-100
        except:
            logConvert = 0
        return str(logConvert)


    @staticmethod
    def quality():
        a = gps.read()
        qual = a.split(',')
        return qual[6]

    @staticmethod
    def nsat():
        a = gps.read()
        nsat = a.split(',')
        return nsat[7]

    @staticmethod
    def alt():
        a = gps.read()
        alt = a.split(',')
        return alt[9]

    @staticmethod
    def check():
        a = gps.read()
        check = a.split(',')

        return check[14]

class calibra:
    @staticmethod
    def zero():
        # type: (object) -> object
        try:
            input = "07CALI0"
            port = serial.Serial(porta, baudrate=115200, timeout=30)
            while True:
                port.write(input)
                resposta = port.readline()
                if resposta == '':
                    # port.close()
                    return ('TIMEOUT')
                else:
                    return (resposta)
        except Exception as e:
            print("Erro' %s" % e)
    @staticmethod
    def duzentos():
        # type: (object) -> object
        try:
            input = "07CALI2"
            port = serial.Serial(porta, baudrate=115200, timeout=30)
            while True:
                port.write(input)
                resposta = port.readline()
                if resposta == '':
                    # port.close()
                    return ('TIMEOUT')
                else:
                    return (resposta)
        except Exception as e:
            print("Erro' %s" % e)

if __name__ == '__main__':
    a = getHx('07SHAF1')
    print a
