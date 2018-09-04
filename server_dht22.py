# coding=utf-8
import urequests
import dht
import machine
from machine import Pin

class AlarmSystem:
    def __init__(self):
        self.d = dht.DHT22(machine.Pin(10))

    def dht22(self):
        try:
            self.d.measure()
            return 'Temp:'+str(self.d.temperature())+'°C---Hum:'+str(self.d.humidity())+'%'
        except:
            return '0'


    def push(self, sckey, result):
        import network
        try:
            title = "方糖提示您:注意天气变化保持健康心情"
            content = 'text='+title+'&'+'desp='+result
            url="https://sc.ftqq.com/"+sckey+".send?"+content
            r = urequests.get(url)
            r.close()
        except:
            print("GET OFF")



p2=Pin(2,Pin.OUT)
ser_dht22 = AlarmSystem()

def dht22_read( bit ):
    try:
        d = dht.DHT22(machine.Pin(10))
        d.measure()
        if( bit == True ):
            return 'Temp:'+str(d.temperature())+'\'C', 'Hum:'+str(d.humidity())+'%'
        else:
            return 'Temp:'+str((float(int((d.temperature()*1.8+32)*10)))/10)+'\'F', 'Hum:'+str(d.humidity())+'%'
    except:
        return 'Temp:'+'-------', 'Hum:'+'-------'

def SendData(sckey):
    p2.value(not p2.value())
    data_= ser_dht22.dht22()
    if(data_!='0'):
        print(data_)
        ser_dht22.push(sckey, data_)
    else:
        print('GET Data Fail')
