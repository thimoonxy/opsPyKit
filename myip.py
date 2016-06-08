#!/usr/bin/env python
#encoding=utf-8
# Author: Simon Xie(Simon)
# E-mail: thimoon@sina.com
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
import re,urllib2
# print re.search('\d+\.\d+\.\d+\.\d+',urllib2.urlopen('http://www.whereismyip.com').read()).group()
content = urllib2.urlopen('http://www.myip.cn').readlines()
for each in content:
    if 'g_sites = ' in each:
        print  re.search('\d+\.\d+\.\d+\.\d+', each).group()
    if 'map_city.php' in each or 'o.src =' in each:
        """
        o.src = "http://www.myip.cn/map_city.php?ip=124.193.167.1&host=124.193.167.1&latitude=39.9289&longitude=116.3883&city=北京&location=北京市 电信通";
        """
        if 'SHELL' in os.environ.keys():
            print re.search('location=(.*)\".*', each).groups()[0]
        else:
            print re.search('location=(.*)\".*', each.decode('utf-8').encode(sys.getfilesystemencoding())).groups()[0]
