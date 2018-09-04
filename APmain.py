import socket
import network
import os

def AP_main( ):
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()#创建套接字
    s.bind(addr)#绑定地址(host,port)到套接字
    s.listen(2)#TCP监听
    print('listening on', addr)


    Web_admin=open('main.html','r')
    main_html=Web_admin.read()
    Web_admin.close()
    Web_admin=open('ok.html','r')
    ok_html=Web_admin.read()
    Web_admin.close()

    while True:
        cl, addr = s.accept()#被动接受TCP客户端连接,(阻塞式)等待连接的到来
        print(cl)
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)#创建一个与该套接字相关连的文件
        req =cl.readline()
        print(req)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
                req+=(line.decode('utf-8').lower())
        sid, sec, pas, sck = Section( req )
        if(sid != '-1' and sec != '-1' and pas != '-1' and sck != '-1'):
            str_data = sid + ',' + sec + ',' + pas + ',' + sck 
            input = open('data.txt', 'w')
            input.write(str_data)
            input.close()
            cl.send(ok_html)
            cl.close() 
            break
        cl.send(main_html)
        cl.close() 
        
    
def Section( data ):
    data=data.decode('utf-8').split('\r\n')
    data=data[0].lstrip().rstrip().replace(' ','')
    data=data.replace('get/?','').replace('http/1.1','').replace('GET/','').replace('GET/?','').replace('HTTP/1.1','')
    try:
        print('data = ',data)
        req_datas = list(data.split('&'))
        bit_0 = list(req_datas[0].split('='))[1]
        bit_1 = list(req_datas[1].split('='))[1]
        bit_2 = list(req_datas[2].split('='))[1]
        bit_3 = list(req_datas[3].split('='))[1]
    except:
        bit_0 = "-1"
        bit_1 = "-1"
        bit_2 = "-1"
        bit_3 = "-1"
    return bit_0,bit_1,bit_2,bit_3