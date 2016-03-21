from azure.servicemanagement import ServiceManagementService
from BaseCloud.BaseRegions.BaseRegions import BaseRegionscls
from Azure.AzureBaseCloud import AzureBaseCloudcls


class AzureRegionscls(AzureBaseCloudcls, BaseRegionscls):
    __sms = None

    def __init__(self, *args, **kwargs):
        self._credentials = kwargs['credentials']

    @property
    def __SMS(self):
        return self.__sms

    @__SMS.getter
    def __SMS(self):
        if self.__sms is None:
            self.__sms = ServiceManagementService(
                self._credentials['subscription_id'], self._credentials['certificate_path'])
        return self.__sms

    def list_regions(self):
        from Azure.AzureRegions.AzureRegion import AzureRegioncls
        azure_locations = self.__SMS.list_locations()
        regions = []
        for azure_location in azure_locations:
            location = AzureRegioncls(
                azure_location, credentials=self._credentials)
            regions.append(location)

        return regions

    def get_region_by_id(self, instance_id): pass

    def get_region_by_name(self, instance_name): pass
