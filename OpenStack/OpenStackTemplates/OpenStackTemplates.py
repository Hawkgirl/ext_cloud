from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls
from BaseCloud.BaseTemplates.BaseTemplates import BaseTemplatescls


class OpenStackTemplatescls(OpenStackBaseCloudcls, BaseTemplatescls):

    __heat = None

    def __init__(self, *args, **kwargs):
        self._credentials['username'] = kwargs['username']
        self._credentials['password'] = kwargs['password']
        self._credentials['region_name'] = kwargs['region_name']

    @property
    def __Heat(self):
        return self.__heat

    @__Heat.getter
    def __Heat(self):
        if self.__heat is None:
            # TODO
            self.__heat = "init heat connection here"
        return self.__heat

    def is_valid(self, *arg, **kwargs):
        if kwargs.has_key('file'):
            json_data = open(kwargs['file']).read()
        elif kwargs.has_key('data'):
            json_data = kwargs['data']

        else:
            raise Exception(
                "is_valid should have file=<filepath> or data=<data> as method args")
        # TODO
        #self.__heat.validate_template(template_body = json_data)
        return True

    def create_template(self):
        pass

    def get_all_templates(self):
        pass
