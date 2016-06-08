__author__ = 'simon'

import pythonwhois
import sys
try:
    ip = sys.argv[1]
except:
    ip = '202.106.0.20'
result = pythonwhois.net.get_whois_raw('%s'%ip,server='v4.whois.cymru.com')
print "Queried %s:\n" %ip
print result[0]