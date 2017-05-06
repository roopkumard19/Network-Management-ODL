import httplib2
import json
import sys
import os
import crypt,getpass
from collections import OrderedDict
import time

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

l1 = []
l2 = []
l3 = []
n1 = []
n2 = []
n3 = []
print "Monitoring OpenFlow Switches.."

def topo():
	url = "http://localhost:8181/restconf/operational/network-topology:network-topology"
	resp, content = h.request(url, "GET")
	portStats = json.loads(content)
	topology = portStats['network-topology']['topology'][0]
	return topology


def checkTopo():
	global l1
	t1 = topo()

	for i in range(len(t1['link'])):
		l1.append(t1['link'][i]['link-id'])
		i += 1

	n = len(t1['node'])

	l = len(t1['link'])
	

	return n,l




def trackLinks():	
	global l1,l2,l3
	t3 = topo()

	for i in range(len(t3['link'])):
		l2.append(json.dumps(t3['link'][i]['link-id']))
		i += 1
	
	#print l2
	#print set(l1)
	l3 = list(set(l1) - set(l2))
	return	l3

def trackNodes():	
	global n2,n1
	t3 = topo()

	for i in range(len(t3['node'])):
		n2.append(json.dumps(t3['node'][i]['node-id']))
		i += 1
	
	#print n2
	#print set(n1)
	n3 = list(set(n1) - set(n2))
	return	n3		


def change():
	while(1):	
		node1,link1 = checkTopo()
	
		time.sleep(2)

		node2,link2 = checkTopo()
	
		if(node2 > node1):
			print
			print "New nodes added - \n"
			print trackNodes()
			print
		elif(node2 < node1):
			print "Nodes deleted - \n"
			print trackNodes()		
			print

		if(link2 > link1):
			print "Links up - \n"
			print trackLinks()
			print

		elif(node2 < node1):
			print "Links down - \n"
			print trackLinks()
			print
			

change()
