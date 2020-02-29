import serial
import time
import threading

readings={'rssi':0,'send_num':0,'x':0,'y':0,'h':0,'pressure':0,
'temperature':0, 'air_quality':0, 'pm25':0, 'pm10':0,'humidity':0,'battery':0}

readings['rssi']=0 #defaultowe rssi

DIR='C:/Users/aszab/desktop/TMP/'

file = open(DIR+"raw.txt","r")
fields = file.readlines()
file.close()

def load_reading(line_num):
    readings['rssi']= str(fields[line_num].split('_')[2])
    readings['send_num'] = str(fields[line_num].split('_')[3])
    readings['x'] = str(fields[line_num].split('_')[4])
    readings['y'] = str(fields[line_num].split('_')[5])
    readings['h'] = str(fields[line_num].split('_')[6])
    readings['pressure'] = str(fields[line_num].split('_')[7])
    readings['temperature'] = str(fields[line_num].split('_')[8])
    readings['air_quality'] = str(fields[line_num].split('_')[9])
    readings['pm25'] = str(fields[line_num].split('_')[10])
    readings['pm10'] = str(fields[line_num].split('_')[11])
    readings['humidity'] = str(fields[line_num].split('_')[12])
    readings['battery'] = str(fields[line_num].split('_')[13])



'''
    file = open(DIR+"BMP280.txt","r")

    fields = file.readlines()

    readings['temperature'] = str(fields[line_num].split(' ')[0])
    readings['pressure'] = str(fields[line_num].split(' ')[1])

    file.close()

    file = open(DIR+"SPS30.txt","r")

    fields = file.readlines()

    readings['pm25'] = str(fields[line_num].split(' ')[1])
    readings['pm10'] = str(fields[line_num].split(' ')[3])

    file.close()

'''




structure=['rssi','send_num','x','y','h','pressure', 'temperature', 'air_quality', 'pm25', 'pm10','humidity','battery']
line_num=0
print("press enter")
input()
with serial.Serial('com1', 19200, timeout=1) as ser:
    while(line_num<4600):
        load_reading(line_num)
        text=''
        for s in structure:
            text+=(str(readings[s])+'_')
        text=text[:-1]+'\'\n'
        print(text)
        #print(c.mesurments)
        ser.write(text.encode())
        time.sleep(0.2)
        line_num=line_num+1
