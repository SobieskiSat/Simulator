from Sensor import Sensor
import serial
import time
import threading

class CanSat:
    def __init__(self, mesurments):
        # Lisy of all used sensors
        self.sensors = []
        #Messurments responses from all sensors
        self.mesurments=mesurments

    def update(self):
        self.past_mesurments=self.mesurments.copy()
        for s in self.sensors:
            s.update()
            for k, v in s.mesurments.items():
                self.mesurments[k]=v

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def remove_sensor(self, name):
        pass

    def get_all_sensors(self):
        return self.sensors

    def get_mesurments(self, id):
        try:
            return self.mesurments[id]
        except Exception as e:
            print(e)

    def get_delta(self, id):
        try:
            return self.past_mesurments[id]-self.mesurments[id]
        except Exception as e:
            print(e)

    def get_all_deltas(self):
        mes=[]
        for m in self.past_mesurments:
            mes.append({m.key:self.get_delta(m.key)})

class Reader:
    def __init__(self, mesurments):
        self.sat = CanSat(mesurments)

    def keep_reading(self, call, condition):
        while(condition):
            self.sat.update()
            deltas = self.sat.get_all_deltas()
            mes = self.sat.mesurments.copy()
            for d in deltas:
                pass


mesurments = {'x':50.5, 'y':19.5, 'h':504, 'temperature':23, 'pm10':50}

c = CanSat(mesurments)
def get_speial(id):
    special = {'wx':10, 'wy':5}
    return special[id]

gps = Sensor('GPS')

gps.add_measurement('x', 'd.x + d.wx*r(-0.00001, 0.00002)', 6)
gps.add_dependency('x', c.get_mesurments, 'x')
gps.add_dependency('wx', get_speial, 'wx')

gps.add_measurement('y', 'd.y + d.wy*r(-0.000002, 0.00004)', 6)
gps.add_dependency('y',c.get_mesurments, 'y')
gps.add_dependency('wy', get_speial , 'wy')

gps.add_measurement('h', 'd.h + r(-1, 0.1)', 2)
gps.add_dependency('h', c.get_mesurments, 'h')
c.add_sensor(gps)

bmp = Sensor('BMP280')

bmp.add_measurement('pressure', '1013-d.h/8*r(0.99,1.01)', 2)
bmp.add_dependency('h', c.get_mesurments, 'h')

bmp.add_measurement('temperature', 'd.t-d.dh/100*r(0.9, 1.1)', 2)
bmp.add_dependency('t', c.get_mesurments, 'temperature')
bmp.add_dependency('dh', c.get_delta, 'h')

c.add_sensor(bmp)

radio = Sensor('Radio')

radio.add_measurement('rssi', 'r(30, 50)', 0)
c.add_sensor(radio)

sps = Sensor('SPS')

sps.add_measurement('pm10', 'r(10, 200)', 2)

sps.add_dependency('pm10', c.get_mesurments, 'pm10')
sps.add_measurement('pm25', 'd.pm10*r(0.8, 1.2)', 2)

c.add_sensor(sps)
structure=['rssi','x','y', 'h', 'temperature', 'pressure', 'pm25', 'pm10']
with serial.Serial('com10', 19200, timeout=1) as ser:
    while(c.mesurments['h']>0):
        c.update()
        text=''
        for s in structure:
            text+=(str(mesurments[s])+'_')
        text=text[:-1]+'\'\n'
        print(text)
        #print(c.mesurments)
        ser.write(text.encode())
        time.sleep(0.3)
