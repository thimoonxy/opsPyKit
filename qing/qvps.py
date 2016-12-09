#!/bin/env python
# -*- encoding: utf-8 -*-
__author__ = 'Simon Xie'
__email__ = 'xieyin@pwrd.com'

import sys,os,json,time
reload(sys)
sys.setdefaultencoding('utf-8')

'''
Doc:
https://docs.qingcloud.com/cli/index.html
'''

def check_online_server_id():
	server_id=""
	desc_server_cmd="qingcloud.cmd iaas describe-instances"
	output=os.popen(desc_server_cmd)
	content=json.loads(output.read())
	# print content.keys()
	all_set = content['instance_set']
	for x in all_set:
	    if x[u'status'] in ['running','stopped']:
	        server_id =  x['instance_id']
	return server_id

def check_eip_id():
	eip_id=eip_ip=""
	desc_eip_cmd="qingcloud.cmd iaas describe-eips"
	output=os.popen(desc_eip_cmd)
	content=json.loads(output.read())
	all_set = content[u'eip_set']
	# print all_set[0]
	for x in all_set:
	    if x[u'status'] not in  ['ceased','terminated']:
	        eip_id =  x['eip_id']
	        eip_ip = x['eip_addr']	
	return eip_id, eip_ip

def destroy_all():
	server_id = check_online_server_id()
	eip_id, ip =check_eip_id()
	stop_cmd="qingcloud.cmd iaas stop-instances -i \"%s\"" %server_id
	terminate_cmd="qingcloud.cmd iaas terminate-instances -i %s" %server_id
	if server_id != '' :
		os.popen(stop_cmd)
		time.sleep(5)
		print "Stopped server %s." %server_id
		os.popen(terminate_cmd)
		time.sleep(5)
		print "Destroyed server %s." %server_id
	if check_online_server_id() != '':
		return destroy_all()
	else:
		release_ip_cmd="qingcloud.cmd iaas release-eips -e %s" %eip_id
		if eip_id != '' and server_id == '':
			os.popen(release_ip_cmd)
			print "Released eip %s." %eip_id
			sys.exit(0)
		elif eip_id != '' and server_id != '':
			return destroy_all()
		else:
			print 'All clear now.'
			sys.exit(0)

def apply_eip():
	cmd='qingcloud.cmd iaas allocate-eips -z ap1 -c 1 -b 4 -B "traffic"'
	output=os.popen(cmd)
	content=json.loads(output.read())
	eip_id=""
	try:
		eip_id=content["eips"][0]
	except KeyError:
		print "Failed to apply EIP."
		sys.exit(1)
	return eip_id	
		
def apply_server():
	cmd="qingcloud.cmd iaas run-instances -z ap1 -t small_b -c 1 -C 1 -M 1024 -l keypair -k kp-cocad8sr -m centos7x64d -n vxnet-0"	
	output=os.popen(cmd)
	content=json.loads(output.read())
	server_id=""
	server_id = content["instances"][0]
	return server_id

def binidng_ip(eip_id, server_id):
	cmd="qingcloud.cmd iaas associate-eip -z ap1 -e %s -i %s" %(eip_id, server_id)
	if check_online_server_id() != '':
		output=os.popen(cmd)
		content=json.loads(output.read())
		if content["ret_code"] == 0:
			return True
		else:
			return False
	else:
		return binidng_ip(eip_id, server_id)
def help():
	print """
Destroy or Create QingCloud VPS.
Actions: 
	kill : destroy_all resources (server and ip).
	new  : create a new VPS.
	"""	

def main():
	try:
		opt = sys.argv[1]
	except:
		help()
		sys.exit(1)
	if opt == 'kill':
		destroy_all()
	elif opt == 'new':
		eip_id, server_id = apply_eip() , apply_server()
		if binidng_ip(eip_id, server_id):
			eip_id, eip_ip = check_eip_id()
			print "Created %s" %eip_ip
		else:
			print "Failed to bind ip."
	else:
		help()
	
	

if __name__ == "__main__":
    main()