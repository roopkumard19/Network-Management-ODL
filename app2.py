import httplib2
import json

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

operation = raw_input("Enter The Operation index: ")

#######################Get Network Topology#########################

def topo():
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

#######################Get Statistics#########################

def portStat():
	switch = raw_input("Enter the Switch Number: ")
	port = raw_input("Enter the port number wrt the switch given above: ")
	url1 = 'http://127.0.0.1:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:'
	url2 =  '/node-connector/openflow:'
	url = url1+switch+url2+switch+':'+port
	#print url

	print
	resp, content = h.request(url, "GET")
	portStats = json.loads(content)

	if portStats:
		print "Node connector - ", portStats['node-connector'][0]['id']

		print "Bytes received - ", portStats['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['received']

		print "Bytes transmitted - ", portStats['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['transmitted']

		print "Packets received - ", portStats['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['packets']['received']

		print "Packets transmitted - ", portStats['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['packets']['transmitted']

		print "MAC address of the host connected thru the node-connector: - ", portStats['node-connector'][0]['address-tracker:addresses'][0]['mac']

		print "IP address of the host connected thru the node-connector: - ", portStats['node-connector'][0]['address-tracker:addresses'][0]['ip']

	else:
		print "No data found"

######################################################


