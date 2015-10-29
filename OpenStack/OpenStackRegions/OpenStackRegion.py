from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls
from BaseCloud.BaseRegions.BaseRegion import BaseRegioncls

class OpenStackRegioncls(OpenStackBaseCloudcls, BaseRegioncls):
	__novaclient = None
	def __init__(self, *args, **kwargs):
		self._credentials = kwargs['credentials']
		super(OpenStackRegioncls, self).__init__(id=args[0], name=args[0], credentials=kwargs['credentials'])

	@property
        def __NovaClient(self):
                return self.__novaclient

        @__NovaClient.getter
        def __NovaClient(self):
                if self.__novaclient is None:
                        from OpenStack.utils.OpenStackClients import OpenStackClientsCls
                        self.__novaclient = OpenStackClientsCls().get_nova_client(self._credentials)
                return self.__novaclient

	def list_zones(self): 
		zones = self.__NovaClient.availability_zones.list()
		openstack_zones = []
		for zone in zones:
                        from OpenStack.OpenStackRegions.OpenStackZone import OpenStackZonecls
                        zone = OpenStackZonecls(zone, credentials=self._credentials)
                        openstack_zones.append(zone)
                return openstack_zones

