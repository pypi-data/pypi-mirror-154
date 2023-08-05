from seafileapi_extended.group import AdminGroup, Group
from seafileapi.exceptions import DoesNotExist
from seafileapi import client as client_groups
from seafileapi_extended.exceptions import GroupExisted


class Groups(client_groups.Groups):
    def __init__(self, client):
        self.client = client

    def create_group(self, name):
        url = '/api/v2.1/groups/'
        params = dict(name=name)
        resp_str = self.client.post(url, data=params,expected=[400,200,201])
        if resp_str.status_code == 400:
            raise GroupExisted  #The group has existed!
        else:
            resp_json = resp_str.json()

        return resp_json

    def get_group(self, name):
        '''
        :param name:
        :return:    [Group]
        '''
        url = "/api2/groups/"
        resp_json = self.client.get(url).json()

        group = None
        groups = resp_json.get("groups", [])
        for grp in groups:
            if grp["name"] == name:
                group = Group(self.client, grp["id"], grp["name"])
                break

        return group

    def rename_group(self, group_name, group_newname):
        '''
        Rename this group
        :param group_name: Existing group name
        :param group_newname: New group name
        :return: [Group]
        '''
        group = self.get_group(group_name)
        if not group:
            raise DoesNotExist(group_name)

        url = '/api2/groups/{group_id}/'.format(group_id=group.group_id)
        params = {'operation': 'rename',
                  'newname': group_newname}
        resp_str = self.client.post(url, data=params, expected=[200])
        group.group_name = group_newname  # Patch local object
        return group


class AdminGroups(Groups):
    def __init__(self, client):
        super().__init__(client)

    def list_groups(self):
        """
        :return:    [list(AdminGroup)]
        """

        url = "/api/v2.1/admin/groups/?page=1&per_page=1000"
        resp_json = self.client.get(url).json()

        resp_groups = resp_json.get("groups",[])
        groups = []

        for item in resp_groups:
            grp = AdminGroup(self.client,group_id=item["id"],group_name=item["name"], owner=item["owner"])
            groups.append(grp)
        return groups

    def get_group(self, group_name):
        '''
        :param group_name:
        :return:    [AdminGroup]
        '''
        grp_list = self.list_groups()

        group = None
        for grp in grp_list:
            if grp.group_name == group_name:
                group = grp
                break

        return group

    def remove_group(self, group_name):

        group = self.get_group(group_name)

        if group:
            self._remove_group(group.group_id)

    def _remove_group(self, group_id):
        url = "/api/v2.1/admin/groups/%d/" % (group_id,)
        self.client.delete(url)
