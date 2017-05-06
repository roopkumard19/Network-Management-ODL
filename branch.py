import httplib2
import json
import sys
import os
import crypt,getpass
from collections import OrderedDict
import time

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

total_links = set()
alive_links = set()
return_links_up = set()
return_links_down = set()
total_nodes = set()
alive_nodes = set()
return_nodes_up = set()
return_nodes_down = set()

print "Monitoring OpenFlow Switches.."

def topo():
	url = "http://localhost:8181/restconf/operational/network-topology:network-topology"
	resp, content = h.request(url, "GET")
	portStats = json.loads(content)
	topology = portStats['network-topology']['topology'][0]
	return topology

def total():
	global total_links, total_nodes
	t1 = topo()

	for i in range(len(t1['link'])):
		total_links.add(t1['link'][i]['link-id'])
		i += 1

	for i in range(len(t1['node'])):
		total_nodes.add(t1['node'][i]['node-id'])
		i += 1
	return

def checkTopo():
	t2 = topo()

	no_nodes = len(t2['node'])

	no_links = len(t2['link'])
	

	return no_nodes,no_links



def trackLinksUp():	
	global total_links,alive_links,return_links_up
	t3 = topo()

	for i in range(len(t3['link'])):
		alive_links.add(t3['link'][i]['link-id'])
		i += 1
	
	#print "total - ", total_links
	#print "alive - ", alive_links
	#print
	return_links_up = list(alive_links - total_nodes)
	total_links = alive_links
	return	return_links_up


def trackLinksDown():	
	global total_links,alive_links,return_links_down
	t3 = topo()

	for i in range(len(t3['link'])):
		alive_links.add(t3['link'][i]['link-id'])
		i += 1
	
	#print "alive - ", alive_links
	#print
	return_links_down = list(total_links - alive_links)
	total_links = alive_links
	print "total - ", total_links
	print
	return	return_links_down


def trackNodesUp():	
	global total_nodes,alive_nodes,return_nodes_up
	t3 = topo()

	for i in range(len(t3['node'])):
		alive_nodes.add(t3['node'][i]['node-id'])
		i += 1
	
	#print "total - ", total_nodes
	#print "alive - ", alive_nodes
	#print
	return_nodes_up = list(alive_nodes - total_nodes)
	total_nodes = alive_nodes
	return	return_nodes_up


def trackNodesDown():	
	global total_nodes,alive_nodes,return_nodes_down
	t3 = topo()

	for i in range(len(t3['node'])):
		alive_nodes.add(t3['node'][i]['node-id'])
		i += 1
	
	#print "total - ", total_nodes
	#print "alive - ", alive_nodes
	#print
	return_nodes_down = list(total_nodes - alive_nodes)
	total_nodes = alive_nodes
	return	return_nodes_down		


def change():
	total()
	while(1):	
		node1,link1 = checkTopo()
	
		time.sleep(2)

		node2,link2 = checkTopo()
	
		if(node2 > node1):
			print
			print "New nodes added - \n"
			print trackNodesUp()
			print
		elif(node2 < node1):
			print "Nodes deleted - \n"
			print trackNodesDown()		
			print

		if(link2 > link1):
			print "Links up - \n"
			print trackLinksUp()
			print

		elif(node2 < node1):
			print "Links down - \n"
			print trackLinksDown()
			print
			

change()
