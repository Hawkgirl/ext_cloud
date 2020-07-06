from ext_cloud.BaseCloud.BaseIdentity.BaseIdentity import BaseIdentitycls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls


class OpenStackIdentitycls(OpenStackBaseCloudcls, BaseIdentitycls):

    def __init__(self, **kwargs):
        super(OpenStackIdentitycls, self).__init__(credentials=kwargs)

    def list_metrics_all(self, dic):
        projects = self.list_projects()
        dic['openstack.toplevel.projects.projectscount'] = len(projects)
   
        for project in projects:
            project.list_metrics_all(dic)

        users = self.list_users()
        dic['openstack.toplevel.users.userscount'] = len(users)
        for user in users:
            user.list_metrics_all(dic) 


    @property
    def Childrens(self):
        return self.list_projects()

    def list_users_cache(self):
        from ext_cloud.utils.dogpile_utils import get_region
        from dogpile.cache.api import NO_VALUE

        region = get_region()

        users = region.get('users')
        if users is not NO_VALUE:
            return users
        dic = {}
        users = self.list_users()
        for user in users:
            dic[user.oid] = user.obj_to_dict()

        region.set('users', dic)
        return dic

    def list_users(self):
        from ext_cloud.OpenStack.OpenStackIdentity.OpenStackUser import OpenStackUsercls
        openstack_users = self._Clients.keystone.users.list()
        users = []
        for openstack_user in openstack_users:
            user = OpenStackUsercls(openstack_user, credentials=self._credentials)
            users.append(user)
        return users

    def get_user_by_id(self, user_id):
        from ext_cloud.OpenStack.OpenStackIdentity.OpenStackUser import OpenStackUsercls
        #from keystoneclient.openstack.common.apiclient.exceptions import NotFound
        #try:
        #    openstack_user = self._Clients.keystone.users.get(user_id)
        #except NotFound:
            # user got deleted
        #    return None

        openstack_user = self._Clients.keystone.users.get(user_id)
        user = OpenStackUsercls(openstack_user, credentials=self._credentials)
        return user

    def list_projects_cache(self):
        from dogpile.cache.api import NO_VALUE
        from ext_cloud.utils.dogpile_utils import get_region

        region = get_region()

        projects = region.get('projects')
        if projects is not NO_VALUE:
            return projects
        dic = {}
        projects = self.list_projects()
        for project in projects:
            dic[project.oid] = project.obj_to_dict()

        region.set('projects', dic)
        return dic

    def list_projects(self):
        from ext_cloud.OpenStack.OpenStackIdentity.OpenStackProject import OpenStackProjectcls
        openstack_projects = self._Clients.keystone.projects.list()
        projects = []
        for openstack_project in openstack_projects:
            project = OpenStackProjectcls(openstack_project, credentials=self._credentials)
            projects.append(project)
        return projects

    def get_project_by_id(self, project_id):
        from ext_cloud.OpenStack.OpenStackIdentity.OpenStackProject import OpenStackProjectcls
        #from keystoneclient.openstack.common.apiclient.exceptions import NotFound
        #try:
        #    openstack_project = self._Clients.keystone.projects.get(project_id)
        #except NotFound:
        #    return None
        openstack_project = self._Clients.keystone.projects.get(project_id)
        project = OpenStackProjectcls(openstack_project, credentials=self._credentials)
        return project

    def create_token(self):
        from ext_cloud.OpenStack.utils.OpenStackClients import OpenStackClientsCls
        from ext_cloud.OpenStack.OpenStackIdentity.OpenStackToken import OpenStackTokenCls
        #keystone_client = OpenStackClientsCls().get_keystone_client(self._credentials)
        keystone_client = OpenStackClientsCls(**self._credentials).keystone
        return OpenStackTokenCls(keystone_client, credentials=self._credentials)
