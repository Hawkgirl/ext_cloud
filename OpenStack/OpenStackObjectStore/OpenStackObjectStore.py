from BaseCloud.BaseObjectStore.BaseObjectStore import BaseObjectStorecls
from OpenStack.OpenStackObjectStore.OpenStackBucket import OpenStackBucketcls
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls


class OpenStackObjectStorecls(OpenStackBaseCloudcls, BaseObjectStorecls):
    __swiftclient = None

    def __init__(self, *args, **kwargs):
        self._credentials['username'] = kwargs['username']
        self._credentials['password'] = kwargs['password']
        self._credentials['region_name'] = kwargs['region_name']

    @property
    def __SwiftClient(self):
        return self.__swiftclient

    @__SwiftClient.getter
    def __SwiftClient(self):
        if self.__swiftclient is None:
            self.__swiftclient = s3.connect_to_region(
                self._credentials['region_name'],
                aws_access_key_id=self._credentials[
                    'username'],
                aws_secret_access_key=self._credentials['password'],
                calling_format=OrdinaryCallingFormat())
        return self.__swiftclient

    def get_all_buckets(self):
        pass

    def get_bucket_by_name(self, bucket_name):
        pass

    def create_bucket(self, bucket_name):
        pass
