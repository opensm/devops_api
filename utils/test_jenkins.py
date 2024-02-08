from __future__ import print_function
import time
import harbor_client
from harbor_client.rest import ApiException
from pprint import pprint


# # Configure HTTP basic authorization: basic
# configuration = harbor_client.Configuration()
# configuration.username = 'admin'
# configuration.password = 'VgcG8my.n'
# configuration.host = "https://harbor.newtsp.newcowin.com/api/v2.0"
#
# # create an instance of the API class
# api_instance = harbor_client.ProjectApi(harbor_client.ApiClient(configuration))
# # uid_list = harbor_client.LdapImportUsers() # LdapImportUsers | The uid listed for importing. This list will check users validity of ldap service based on configuration from the system.
# # x_request_id = 'x_request_id_example' # str | An unique ID for the request (optional)
# #
# # try:
# #     # Import selected available ldap users.
# #     api_instance.import_ldap_user(uid_list, x_request_id=x_request_id)
# # except ApiException as e:
# #     print("Exception when calling LdapApi->import_ldap_user: %s\n" % e)
# data = api_instance.get_project(project_name_or_id="ky-newtsp")
# print(data)
#

class HarborSDKManager:
    _configuration = None

    def connect(self, **kwargs):
        self._configuration = harbor_client.Configuration()

        for k, v in kwargs.items():
            if not hasattr(self._configuration, k):
                continue
            else:
                setattr(self._configuration, k, v)

    @property
    def ProjectApi(self):
        try:
            return harbor_client.ProjectApi(harbor_client.ApiClient(self._configuration))
        except AttributeError:
            raise ValueError("configuration is not available")

    @property
    def RegistryApi(self):
        try:
            return harbor_client.RegistryApi(harbor_client.ApiClient(self._configuration))
        except AttributeError:
            raise ValueError("configuration is not available")

    @property
    def ArtifactApi(self):
        try:
            return harbor_client.ArtifactApi(harbor_client.ApiClient(self._configuration))
        except AttributeError:
            raise ValueError("configuration is not available")

    @property
    def RepositoryApi(self):
        try:
            return harbor_client.RepositoryApi(harbor_client.ApiClient(self._configuration))
        except AttributeError:
            raise ValueError("configuration is not available")

    def get_project(self, name):
        return self.ProjectApi.get_project(project_name_or_id=name)

    def get_registry(self):
        return self.RegistryApi.list_registries()

    def get_repository(self, project_name):
        return self.RepositoryApi.list_repositories(project_name=project_name)

    def get_tags(self, project, repository_name, service_name):
        return self.ArtifactApi.list_tags(project_name=project, repository_name=repository_name, reference=service_name)

    def get_artifacts(self, project_name: str, repository_name: str, **kwargs):
        return self.ArtifactApi.list_artifacts(project_name=project_name, repository_name=repository_name, **kwargs)


hb = HarborSDKManager()
hb.connect(username="admin", password="VgcG8my.n", host="https://harbor.newtsp.newcowin.com/api/v2.0")
# project = hb.get_project("ky-newtsp")
# print(project)
repository = hb.get_repository("ky-newtsp")
print(repository)
# register = hb.get_registry()
# print(register)
# tags = hb.get_tags(project="ky-newtsp", repository_name="ky-newtsp/sms", service_name="20230728103758")
# print(tags)
data = hb.get_artifacts(project_name="ky-newtsp", repository_name="tsp-bss")
for xy in data:
    print(xy)

dd = {
    "component": {
        "key": "git.kyoffice.cn.ky.ari.newtsp.tencent.tsp-bss.master",
        "name": "git.kyoffice.cn.ky.ari.newtsp.tencent.tsp-bss.master",
        "qualifier": "TRK", "measures": [
            {"metric": "new_vulnerabilities", "period": {"index": 1, "value": "0", "bestValue": true}},
            {"metric": "vulnerabilities", "value": "1", "bestValue": false},
            {"metric": "duplicated_lines_density", "value": "8.4", "bestValue": false},
            {"metric": "coverage", "value": "0.0", "bestValue": false},
            {"metric": "bugs", "value": "12", "bestValue": false},
            {"metric": "new_bugs", "period": {"index": 1, "value": "0", "bestValue": true}}
        ]
    }
}
