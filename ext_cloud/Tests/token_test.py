#!/usr/bin/python
from ext_cloud import get_ext_cloud

# cloud_obj =  get_ext_cloud("openstack",username='admin', password='C123', tenant_name='openstack', auth_url='http://10.233.52.56:5000/v2.0/', service_type='compute', region_name='regionOne')

cloud_obj = get_ext_cloud("openstack")
token  = cloud_obj.identity.create_token()
#token = cloud_obj.identity.OpenStackTokenCls()
import pdb
pdb.set_trace()
print token
