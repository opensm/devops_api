from __future__ import print_function
import time
import harbor_client


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


__all__ = ['HarborSDKManager']
