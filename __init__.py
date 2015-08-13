import os
from utilities import ConfigUtilities

SUPPORTED_CLOUD_TYPES = ["amazon", "openstack", "azure"]

def get_ext_cloud(cloud_type, *args, **kwargs):

	if cloud_type.lower() not in SUPPORTED_CLOUD_TYPES:
		msg = "cloud type:" + cloud_type + " not supported"
		raise Exception(msg)	

	if cloud_type.lower() == "openstack":

		from OpenStack.OpenStack import OpenStackcls
        	cloud_obj = OpenStackcls( **kwargs)
		
		return cloud_obj

	if cloud_type.lower()  == "amazon":
		if kwargs.has_key('username'):
			username = kwargs['username']

		if kwargs.has_key('password'):
			password = kwargs['password']

		if kwargs.has_key('region_name'):
			region_name = kwargs['region_name']
		else:
			region_name = 'us-east-1'

		from AWS.AWS import AWScls
		cloud_obj =  AWScls(username=username, password=password, region_name=region_name)		 
		return cloud_obj

	if cloud_type.lower() == "azure":
		from Azure.Azure import Azurecls
		cloud_obj = Azurecls(**kwargs)
		
		return cloud_obj
