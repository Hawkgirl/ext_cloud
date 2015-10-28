from ext_cloud import get_ext_cloud

cloud_obj =  get_ext_cloud("openstack",username='admin', password='G3rm4n1cus', tenant_name='admin', auth_url='http://192.168.3.130:5000/v2.0/')

metrics = cloud_obj.stats.get_metrics()
for metric in metrics:
	print metric.name,'\t',metric.value,'\t',metric.timestamp
