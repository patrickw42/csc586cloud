import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.igext as IG

pc = portal.Context()
request = pc.makeRequestRSpec()

tourDescription = \
"""
This profile provides a two-node set for assignment 2. One node will be the LDAP/NFS server (observer) with a public IP,
one node will be the NFSclient/Apache server without a public IP (webserver).
 
"""
#
# Setup the Tour info with the above description and instructions.
#  
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
request.addTour(tour)
prefixForIP = "192.168.1."
link = request.LAN("lan")

for i in range(2):
  if i == 0:
    node = request.XenVM("observer")          #this node runs the NFS server without public IP    
    node.routable_control_ip = "false"         
  elif i == 1:
    node = request.XenVM("webserver")         # this node runs the Apache server with a public IP
    node.routable_control_ip = "true"
  
  node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD"
  iface = node.addInterface("if" + str(i))
  iface.component_id = "eth1"
  iface.addAddress(pg.IPv4Address(prefixForIP + str(i + 1), "255.255.255.0"))
  link.addInterface(iface)  
# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
