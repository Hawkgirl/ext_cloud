class BaseResourceUsagecls:

    __available_vms = None
    __free_vms = None
    __used_vms = None
    __deleted_vms = None
    __available_memory = None
    __free_memory = None
    __used_memory = None
    __hours_memory = None
    __available_disk = None
    __used_disk = None
    __free_disk = None
    __hours_disk = None
    __availble_cpus = None
    __used_cpus = None
    __free_cpus = None
    __hours_cpus = None

    def __init__(self, *args, **kwargs):
        for key in kwargs:
            attr = '_' + self.__class__.__name__ + '__' + key
            setattr(self, attr, kwargs[key])

    @property
    def available_vms(self):
        return self.__available_vms

    @property
    def free_vms(self):
        return self.__free_vms

    @property
    def used_vms(self):
        return self.__used_vms

    @property
    def deleted_vms(self):
        return self.__deleted_vms

    @property
    def available_memory(self):
        return self.__available_memory

    @property
    def free_memory(self):
        return self.__free_memory

    @property
    def used_memory(self):
        return self.__used_memory

    @property
    def hours_memory(self):
        return self.__hours_memory

    @property
    def available_disk(self):
        return self.__available_disk

    @property
    def used_disk(self):
        return self.__used_disk

    @property
    def free_disk(self):
        return self.__free_disk

    @property
    def hours_disk(self):
        return self.__hours_disk

    @property
    def availble_cpus(self):
        return self.__availble_cpus

    @property
    def used_cpus(self):
        return self.__used_cpus

    @property
    def free_cpus(self):
        return self.__free_cpus

    @property
    def hours_cpus(self):
        return self.__hours_cpus
