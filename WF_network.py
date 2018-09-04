

def ap_WF_open( bit ):
    """设置成"""
    import network
    import machine
    from machine import Pin,I2C,SPI,Timer
    import ssd1306
    spi = SPI(baudrate=10000000, polarity=1, phase=0, sck=Pin(14,Pin.OUT), mosi=Pin(13,Pin.OUT), miso=Pin(12))
    display = ssd1306.SSD1306_SPI(128, 64, spi, Pin(5),Pin(4), Pin(16))
    if( bit == True ):
        try:
            display.poweron()
            display.init_display()
            print( 'AP_set......' )
            display.fill(0)
            display.text('AP_set......',17,31)
            display.show()

        except Exception as ex: 
            #led_blue.value(0)
            print('Unexpected error: {0}'.format(ex))
            display.poweroff()

    ap = network.WLAN(network.AP_IF) # create access-point interface
    if( bit == True ):
        ap.active(True)         # activate the interface
        #设置成开放
        ap.config(essid='Sev-AP',authmode=network.AUTH_OPEN) # set the ESSID of the access point,password='xxx'et the ESSID of the access point,password='xxx'
    else:
        ap.active(False) 



def an_WF(WFname, WFpassword, WFpattern):
    """定义开发板连接无线网络的函数,返回MAC"""
    import network
    import time
    import machine
    from machine import Pin,I2C,SPI,Timer
    import ssd1306
    spi = SPI(baudrate=10000000, polarity=1, phase=0, sck=Pin(14,Pin.OUT), mosi=Pin(13,Pin.OUT), miso=Pin(12))
    display = ssd1306.SSD1306_SPI(128, 64, spi, Pin(5),Pin(4), Pin(16))

    try:
        display.poweron()
        display.init_display()
        print( 'loading......' )

    except Exception as ex: 
        #led_blue.value(0)
        print('Unexpected error: {0}'.format(ex))
        display.poweroff()

    summ = 0
    wlan = network.WLAN(network.STA_IF)  # 设置开发板的网

    wlan.active(True)  # 打开网络连接

    if not wlan.isconnected():  # 判断是否有网络连接

        print('connecting to network...')
        display.fill(0)
        display.text('loading...',23,31)
        display.show()
        # 设置想要连接的无线网络
        if WFpattern == '1':
            wlan.connect(WFname)
        else:
            wlan.connect(WFname, WFpassword)

        while not wlan.isconnected():  # 等待连接上无线网络
            time.sleep(1)
            summ = summ + 1
            display.fill(0)
            if( summ <=5):
                display.text('loading...',23,31)
            if( summ > 5 and summ <= 10 ):
                display.text('loading....',17,31)
            if( summ > 10 and summ <= 15 ):
                display.text('loading.....',13,31)
            if( summ > 15 and summ <= 20 ):
                display.text('loading......',10,31)
            display.show()
            if summ==20:
                return "WF:OFF"
    return "WF:ON"

    """
    mac = wlan.config('mac')      # 获取模块MAC地址
    print('networkconfig:', wlan.ifconfig())
    return mac    
    """