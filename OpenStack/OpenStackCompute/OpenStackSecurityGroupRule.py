
class OpenStackSecurityGroupRulecls():

    __ip_protocol = None
    __from_port = None
    __to_port = None
    __cidr_block = None
    __id = None

    def __init__(self, *args, **kwargs):
        self.__ip_protocol = kwargs['ip_protocol']
        self.__from_port = kwargs['from_port']
        self.__to_port = kwargs['to_port']
        self.__cidr_block = kwargs['cidr_block']
        self.__id = kwargs['id']

    @property
    def ip_protocol(self):
        return self.__ip_protocol

    @property
    def from_port(self):
        return self.__from_port

    @property
    def to_port(self):
        return self.__to_port

    @property
    def cidr_block(self):
        return self.__cidr_block

    @property
    def id(self):
        return self.__id
