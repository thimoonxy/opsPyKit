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


addzero= lambda x : ( x not in "10" ) and '0' or x

def ip2network_address(ip, cidr='32'):
    """
    This func also corrects wrong subnet, e.g.
    if found 10.69.231.70/29, it'll be corrected to 10.69.231.64/29.
    """
    ip = ip.split('.')
    netmask = cidr2mask(cidr)
    bin_mask_list = ip2binlist(netmask)
    for x in range(len(ip)):
        ip[x] = int(ip[x]) & int(bin_mask_list[x], 2)
    if int(cidr) < 31:
        network_address = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3])
        first_avail_ip = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3]+1)
        avail_host_numbers = 2 ** (32 - int(cidr)) - 2
        complement_bin_list = mask2complement_bin_list(netmask)
        broadcast_address = '.'.join([ str(ip[x]+int(complement_bin_list[x],2)) for x in range(4)])
        last_avail_ip_list = broadcast_address.split('.')[0:3]
        last_avail_ip_list.append( str( int(broadcast_address.split('.')[-1]) -1 ) )
        last_avail_ip = '.'.join(last_avail_ip_list)
    elif int(cidr) == 31:
        broadcast_address = network_address = None
        first_avail_ip = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3])
        last_avail_ip = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3]+1)
        avail_host_numbers = 2
    else:
        broadcast_address = network_address = None
        first_avail_ip = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3])
        last_avail_ip = first_avail_ip
        avail_host_numbers = 1
    return  avail_host_numbers, netmask, network_address, first_avail_ip,last_avail_ip, broadcast_address

def mask2cidr(mask='255.255.255.0'):
    '''
    1.  '255.11111.266.4' to '255.255.255.0' to 24
    2.  '255.128.255.0'  to 9
    '''
    mask_list = mask.split('.')
    mask_list = map(int,mask_list)                          # int list
    notexcess = lambda x: ( x > 255) and 255 or x          # if any one bigger than 255, set to 255
    # addzero= lambda x : ( x not in "10" ) and '0' or x    # set as global func
    mask_list = map(notexcess, mask_list)
    binmask_total=''
    for x in range(4):
        binmask = "%8s" %bin(mask_list[x]).split('0b')[1]   #  '    1101'
        binmask = ''.join(map(addzero,list(binmask)))       #  '00001101'  , addzero
        binmask_total += binmask
    try:
        zindex = binmask_total.index('0')
    except ValueError:
        zindex = 32
    return  zindex

def cidr2mask(cidr='24'):
    cidr=int(cidr)
    fullnet = '0b11111111'
    zeronet = '0b00000000'
    if cidr <= 8:
        hosts = 8 - cidr
        net = '0b' + '1'* cidr + '0' * hosts
        net = (net, zeronet, zeronet, zeronet)
    elif 8 < cidr <= 16:
        hosts = 16 - cidr
        net = '0b' + '1'* (cidr-8) + '0' * hosts
        net = (fullnet, net, zeronet, zeronet)
    elif 16 < cidr <= 24:
        cidr = cidr - 16
        hosts = 8 - cidr
        net = '0b' + '1'* cidr + '0' * hosts
        net = (fullnet, fullnet, net, zeronet)
    else:
        cidr = cidr - 24
        hosts = 8 - cidr
        # print cidr,hosts
        net = '0b' + '1'* cidr + '0' * hosts
        net = (fullnet, fullnet, fullnet, net)
    netmask = '.'.join([ str(int(net[x], 2)) for x in range(len(net)) ])
    return netmask

def cidr2hex(cidr='24'):
    netmask = cidr2mask(cidr)
    bin_mask_list = ip2binlist(netmask)
    hex_list = [ hex(int(b,2)).split('0x')[1].upper() for b in bin_mask_list ]
    return hex_list


def mask2complement_bin_list(mask='255.255.255.0'):
    xcomplement_bin_list = ip2binlist(mask)
    anti = lambda x: (x == '1') and '0' or '1'
    complement_bin_list = [  ''.join(map(anti,list(x))) for x in xcomplement_bin_list ]
    return  complement_bin_list

def ipmask2network_address(ip, mask):
    cidr = mask2cidr(mask)
    return ip2network_address(ip, cidr)

def ip2binlist(ip):
    iplist = ip.split('.')
    iplist = map(int,iplist)
    binlist = []
    for x in range(4):
        binmask = "%8s" %bin(iplist[x]).split('0b')[1]   #  '    1101'
        binmask = ''.join(map(addzero,list(binmask)))       #  '00001101'  , addzero
        binlist.append(binmask)
    return binlist

binlist2hexlist = lambda binlist:  [ hex(int(b,2)).split('0x')[1].upper() for b in binlist ]

def ip2hexlist(ip):
    binlist = ip2binlist(ip)
    hex_list = [ hex(int(b,2)).split('0x')[1].upper() for b in binlist ]
    return hex_list

def binlist2ip(binlist):
    add_bin_prefix = lambda binstr: '0b' + binstr
    bin2int = lambda bstr: str( int(bstr,2))
    binlist = map(add_bin_prefix,binlist)
    ip = '.'.join( map(bin2int,binlist)  )
    return ip

def hexlist2ip(hexlist):
    add_hex_prefix = lambda xstr: '0x' + xstr
    hex2int  = lambda bstr: str( int(bstr,16))
    hexlist = map(add_hex_prefix,hexlist)
    ip = '.'.join( map(hex2int,hexlist)  )
    return ip

def hexlist2binlist(hexlist):
    ip = hexlist2ip(hexlist)
    return ip2binlist(ip)

def help():
    print 'help info...'
    sys.exit(1)

def main():
    ip = '192.168.141.111'
    net = 22
    print ip2network_address(ip, net)
    print cidr2mask(net)
    mask = cidr2mask(net)
    print mask2cidr(mask)
    # print mask2complement_bin_list(mask)
    # print ipmask2network_address(ip,mask)
    binlist = ip2binlist(ip)
    # print binlist
    hexlist =  binlist2hexlist(binlist)
    # print hexlist2binlist(hexlist)
    '''
    # cmd
    args = sys.argv
    net = args[1].split('/')

    if len(net) == 1 or net[1]=='':   # assume it's a mask
        net = net[0]
        print mask2int(net)
    else:                             # in form like 192.168.1.2/24
        net,mask = net
        print subnet_correct(net,mask)
    '''
if __name__ == '__main__':
    main()
