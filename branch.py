import httplib2
import json
import sys
import os
import crypt,getpass
from collections import OrderedDict
import time

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

s1 = []
s2 = []
print "Monitoring OpenFlow Switches.."

def topo():
	url = "http://localhost:8181/restconf/operational/network-topology:network-topology"
	resp, content = h.request(url, "GET")
	portStats = json.loads(content)
	topology = json.dumps(portStats['network-topology']['topology'][0])
	return topology


def checkTopo():
	global s1
	t1 = topo()

	for i in range(len(t1['link'])):
		s1.append(t1['link'][i]['link-id'])
		i += 1

	n1 = len(t1['node'])

	l1 = len(t1['link'])
	

	return n1,l1




def trackLinks():	
	global s2,s1
	t3 = topo()

	for i in range(len(t3['link'])):
		s2.append(t3['link'][i]['link-id'])
		i += 1
	
	print s2
	print set(s1)
	s3 = set(s1) - set(s2)
	return	s3
		


def change():
	while(1):
		print	
		m1,n1 = checkTopo()
	
		time.sleep(2)

		m2,n2 = checkTopo()
	
		if(m2 > m1):
			print "link added"
		elif(m2 < m1):
			print "link deleted....", trackLinks()
			

change()
