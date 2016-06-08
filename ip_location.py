#!/usr/bin/env python
# encoding=utf-8
# Author: Simon Xie(Simon)
# E-mail: thimoon@sina.com

import sys, urllib2, json

ip_list = []

try:
    if sys.argv[1] == '-s':
        ip_list = sys.stdin.readlines()
    else:
        ip_list.append(sys.argv[1])
except:
    print '''NOTE:
1. single ip as argv:
	ip_location.py 8.8.8.8
2. stdin a list of IPs with -s parm:
	cat list| ip_location.py -s
	\n'''
    if len(ip_list) == 0:
        sys.exit(1)
print "query".ljust(20) + "city".ljust(20) + "country".ljust(20) + "isp".ljust(40) + "regionName".ljust(
    20) + "timezone".ljust(20)

if len(ip_list) == 1:
    ip = ip_list[0]
    #url = "http://ip-api.com/json/%s" % ip.split('\n')[0]
    url = "http://81.4.121.206/json/%s" % ip.split('\n')[0]
    """
	Usage limits

	Our system will automatically ban any IP addresses doing over 250 requests per minute. To unban your IP go to http://outgoing.ip-api.com/docs/api:batch.
	"""
    request = urllib2.Request(url)
    request.add_header('Host','ip-api.com')
    # try:
    respond = urllib2.urlopen(request, data=None, timeout=len(ip_list) * 0.6 + 5)
    # except:
    # print ip.split('\n')[0]+'Unknown'
    # continue
    content = json.loads(respond.read())
    if content['status'] != 'fail':
        # print content
        """
		{u'as': u'AS4134 Chinanet',
		 u'city': u'Xiamen',
		 u'country': u'China',
		 u'countryCode': u'CN',
		 u'isp': u'China Telecom',
		 u'lat': 24.4798,
		 u'lon': 118.0819,
		 u'org': u'China Telecom',
		 u'query': u'110.84.0.129',
		 u'region': u'35',
		 u'regionName': u'Fujian',
		 u'status': u'success',
		 u'timezone': u'Asia/Shanghai',
		 u'zip': u''}
		"""
        city = content['city']
        country = content['country']
        isp = content['isp']
        timezone = content['timezone']
        regionName = content['regionName']
        query = content['query']
        print query.ljust(20) + city.ljust(20) + country.ljust(20) + isp.ljust(40) + regionName.ljust(
            20) + timezone.ljust(20)
    else:
        print ip.split('\n')[0].ljust(20) + 'Unknown'
else:
    json_list = []
    # print ip_list
    for ip in ip_list:
        json_list.append({'query': ip})
    # data = urllib.urlencode(json_list)
    url = "http://81.4.121.206/batch"
    request = urllib2.Request(url)
    request.add_header('Host','ip-api.com')
    for ip in ip_list:
        json_list.append({'query': ip.strip()})
        # data=str({'query': ip.strip()})
    data = json.dumps(json_list)
    # print (data)
    request.add_data(data)
    respond = urllib2.urlopen(request,timeout=len(ip_list) * 0.6 + 5)
    content_list = json.loads(respond.read())
    for content in content_list:
        if content['status'] != 'fail':
            city = content['city']
            country = content['country']
            isp = content['isp']
            timezone = content['timezone']
            regionName = content['regionName']
            query = content['query']
            print query.ljust(20) + city.ljust(20) + country.ljust(20) + isp.ljust(40) + regionName.ljust(
                20) + timezone.ljust(20)
        else:
            pass