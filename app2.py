import httplib2
import json

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

# Uncommented below line, use it on your needs.. #swapnasheel
#operation = raw_input("Enter The Operation index: ")

####################### Get Network Topology #########################

def topology():
	url = "http://localhost:8181/restconf/operational/network-topology:network-topology"
	print url

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

####################### Get Port Statistics #########################

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
	
	stats1 = portStats['node-connector'][0]['id']
	stats2 = portStats['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']
	stats3 = portStats['node-connector'][0]['address-tracker:addresses'][0]

	if portStats:
		print "Node connector - ", stats1

		print "Bytes received - ", stats2['bytes']['received']

		print "Bytes transmitted - ", stats2['bytes']['transmitted']

		print "Packets received - ", stats2['packets']['received']

		print "Packets transmitted - ", stats2['packets']['transmitted']

		print "MAC address of the host connected thru the node-connector: - ", stats3['mac']

		print "IP address of the host connected thru the node-connector: - ", stats3['ip']
		print

	else:
		print "No data found"
		print
########################## SNMP-GET ################################

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
						print Info['output']['results'][i]['oid'],'\t\t',Info['output']['results'][i]['value']
						print
				else:
					print 'No output for the OID!'
					print
	except ValueError as err:
		print "ERROR: ", err
#########################################################

#Added swicth case Input type

options = {     1: topology,
		2: portStats,
		3: snmpGET,
		4: exit,
}

print "Please select operation : \n1. Topo \n2. PortStats \n3. SNMPGET \n4. Exit \n \n" 
num=input()
options[num]()



