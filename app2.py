import httplib2
import json
from collections import OrderedDict

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

####################### Get Network Topology #########################

def topology():
	url = "http://localhost:8181/restconf/operational/network-topology:network-topology"
	#print url

	print
	resp, content = h.request(url, "GET")
	portStats = json.loads(content)

	topology = portStats['network-topology']['topology'][0]
	print "Topology ID - ", topology['topology-id']
	print
	print "Nodes present in the topology:"

	for i in range(len(topology['node'])):
		print "Node ID - ", topology['node'][i]['node-id']
		i += 1

	print
	print "Links connecting the nodes:"

	for i in range(len(topology['link'])):
		print "Link ID - ", topology['link'][i]['link-id']
		i += 1

####################### Get Port Statistics ###########################

def portStats():
	switch = raw_input("Enter the Switch Number: ")
	port = raw_input("Enter the port number wrt the switch given above: ")
	url1 = 'http://127.0.0.1:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:'
	url2 =  '/node-connector/openflow:'
	url = url1+switch+url2+switch+':'+port
	#print url

	print
	resp, content = h.request(url, "GET")
	portStats = json.loads(content)
	
	stats1 = portStats['node-connector'][0]
	stats2 = portStats['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']
	stats3 = portStats['node-connector'][0]['address-tracker:addresses'][0]


	if portStats:
		print "Node connector - ", stats1['id']
	
		print "Flow-node-name - ", stats1['flow-node-inventory:name']

		print "Flow-node-speed - ", stats1['flow-node-inventory:current-speed']

		print "Link feature - ", stats1['flow-node-inventory:current-feature']

		print "Bytes received - ", stats2['bytes']['received']

		print "Bytes transmitted - ", stats2['bytes']['transmitted']

		print "Packets received - ", stats2['packets']['received']

		print "Packets transmitted - ", stats2['packets']['transmitted']
	
		print
		print "Link State: ", json.dumps(stats1['flow-node-inventory:state'])
		print

	else:
		print "No data found"
		print
########################## SNMP-GET ##################################

def snmpGET():
	ip = raw_input("Please enter the IP address: ")
	oid = raw_input("Please enter the OID: ")
	get = raw_input("Please enter the get-type: ")
	community = raw_input("Please enter the community: ")

	url = 'http://127.0.0.1:8181/restconf/operations/snmp:snmp-get'
	Param = {
		    "input":
		            {
		                "ip-address": str(ip),
		                "oid" : str(oid),
		                "get-type" : get,
		                "community" : community
	    }			
	}
	 
	resp, content = h.request(
	    uri = url,
	    method = 'POST',
	    headers={'Content-Type':'application/json'},
	    body=json.dumps(Param)
	    )
	 
	print
	try:
		Info = json.loads(content)
		for key in Info:
			if key == 'errors':
				print "Invalid data provided"
				print
				break
			else:	
				count = 0
				if Info['output']: 	
					count = len(Info['output']['results'])	
					for i in range(count):
			    			print 'OID\t\t\t\t\t\tValue'
						print Info['output']['results'][i]['oid'],'\t\t\t',Info['output']['results'][i]['value']
						
				else:
					print 'No output for the OID!'
					print
	except ValueError as err:
		print "ERROR: ", err

####################### SYSTEM STATUS #############################################

