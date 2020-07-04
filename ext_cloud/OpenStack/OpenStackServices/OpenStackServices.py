from ext_cloud.BaseCloud.BaseServices.BaseServices import BaseServicescls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls


class OpenStackServicescls(OpenStackBaseCloudcls, BaseServicescls):

    def __init__(self, **kwargs):
        super(OpenStackServicescls, self).__init__(credentials=kwargs)

    @property
    def Childrens(self):
        return []

    def list_metrics_all(self, dic):
        self.__list_metrics(self.list_compute_services(), dic)
        self.__list_metrics(self.list_network_services(), dic)
        self.__list_metrics(self.list_volume_services(), dic)

    def __list_metrics(self, services, dic):
        if len(services) is 0:
            return []
        metric_str = 'openstack.' + services[0].group + '.services.'
        enabled = disabled = up = down = 0
        for service in services:

            if service.state == 'up':
                up += 1
            elif service.state == 'down':
                down += 1
            else:
                pass

            if service.status == 'enabled':
                enabled += 1
            elif service.status == 'disabled':
                disabled += 1
            else:
                pass
        dic[metric_str + 'up'] = up
        dic[metric_str + 'down'] = down
        dic[metric_str + 'enabled'] = enabled
        dic[metric_str + 'disabled'] = disabled


    def list_services(self):
        services = []
        services += self.list_compute_services()
        services += self.list_network_services()
        services += self.list_volume_services()
        return services

    def list_compute_services(self):
        services = []
        nova_services = self._Clients.nova.services.list()
        for nova_service in nova_services:
            kwargs = {}
            kwargs['id'] = nova_service.id
            kwargs['name'] = nova_service.binary
            kwargs['group'] = 'nova'
            kwargs['state'] = nova_service.state
            kwargs['status'] = nova_service.status
            kwargs['host'] = nova_service.host
            from ext_cloud.OpenStack.OpenStackServices.OpenStackService import OpenStackServicecls
            service = OpenStackServicecls(**kwargs)
            services.append(service)

        return services

    def list_network_services(self):
        services = []
        neutron_services = self._Clients.neutron.list_agents()['agents']
        for service in neutron_services:
            kwargs = {}
            kwargs['id'] = service['id']
            kwargs['name'] = service['binary']
            kwargs['group'] = 'network'
            kwargs['state'] = 'up' if service['alive'] is True else 'down'
            kwargs['status'] = 'enabled' if service[
                'admin_state_up'] is True else 'disabled'
            kwargs['host'] = service['host']
            from ext_cloud.OpenStack.OpenStackServices.OpenStackService import OpenStackServicecls
            service = OpenStackServicecls(**kwargs)
            services.append(service)

        return services

    def list_volume_services(self):
        services = []
        volume_services = self._Clients.cinder.services.list()
        for service in volume_services:
            kwargs = {}
            kwargs['id'] = service.binary
            kwargs['name'] = service.binary
            kwargs['group'] = 'volumes'
            kwargs['state'] = service.state
            kwargs['status'] = service.status
            kwargs['host'] = service.host
            from ext_cloud.OpenStack.OpenStackServices.OpenStackService import OpenStackServicecls
            service = OpenStackServicecls(**kwargs)
            services.append(service)

        return services
