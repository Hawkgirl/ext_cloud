from os.path import dirname
from sys import path

basepath = dirname(__file__)
basepath = basepath + "../../"
path.append(basepath)

from ext_cloud import get_ext_cloud

#cloud_obj =  get_ext_cloud("openstack",username='admin', password='Cisco123', tenant_name='openstack', auth_url='http://10.233.52.56:5000/v2.0/', service_type='compute', region_name='regionOne')
cloud_obj = get_ext_cloud("amazon", username='AKIAJ2WDTBHN33WQPE7A',
                          password='ofcBq4MOLoz46hdEvRpYXN7eY/xXvSoh/bur5Mgx', region_name='us-east-1')

template = cloud_obj.templates.is_valid(
    file='/root/ext_cloud/Tests/Templates/AmazonBaseTemplate.template')
print template
