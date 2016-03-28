#!/usr/bin/python
from ext_cloud import get_ext_cloud

#cloud_obj =  get_ext_cloud("openstack",username='admin', password='Cisco123', tenant_name='openstack', auth_url='http://10.233.52.56:5000/v2.0/', service_type='compute', region_name='regionOne')
cloud_obj = get_ext_cloud("amazon", username='AKIA2ZK6SOG6EJQ',
                          password='2Z0Yzqr6JwICnEffklbVbOM+t/g+6ePCyRo', region_name='us-east-1')

#cloud_obj =  get_ext_cloud("azure", subscription_id = 'cd42b929-8458-4acd-b599-398cd51f4c6c', certificate_path = './Tests/Azure/mycert.pem')
instances = cloud_obj.compute.list_instances()
for instance in instances:
    print instance
