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

def mask2int(mask='255.255.255.0'):
    '''
    1.  '255.11111.266.4' to '255.255.255.0' to 24
    2.  '255.128.255.0'  to 9
    '''
    mask_list = mask.split('.')
    mask_list = map(int,mask_list)                            # int list
    notexcess = lambda x: ( x > 255) and 255 or x           # if any one bigger than 255, set to 255
    addzero= lambda x : ( x not in "10" ) and '0' or x
    mask_list = map(notexcess, mask_list)
    # print( mask_list)
    binmask_total=''
    for x in range(4):
        binmask = "%8s" %bin(mask_list[x]).split('0b')[1]   #  '    1101'
        binmask = ''.join(map(addzero,list(binmask)))       #  '00001101'  , addzero
        binmask_total += binmask
    zindex = binmask_total.index('0')
    return  zindex

def help():
    print 'help info...'
    sys.exit(1)

def main():
    '''
    ip = '10.69.231.70'
    net = '29'
    ip = subnet_correct(ip, net)
    '''
    # print mask2int('224.0.0.0')
    # mask_correcter('255.128.255.0')

    args = sys.argv
    net = args[1].split('/')

    if len(net) == 1 or net[1]=='':   # assume it's a mask
        net = net[0]
        print mask2int(net)
    else:                             # in form like 192.168.1.2/24
        net,mask = net
        print subnet_correct(net,mask)

if __name__ == '__main__':
    main()
