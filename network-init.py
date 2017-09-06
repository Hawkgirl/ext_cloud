#!/usr/bin/python
from ext_cloud import get_ext_cloud

CIDR_BLOCK='10.14.0.0/24'
TENANT_NAME='demo'
EXT_NET_ID='f70e083c-fb1f-45e6-a4bc-03e7f6df3cda'



cloud_obj =  get_ext_cloud("openstack")
print "Creating network"
network = cloud_obj.networks.create_network(name=TENANT_NAME+'-net')
print "Creating subnet"
subnet = network.create_subnet(name=TENANT_NAME+'-subnet', cidr_block=CIDR_BLOCK)
print "Creating router"
router = cloud_obj.networks.create_router(name=TENANT_NAME+'-router')
print "Attach router to subnet"
router.attach_subnet(subnet.id)
print "Attach gateway to router"
router.attach_gateway(EXT_NET_ID)
#print router
