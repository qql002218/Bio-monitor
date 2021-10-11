from socket import *
udp_ser = socket(AF_INET, SOCK_DGRAM)  # 数据报式的套接字
udp_ser.bind(('10.192.57.114', 9008))

while 1:
    data = udp_ser.recvfrom(1024)
    print(data)
    udp_ser.sendto('data'.encode('utf-8'), data[1])
# udp_ser.close()