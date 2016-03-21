from BaseCloud.BaseTemplates.BaseTemplates import BaseTemplatescls
from AWS.AWSTemplates.AWSTemplate import AWSTemplatecls
from AWS.AWSBaseCloud import AWSBaseCloudcls
import json
from boto.cloudformation.connection import CloudFormationConnection


class AWSTemplatescls(AWSBaseCloudcls, BaseTemplatescls):

    __cloudformation = None

    def __init__(self, *args, **kwargs):
        self._credentials['username'] = kwargs['username']
        self._credentials['password'] = kwargs['password']
        self._credentials['region_name'] = kwargs['region_name']

    @property
    def __CloudFormation(self):
        return self.__cloudformation

    @__CloudFormation.getter
    def __CloudFormation(self):
        if self.__cloudformation is None:
            self.__cloudformation = CloudFormationConnection(aws_access_key_id=self._credentials[
                                                             'username'], aws_secret_access_key=self._credentials['password'])
        return self.__cloudformation

    def is_valid(self, *arg, **kwargs):
        if kwargs.has_key('file'):
            json_data = open(kwargs['file']).read()
        elif kwargs.has_key('data'):
            json_data = kwargs['data']

        else:
            raise Exception(
                "is_valid should have file=<filepath> or data=<data> as method args")
        self.__CloudFormation.validate_template(template_body=json_data)
        return True

    def create_template(self, *arg, **kwargs):
        if kwargs.has_key('file'):
            json_data = open(kwargs['file']).read()
        elif kwargs.has_key('data'):
            json_data = kwargs['data']
        else:
            raise Exception(
                "create_template should have file=<filepath> or data=<data> as method args")

        aws_template = self.__CloudFormation.create_stack(
            kwargs['name'], template_body=json_data)
        data = dict()
        data['id'] = aws_template
        data['name'] = kwargs['name']

        return AWSTemplatecls(data, credentials=self._credentials)

    def get_template_by_name(self, name):
        templates = self.get_all_templates()
        for template in templates:
            if template.name == name:
                return template
        return None

    def get_template_by_id(self, template_id):
        templates = self.get_all_templates()
        for template in templates:
            if template.id == template_id:
                return template
        return None

    def get_all_templates(self):
        stacks = self.__CloudFormation.list_stacks()
        templates = []
        for stack in stacks:
            data = dict()
            data['id'] = stack.stack_id
            data['name'] = stack.stack_name
            template = AWSTemplatecls(data, credentials=self._credentials)
            templates.append(template)
        return templates
