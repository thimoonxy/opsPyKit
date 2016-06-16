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

def ip2network_address(ip, cidr='32'):
    """
    This func also corrects wrong subnet, e.g.
    if found 10.69.231.70/29, it'll be corrected to 10.69.231.64/29.
    """
    ip = ip.split('.')
    netmask, bin_mask_list = cidr2mask(cidr)
    for x in range(len(ip)):
        # print ip[x], int(bin_mask_list[x], 2)
        ip[x] = int(ip[x]) & int(bin_mask_list[x], 2)
    if int(cidr) < 31:
        network_address = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3])
        first_avail_ip = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3]+1)
        avail_host_numbers = 2 ** (32 - int(cidr)) - 2
        complement_mask, complement_bin_list = mask_complement(netmask)
        broadcase_address = '.'.join([ str(ip[x]+int(complement_bin_list[x],2)) for x in range(4)])
        last_avail_ip_list = broadcase_address.split('.')[0:3]
        last_avail_ip_list.append( str( int(broadcase_address.split('.')[-1]) -1 ) )
        last_avail_ip = '.'.join(last_avail_ip_list)
    elif int(cidr) == 31:
        broadcase_address = network_address = None
        first_avail_ip = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3])
        last_avail_ip = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3]+1)
        avail_host_numbers = 2
    else:
        broadcase_address = network_address = None
        first_avail_ip = "%s.%s.%s.%s" % (ip[0], ip[1], ip[2], ip[3])
        last_avail_ip = first_avail_ip
        avail_host_numbers = 1
    return  avail_host_numbers, netmask, network_address, first_avail_ip,last_avail_ip, broadcase_address

def mask2cidr(mask='255.255.255.0'):
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

def cidr2mask(cidr='23'):
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
    bin_mask_list = net
    netmask = '.'.join([ str(int(net[x], 2)) for x in range(len(net)) ])
    return netmask, bin_mask_list

def mask_complement(mask='255.255.255.0'):
    cidr = mask2cidr(mask)
    netmask, bin_mask_list = cidr2mask(cidr)
    xcomplement_bin_list = [x.split('0b')[1] for x in bin_mask_list]
    anti = lambda x: (x == '1') and '0' or '1'
    bin2mask = lambda bstr: str( int(bstr,2))
    complement_bin_list = [  ''.join(map(anti,list(x))) for x in xcomplement_bin_list ]
    complement_bin_list = [ '0b'+x for x in complement_bin_list]
    complement_mask = '.'.join(map(bin2mask,complement_bin_list))
    return complement_mask, complement_bin_list


def help():
    print 'help info...'
    sys.exit(1)

def main():

    ip = '10.69.231.70'
    net = 29
    print ip2network_address(ip, net)
    print cidr2mask(net)
    print mask_complement(cidr2mask(net)[0])

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
