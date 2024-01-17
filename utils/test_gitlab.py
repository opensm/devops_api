import gitlab


class GitlabAPI(object):

    def __init__(self, *args, **kwargs):
        self.gl = gitlab.Gitlab(
            url='https://git.kyoffice.cn',
            private_token='sFWaDy6fykEMpw5sJtks',  # 参数为gitlab仓库地址和个人private_take
            api_version='4'
        )

    def get_user_id(self, username):
        """
        通过用户名获取用户id
        :param username:
        :return:
        """
        user = self.gl.users.get_by_username(username)
        return user.id

    def get_group_id(self, groupname):
        """
        通过组名获取组id
        :param groupname:
        :return:
        """
        group = self.gl.groups.get(groupname, all=True)
        return group.id

    def get_user_projects(self, userid):
        """
        获取用户所拥有的项目
        :param userid:
        :return:
        """
        projects = self.gl.projects.owned(userid=userid, all=True)
        result_list = []
        for project in projects:
            result_list.append(project.http_url_to_repo)
        return result_list

    def get_group_projects(self, groupname):
        """
        获取组内项目！！！！！！！其他博客也有类似方法，实测不能拿到群组内项目，现经过小改动，亲测可满足要求
        :param groupname:
        :return:
        """
        group = self.gl.groups.get(groupname, all=True)
        projects = group.projects.list(all=True)
        return projects

    def getContent(self, projectID):
        """
        通过项目id获取文件内容
        :param projectID:
        :return:
        """
        projects = self.gl.projects.get(projectID)
        f = projects.files.get(file_path='指定项目中的文件路径', ref='master')
        content = f.decode()
        # print(content)
        return content.decode('utf-8')

    def get_all_group(self):
        """
        获取所有群组
        :return:
        """
        return self.gl.groups.list(all=True)

    def get_projects(self, key=None):
        if key:
            return self.gl.projects.list(keyword=key, get_all=True)
        else:
            return self.gl.projects.list(get_all=True)

    def get_project_branches(self, project_id):
        for x in self.get_projects():
            if x.id == project_id:
                return x.branches.list()
            else:
                continue
        return list()


g = GitlabAPI()
# data = g.get_project_branches(project_id=30)
# print(data)

d = g.get_projects(key="tsp-bss")
for x in d:
    print(x)