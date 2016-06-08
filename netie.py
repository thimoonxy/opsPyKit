#!/usr/bin/env python
# encoding=utf-8
# Author: Simon Xie(Simon)
# E-mail: thimoon@sina.com
'''
Target: enable every func in http://tool.chinaz.com/Tools/subnetmask
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def subnet_correct(ip, postfix='32'):
    """
    This func corrects wrong subnet, e.g.
    if found 10.69.231.70/29, it'll be corrected to 10.69.231.64/29.
    """
    ip = ip.split('.')
    net = int(postfix)
    fullnet = '0b11111111'
    zeronet = '0b00000000'
    if net <= 8:
        hosts = 8 - net
        net = '0b' + '1'* net + '0' * hosts
        net = (net, zeronet, zeronet, zeronet)
    elif 8 < net <= 16:
        hosts = 16 - net
        net = '0b' + '1'* net + '0' * hosts
        net = (fullnet, net, zeronet, zeronet)
    elif 16 < net <= 24:
        hosts = 24 - net
        net = '0b' + '1'* net + '0' * hosts
        net = (fullnet, fullnet, net, zeronet)
    else:
        hosts = 32 - net
        net = '0b' + '1'* net + '0' * hosts
        net = (fullnet, fullnet, fullnet, net)
    for x in range(len(ip)):
        # print ip[x], type(net[x])
        ip[x] = int(ip[x]) & int(net[x], 2)
    ip = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3])
    return  ip

def simplify_mask(mask='255.255.255.0',net_number=8):
    mask = mask.split('.')
    mask = map(int,mask)            #   [255, 255, 255, 0]
    power = lambda x: 2**x
    meta = map(power,range(8))      #   [1, 2, 4, 8, 16, 32, 64, 128]
    meta.reverse()                  #   [128, 64, 32, 16, 8, 4, 2, 1]
    result = 0

    def complicate(mask=255):
        for net_number in range(8,-1,-1):
            hosts = 8 - net_number
            net = '0b' + '1'* net_number + '0' * hosts
            print  net,int(net,2), net_number
            if int(net,2) == mask:
                 return net_number
    return  complicate(248)
def main():
    '''
    ip = '10.69.231.70'
    net = '29'
    ip = subnet_correct(ip, net)
    '''
    print simplify_mask('254.0.0.0')


if __name__ == '__main__':
    main()
