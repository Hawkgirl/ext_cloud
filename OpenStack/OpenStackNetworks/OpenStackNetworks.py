from ext_cloud.BaseCloud.BaseNetworks.BaseNetworks import BaseNetworkscls
from ext_cloud.OpenStack.OpenStackNetworks.OpenStackNetwork import OpenStackNetworkcls
from ext_cloud.OpenStack.OpenStackNetworks.OpenStackSubnet import OpenStackSubnetcls
from ext_cloud.OpenStack.OpenStackNetworks.OpenStackNIC import OpenStackNICcls
from ext_cloud.OpenStack.OpenStackNetworks.OpenStackFloatingIp import OpenStackFloatingIpcls
from ext_cloud.OpenStack.OpenStackNetworks.OpenStackRouter import OpenStackRoutercls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls


class OpenStackNetworkscls(OpenStackBaseCloudcls, BaseNetworkscls):
    def __init__(self, *args, **kwargs):
        super(OpenStackNetworkscls, self).__init__(credentials=kwargs)

    @property
    def Childrens(self):
        return self.list_networks() + self.list_routers() + self.list_nics(
        ) + self.list_floating_ips() + self.list_subnets()

    def list_metrics(self):
        metrics = []
        from ext_cloud.BaseCloud.BaseResources.BaseMetrics import BaseMetricscls
        metrics.append(BaseMetricscls('openstack.networks.count', len(
            self.list_networks())))
        metrics.append(BaseMetricscls('openstack.networks.subnets.count', len(
            self.list_subnets())))
        metrics.append(BaseMetricscls('openstack.networks.free_floating_ips',
                                      self.free_floating_ips))
        metrics.append(BaseMetricscls('openstack.networks.used_floating_ips',
                                      self.used_floating_ips))
        metrics.append(BaseMetricscls('openstack.networks.total_floating_ips',
                                      self.total_floating_ips))
        return metrics

    def get_network_by_id(self, network_id):
        return [OpenStackNetworkcls(openstack_network,
                                    credentials=self._credentials)
                for openstack_network in self._NeutronClient.list_networks(
                    id=network_id)['networks']]

    def get_networks_by_name(self, network_name):
        return [OpenStackNetworkcls(openstack_network,
                                    credentials=self._credentials)
                for openstack_network in self._NeutronClient.list_networks(
                    name=network_name)['networks']]

    def get_networks_by_tenant_id(self, tenant_id):
        return [OpenStackNetworkcls(openstack_network,
                                    credentials=self._credentials)
                for openstack_network in self._NeutronClient.list_networks(
                    tenant_id=tenant_id)['networks']]

    def get_networks_by_tag(self, tag_name, tag_value):
        pass

    def list_networks(self):
        return [OpenStackNetworkcls(openstack_network,
                                    credentials=self._credentials)
                for openstack_network in self._NeutronClient.list_networks()[
                    'networks']]

    def list_external_networks(self):
        return [network
                for network in self.list_networks()
                if network.is_external_network]

    def create_network(self, name=None, cidr_block=None):
        params = {'network': {'name': name}}
        openstack_network_dic = self._NeutronClient.create_network(params)
        openstack_network = openstack_network_dic['network']
        network = OpenStackNetworkcls(openstack_network,
                                      credentials=self._credentials)
        return network
    # ----------------- Subnet operations ------------------------- #

    def list_subnets(self):
        return [OpenStackSubnetcls(openstack_subnet,
                                   credentials=self._credentials)
                for openstack_subnet in self._NeutronClient.list_subnets()[
                    'subnets']]

    def get_subnets_by_tenant_id(self, tenant_id):
        return [OpenStackSubnetcls(openstack_subnet,
                                   credentials=self._credentials)
                for openstack_subnet in self._NeutronClient.list_subnets(
                    tenant_id=tenant_id)['subnets']]

    def list_external_subnets(self):
        return [subnet
                for network in self.list_external_networks()
                for subnet in network.list_subnets()]

    def get_subnet_by_id(self, subnet_id):
        subnets = self.list_subnets()
        for subnet in subnets:
            if subnet.id == subnet_id:
                return subnet
        return None

    def get_subnets_by_name(self, subnet_name):
        pass

    def get_subnets_by_tag(self, tag_name, tag_value):
        pass

    # ----------------- Nic operations ------------------------- #
    def list_nics(self):
        return [OpenStackNICcls(openstack_nic,
                                credentials=self._credentials)
                for openstack_nic in self._NeutronClient.list_ports()['ports']]

    # ----------------- Router operations ------------------------- #
    def list_routers(self):
        return [OpenStackRoutercls(router,
                                   credentials=self._credentials)
                for router in self._NeutronClient.list_routers()['routers']]

    # ----------------- Floating ip operations ------------------------- #
    def list_floating_ips(self):
        return [OpenStackFloatingIpcls(openstack_floating_ip,
                                       credentials=self._credentials)
                for openstack_floating_ip in
                self._NeutronClient.list_floatingips()['floatingips']]

    def list_floating_ips_by_tenant_id(self, tenant_id):
        return [
            OpenStackFloatingIpcls(openstack_floating_ip,
                                   credentials=self._credentials)
            for openstack_floating_ip in self._NeutronClient.list_floatingips(
                tenant_id=tenant_id)['floatingips']
        ]

    @property
    def total_floating_ips(self):
        return sum([subnet.count_total_ips
                    for subnet in self.list_external_subnets()])

    @property
    def used_floating_ips(self):
        return sum([1
                    for floating_ip in self.list_floating_ips()
                    if floating_ip.state == 'up'])

    @property
    def free_floating_ips(self):
        return self.total_floating_ips - self.used_floating_ips
