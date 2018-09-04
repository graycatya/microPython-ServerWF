import socket
import network
import APmain
import WF_network #import an_WF,ap_WF_open
import server_dht22
import os
import machine
from machine import Pin,I2C,SPI,Timer
import math
import ssd1306
import time

spi = SPI(baudrate=10000000, polarity=1, phase=0, sck=Pin(14,Pin.OUT), mosi=Pin(13,Pin.OUT), miso=Pin(12))
display = ssd1306.SSD1306_SPI(128, 64, spi, Pin(5),Pin(4), Pin(16))

p15 = Pin(15, Pin.IN)
p0 = Pin(0, Pin.IN)



WF_data = ""


for x in range(0, 64):
    display.fill(0)
    for y in range(0, 10):
        display.pixel(128-(x+y), 32+int(math.cos(x/32*math.pi)*30 +2), 1)
        display.pixel(128-(x+y), 32+int(math.cos((x+32)/32*math.pi)*30 +2), 1)
        display.pixel(x+y, 32+int(math.cos(x/32*math.pi)*30 +2), 1)
        display.pixel(x+y, 32+int(math.cos((x+32)/32*math.pi)*30 +2), 1)
    display.show()

try:
    input = open('data.txt')
    print("yes")
    WF_data = input.read()
    input.close()
    print(WF_data)
    WF_network.ap_WF_open(False)#关闭局域网
except:
    print("no")
    WF_network.ap_WF_open(True)#创建局域网
    APmain.AP_main() #服务器创建

"""
打开文件加载数据
"""
WF_network.ap_WF_open(False)#关闭局域网
input = open('data.txt')
WF_data = input.read()
WF_data = WF_data.split(',')

key0_bot = 1
key1_bot = 1
key1_num = 0
key0_bol_2 = True
key1_bol = True
key0_bol_1 = True

def Send_data(t):
    if ( key0_bol_1 == True ):
        display.fill(0)
        display.text('Send mail..',23,31)
        display.show()
        time.sleep(0.5)
        server_dht22.SendData(WF_data[3])
        display.fill(0)
        display.text('Send mail....',16,31)
        display.show()
        time.sleep(0.5)

tim = Timer(-1)  #新建一个虚拟定时器



while True:
    wlan = network.WLAN(network.STA_IF)  # 设置开发板的网
    WF_bit = WF_network.an_WF(WF_data[0], WF_data[2], WF_data[1])
    print('WF_bit = ', WF_bit)
    tim.init(period=60000, mode=Timer.PERIODIC, callback=Send_data) #打开定时器
    while True:


        if( p15.value() == 1 and key1_bot == 1 ): #C-F温度算法切换
            key1_bol = ~key1_bol
            key1_bot = 0
        elif p15.value() == 0:
            key1_bot = 1

        if( p0.value() == 0 and key0_bot == 1 ): #短按关闭或打开发送数据位
            key0_bol_1 = ~key0_bol_1 
            key0_bot = 0
        elif ( p0.value() == 1 ):
            key1_num = 0
            key0_bot = 1
        elif ( p0.value() == 0 ):
            key1_num = key1_num + 1
            if( key1_num == 20 ):
                display.fill(0)
                display.text('remove....',17,31)
                display.show()
                time.sleep_ms(500)
                os.remove( 'data.txt' )
                display.fill(0)
                display.text('remove......',10,31)
                display.show()
                time.sleep_ms(500)

        tem, hum = server_dht22.dht22_read( key1_bol )

        display.fill(0)
        if(not wlan.isconnected()):
            display.text('WF:OFF',1,1)
        else:
            display.text('WF:ON',1,1)
        display.text('|',50,1)
        for x in range(0, 128):
            display.text('_',x,4)
        display.text('|',50,1)
        if( key0_bol_1  == True ):
            display.text('SEND:ON',60,1)
        else:
            display.text('SEND:OFF',60,1)
        display.text(tem,20,30)
        display.text(hum,20,45)
        display.show()

        #print(tem + ' ' + hum)
        time.sleep_ms(100)