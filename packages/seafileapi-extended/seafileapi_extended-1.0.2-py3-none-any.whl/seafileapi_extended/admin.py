from seafileapi_extended.account import Account
from seafileapi_extended.exceptions import UserExisted, DoesNotExist


class SeafileAdmin(object):
    def __init__(self, client):
        self.client = client

    def lists_users(self, maxcount=100):
        pass

    def list_accounts(self, start=0, limit=100, scope=None):
        """
        Return a list of :class:`Account` objects. To retrieve all users, just set both start and limit to -1.
        :param start: (default to 0)
        :param limit: (default to 100)
        :param scope: (default None, accepted values: 'LDAP' or 'DB' or 'LDAPImport')
        :return:
        """
        accounts = self.client.get(
            "/api2/accounts/", params={"start": start, "limit": limit, "scope": scope}
        ).json()
        # return [Account.from_json(self.client, account) for account in accounts]
        return accounts

    def search_user(self, filter):
        """Search for user accounts, to be used by autocompleters"""
        params = {"q": filter}
        response = self.client.get("/api2/search-user", params=params)
        response_json = response.json()
        return response_json["users"]

    def get_user(self, email):
        account_json = self.client.get("/api2/accounts/{}/".format(email)).json()
        return Account.from_json(self.client, account_json)

    def create_user(self, email, password, is_active=True, is_staff=False):
        url = "/api2/accounts/{}/".format(email)
        params = {
            "password": password,
            "is_active": is_active and "true" or "false",
            "is_staff": is_staff and "true" or "false",
        }
        result = self.client.put(url, data=params, expected=[200, 201])
        if result.status_code == 201:
            return result.json()  # User created
        elif result.status_code == 200:
            raise UserExisted()

    def update_user(self, email, **kwargs):
        """Update a user account. Any of the following keys must be provided:
        - password, is_staff, is_active, name, note, storage."""
        url = "/api2/accounts/{}/".format(email)
        params = {}
        attrs = ["password", "is_active", "is_staff", "name", "note", "storage"]
        for attr in attrs:
            if attr in kwargs:
                val = kwargs.pop(attr)
                if val is not None:
                    params[attr] = val
        result = self.client.put(url, data=params, expected=[200, 201, 400])
        if result.status_code == 400:
            raise DoesNotExist("User {}".format(email))
        return True

    def delete(self, email):
        url = "/api2/accounts/{}/".format(email)
        result = self.client.delete(url, expected=[200, 202])
        if result.status_code == 200:
            return True
        elif result.status_code == 202:
            raise DoesNotExist("User {}".format(email))

    def list_user_repos(self, username):
        pass

    def is_exist_group(self, group_name):
        pass