def sysStatus():
	url = 'http://127.0.0.1:8181/restconf/operations/snmp:snmp-get'

	system = [('System Description', '1.3.6.1.2.1.1.1.0'),
		('Local Time', '1.3.6.1.4.1.2021.100.4.0'),
		('System Uptime', '1.3.6.1.2.1.1.3.0')]

	CPU = [('1-minute Load average', '1.3.6.1.4.1.2021.10.1.3.1'),
		('5-minute Load average', '1.3.6.1.4.1.2021.10.1.3.2'),
		 ('15-minute Load average', '1.3.6.1.4.1.2021.10.1.3.3')]

	memory = [('Total', '1.3.6.1.4.1.2021.4.5.0'),
		('Available', '1.3.6.1.4.1.2021.4.6.0'),
		('Buffered', '1.3.6.1.4.1.2021.4.14.0'),
		('Cached', '1.3.6.1.4.1.2021.4.15.0')]

	disk = [('Path where the disk is mounted', '1.3.6.1.4.1.2021.9.1.2.1'),
		('Path of the device for the partition', '1.3.6.1.4.1.2021.9.1.3.1'),
		('Total size of the disk/partion (kBytes)', '1.3.6.1.4.1.2021.9.1.6.1'),
		('Available space on the disk', '1.3.6.1.4.1.2021.9.1.7.1'),
		('Used space on the disk', '1.3.6.1.4.1.2021.9.1.8.1'),
		('% space used on disk', '1.3.6.1.4.1.2021.9.1.9.1')]

	system = OrderedDict(system)
	memory = OrderedDict(memory)
	disk = OrderedDict(disk)
	CPU = OrderedDict(CPU)

	print
	print "######################## System Info ###########################"
	for oid in system:
		Param = {
			    "input":
				    {
				        "ip-address": "127.0.0.1",
				        "oid" : system[oid],
				        "get-type" : "GET",
				        "community" : "public"
		    }
		}
	 
		resp, content = h.request(
		    uri = url,
		    method = 'POST',
		    headers={'Content-Type':'application/json'},
		    body=json.dumps(Param)
		    )
	 
		Info = json.loads(content)
		print
		count = len(Info['output']['results'])	
		for i in range(count):
			print  oid + " - ", Info['output']['results'][i]['value']
	###################################################################################
	print
	print
	print "############################ CPU Info ##########################"
	for oid in CPU:
		Param = {
			    "input":
				    {
				        "ip-address": "127.0.0.1",
				        "oid" : CPU[oid],
				        "get-type" : "GET",
				        "community" : "public"
		    }
		}
	 
		resp, content = h.request(
		    uri = url,
		    method = 'POST',
		    headers={'Content-Type':'application/json'},
		    body=json.dumps(Param)
		    )
	 
		Info = json.loads(content)
		print
		count = len(Info['output']['results'])	
		for i in range(count):
			print  oid + " - ", Info['output']['results'][i]['value']
	#################################################################################
	print
	print
	print "########################### Memory Info (kB) #####################"
	for oid in memory: 
		Param = {
			    "input":
				    {
				        "ip-address": "127.0.0.1",
				        "oid" : memory[oid],
				        "get-type" : "GET",
				        "community" : "public"
		    }
		}
	 
		resp, content = h.request(
		    uri = url,
		    method = 'POST',
		    headers={'Content-Type':'application/json'},
		    body=json.dumps(Param)
		    )
	 
		Info = json.loads(content)
		print
		count = len(Info['output']['results'])	
		for i in range(count):
			print  oid + " - ", Info['output']['results'][i]['value']

	##################################################################################
	print
	print
	print "############################ Disk Info (kB) #######################"
	for oid in disk: 
		Param = {
			    "input":
				    {
				        "ip-address": "127.0.0.1",
				        "oid" : disk[oid],
				        "get-type" : "GET",
				        "community" : "public"
		    }
		}
	 
		resp, content = h.request(
		    uri = url,
		    method = 'POST',
		    headers={'Content-Type':'application/json'},
		    body=json.dumps(Param)
		    )
	 
		Info = json.loads(content)
		print
		count = len(Info['output']['results'])	
		for i in range(count):
			print  oid + " - ", Info['output']['results'][i]['value']
	print '##############################################################################'
	

#####################################################################

def Exit():
	print "Exiting..!!"
	sys.exit()


#Added swicth case Input type

options = {     1: topology,
		2: portStats,
		3: snmpGET,
		4: sysStatus,
		5: Exit,
}

print "Please select operation : \n1. Topology \n2. Port Statistics \n3. SNMPGET \n4. System Status \n5. Exit \n" 
num=input("Enter here: ")
options[num]()

